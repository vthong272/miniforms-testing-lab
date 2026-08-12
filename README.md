# MiniForms Testing Lab

A pure HTML/CSS/JavaScript target application for comparing Equivalence Partitioning, Boundary Value Analysis, and Decision Table Testing on web-form business logic.

## Run the application

```powershell
cd miniforms-study
python -m http.server 8000 --directory app
```

Open `http://localhost:8000/`.

## Run JavaScript unit tests

```powershell
npm test
```

## Run Selenium smoke tests

Keep the local server running in one terminal. In another terminal:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest tests/selenium -v
```

`tests/selenium/test_golden_smoke.py` is only a golden-version sanity check. The EP, BVA, and Decision Table research suites should be created separately after the requirements are reviewed and frozen.

### Run the Registration BVA suite

```powershell
pytest tests/bva/test_registration_bva.py -v
```

The 18 frozen BVA cases are stored in `test-design/bva-registration.csv`.

## Deploy to Vercel

Import the repository with the project root unchanged. `vercel.json` disables framework builds and serves the static files from `app/`.
