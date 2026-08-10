# Run this from inside the "museum" folder (PowerShell)
# One-time setup:
#   python -m venv .venv
#   .\.venv\Scripts\Activate.ps1
#   pip install -r requirements.txt
#
# Every time you want to run the backend:
#   .\.venv\Scripts\Activate.ps1
#   .\run_backend.ps1

$env:PYTHONPATH = "."
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
