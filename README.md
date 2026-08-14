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

## Run the frozen Selenium suites on the golden version

The pytest fixture starts the golden application automatically on
`http://127.0.0.1:8765/`, launches one headless Chrome session, and shuts both
down after the run:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
.venv\Scripts\python.exe -m pytest tests/selenium/test_frozen_golden.py -v
```

The Frozen v1.0 manifest contains exactly 110 unique cases:

- EP: 30 cases
- BVA: 51 cases
- Decision Table Testing: 29 cases

Run one technique independently with `-m ep`, `-m bva`, or `-m dtt`. Every
case uses its frozen test ID in pytest output. To run against another golden
deployment, set `MINIFORMS_URL` before invoking pytest.

### Legacy Registration-only BVA suite

```powershell
pytest tests/bva/test_registration_bva.py -v
```

This older 18-case file remains for traceability. The authoritative Frozen
v1.0 research manifest is `tests/frozen_cases.py` and covers all three forms.

## Deploy to Vercel

Import the repository with the project root unchanged. `vercel.json` disables framework builds and serves the static files from `app/`.

## Reproduce the mutation experiment

Frozen v1.0 is protected by a recorded SHA-256 fingerprint. Generate and verify
the 18 single-fault mutants, then run the three suites against golden and every
mutant:

```powershell
.venv\Scripts\python.exe -m scripts.generate_mutants
.venv\Scripts\python.exe -m scripts.verify_mutants
.venv\Scripts\python.exe -m scripts.run_experiment
.venv\Scripts\python.exe -m scripts.analyze_results <result-directory>
```

The experiment runner creates a new result directory, checks the frozen hash,
requires all golden tests to pass, and classifies a mutant as killed only when
the complete suite has assertion failures but no errors or skipped tests. It
refuses to reuse a non-empty output directory.
