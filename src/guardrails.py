import re
from decimal import Decimal, InvalidOperation
from typing import Any

import pandas as pd


_NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)"
_HR_PATTERN = re.compile(
    rf"\b(?:heart\s*rate|hr|pulse)\b"
    rf"\s*(?:(?:is|was|of|at|reading)\s*)?(?:[:=]\s*)?"
    rf"(?P<value>{_NUMBER})"
    rf"(?:\s*(?:-|–|to)\s*(?P<range_end>{_NUMBER}))?",
    re.IGNORECASE,
)
_BP_PATTERN = re.compile(
    rf"\b(?:blood\s+pressure|bp)\b"
    rf"\s*(?:(?:is|was|of|reading)\s*)?(?:[:=]\s*)?"
    rf"(?P<systolic>{_NUMBER})\s*(?:/|over)\s*(?P<diastolic>{_NUMBER})",
    re.IGNORECASE,
)
_SYSTOLIC_PATTERN = re.compile(
    rf"\b(?:systolic|sys)\b(?:\s+(?:blood\s+)?pressure)?(?:\s+bp)?"
    rf"\s*(?:(?:is|was|of|at|reading)\s*)?(?:[:=]\s*)?"
    rf"(?P<value>{_NUMBER})",
    re.IGNORECASE,
)
_DIASTOLIC_PATTERN = re.compile(
    rf"\b(?:diastolic|dia)\b(?:\s+(?:blood\s+)?pressure)?(?:\s+bp)?"
    rf"\s*(?:(?:is|was|of|at|reading)\s*)?(?:[:=]\s*)?"
    rf"(?P<value>{_NUMBER})",
    re.IGNORECASE,
)


def _decimal(value: Any) -> Decimal | None:
    if pd.isna(value):
        return None
    try:
        return Decimal(str(value).strip())
    except (InvalidOperation, ValueError):
        return None


def validate_generated_email(
    email: str,
    anomalies: pd.DataFrame,
    patient_id: str,
) -> dict[str, Any]:
    """Block an email if its stated heart rate or blood pressure differs from anomalies."""
    required_columns = {"patient_id", "hr", "sys", "dia"}
    missing_columns = required_columns.difference(anomalies.columns)
    if missing_columns:
        return {
            "approved": False,
            "text": "",
            "hallucinations": [],
            "reason": f"Source data is missing columns: {', '.join(sorted(missing_columns))}",
        }

    patient_rows = anomalies.loc[
        anomalies["patient_id"].astype(str) == str(patient_id)
    ]
    if len(patient_rows) != 1:
        return {
            "approved": False,
            "text": "",
            "hallucinations": [],
            "reason": f"Expected exactly one source row for patient_id {patient_id!r}; found {len(patient_rows)}",
        }

    row = patient_rows.iloc[0]
    claims: list[tuple[str, str, str]] = []

    for match in _BP_PATTERN.finditer(email):
        claims.append(("systolic blood pressure", "sys", match.group("systolic")))
        claims.append(("diastolic blood pressure", "dia", match.group("diastolic")))

    for pattern, label, column in (
        (_SYSTOLIC_PATTERN, "systolic blood pressure", "sys"),
        (_DIASTOLIC_PATTERN, "diastolic blood pressure", "dia"),
    ):
        for match in pattern.finditer(email):
            claims.append((label, column, match.group("value")))

    hallucinations = []
    for match in _HR_PATTERN.finditer(email):
        claimed = match.group("value")
        range_end = match.group("range_end")
        if range_end is not None:
            hallucinations.append(
                f"Heart-rate range {claimed}-{range_end} is not an exact source value."
            )
        else:
            claims.append(("heart rate", "hr", claimed))

    for label, column, claimed_text in claims:
        claimed_value = _decimal(claimed_text)
        source_value = _decimal(row[column])
        if source_value is None or claimed_value is None:
            hallucinations.append(
                f"Could not verify {label} value {claimed_text!r} against the source row."
            )
        elif claimed_value != source_value:
            hallucinations.append(
                f"{label.title()} value {claimed_text} does not match source value {row[column]}."
            )

    approved = not hallucinations
    return {
        "approved": approved,
        "text": email if approved else "",
        "hallucinations": hallucinations,
        "reason": "Validated against the source row." if approved else "Email blocked due to unverified vital signs.",
    }