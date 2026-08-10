from backend.app import create_app

app = create_app()

# Run with:
#   cd museum
#   .\.venv\Scripts\Activate.ps1
#   $env:PYTHONPATH = "."
#   python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000