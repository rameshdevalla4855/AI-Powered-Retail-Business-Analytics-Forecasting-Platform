import subprocess
import sys

subprocess.run([
    sys.executable,
    "-m",
    "streamlit",
    "run",
    "dashboard/Home.py"
])