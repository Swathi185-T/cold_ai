# ColdChain AI

Prediction-guided cold-chain monitoring: temporal forecasts are converted to configurable risk, then used by a two-objective non-dominated optimizer to recommend cooling actions. Demonstration data is explicitly simulated.

## Run

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations monitoring
python manage.py migrate
python manage.py runserver
```

The dashboard is at http://127.0.0.1:8000/. Use `core.prediction_guided_optimization()` for the integrated programmatic pipeline.
