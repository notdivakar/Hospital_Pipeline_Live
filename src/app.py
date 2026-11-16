import inspect
import subprocess
import sys
from importlib import import_module
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware


PROJECT_ROOT = Path(__file__).resolve().parent.parent

app = FastAPI(title="Hospital Pipeline API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/run")
def run_pipeline():
    """Execute the project pipeline defined in main.py."""
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "main.py")],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Pipeline execution failed",
                "stdout": result.stdout,
                "stderr": result.stderr,
            },
        )

    return {"status": "success", "output": result.stdout}


@app.get("/alerts")
async def get_alerts():
    """Return AI-generated doctor emails from the LLM agent."""
    try:
        llm_agent = import_module("src.llm_agent")
    except ModuleNotFoundError as exc:
        raise HTTPException(
            status_code=500,
            detail="src.llm_agent is not available",
        ) from exc

    generator = getattr(llm_agent, "generate_doctor_emails", None)
    if generator is None:
        raise HTTPException(
            status_code=500,
            detail="src.llm_agent.generate_doctor_emails is not available",
        )

    emails = generator()
    if inspect.isawaitable(emails):
        emails = await emails

    return {"emails": emails}
