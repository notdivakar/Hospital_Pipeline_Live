import os
from PIL import Image
import requests
import streamlit as st

st.set_page_config(
    page_title="Hospital Pipeline & Vitals Dashboard", layout="wide"
)

st.title("🏥 Hospital Pipeline & Vitals Intelligence")

# Sidebar controls
st.sidebar.header("Control Center")
if st.sidebar.button("Run Pipeline"):
  try:
    response = requests.post("http://127.0.0.1:8000/run")
    if response.status_code == 200:
      st.sidebar.success("Pipeline executed successfully!")
    else:
      st.sidebar.error(f"Execution failed: {response.text}")
  except requests.exceptions.ConnectionError:
    st.sidebar.error("Could not connect to FastAPI backend at 127.0.0.1:8000")

# Main window layout
col1, col2 = st.columns([2, 1])

with col1:
  st.header("📈 Heart Rate Trends")
  img_path = "visualizations/hr_trend.png"
  if os.path.exists(img_path):
    image = Image.open(img_path)
    st.image(image, caption="Patient Heart Rate Trends", use_container_width=True)
  else:
    st.warning(
        "Visualization not found. Click 'Run Pipeline' to generate the trend"
        " plot."
    )

with col2:
  st.header("🚨 AI-Generated Alerts")
  try:
    alerts_res = requests.get("http://127.0.0.1:8000/alerts")
    if alerts_res.status_code == 200:
      alerts = alerts_res.json()
      if alerts:
        # Assuming alerts is a list of strings or dictionaries
        for alert in alerts:
          st.error(
              f"⚠️ {alert.get('message', alert) if isinstance(alert, dict) else alert}"
          )
      else:
        st.success("No active anomalies detected.")
    else:
      st.error("Failed to fetch alerts.")
  except requests.exceptions.ConnectionError:
    st.info(
        "Backend offline. Start FastAPI to view real-time dynamic AI alerts."
    )