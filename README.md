---
title: CareerShield AI
sdk: docker
app_port: 7860
---

# CareerShield AI

CareerShield AI is a Flask web application that provides basic recruitment-safety checks. It analyzes job-ad text, scans pasted resume text for selected sensitive-data patterns, classifies recruiter email domains, and checks website URL format and HTTPS usage. Results are screening guidance only; they do not prove that a job, recruiter, email address, or website is legitimate.

## Features

- **Job Scam Detection:** A TF-IDF and Logistic Regression pipeline predicts `Genuine` or `Likely Scam`. Rule-based checks look for warning signals and produce a risk score and explanations. The final result is `Genuine`, `Suspicious`, or `Likely Scam`; confidence is shown separately. A risk score of 60 or higher produces `Likely Scam`. A high-confidence ML scam result (90% or higher) also produces `Likely Scam`; a lower-confidence ML scam result is `Suspicious`.
- **Resume Privacy Analysis:** Scans pasted text for patterns resembling phone numbers, email addresses, PAN, Aadhaar, passport, and bank-account details. The privacy score is based on the number of detected categories. This pattern-based scan may miss information or flag unrelated text.
- **Recruiter Email Verification:** Checks basic email syntax and extracts the domain. The configured public-provider domains (`gmail.com`, `yahoo.com`, `outlook.com`, and `hotmail.com`) are marked invalid for this module's recruiter-domain check. Other syntactically valid domains are labeled domain-specific. This does not confirm mailbox existence, domain ownership, or recruiter identity.
- **Website Verification:** Checks a basic URL structure and HTTPS scheme. URLs without a scheme are treated as HTTPS URLs. HTTP URLs with a valid-looking domain are marked `HTTPS Disabled` and `Valid Format: No`; HTTPS URLs with a valid-looking domain are marked valid. The app does not contact the website or verify ownership, certificate trust, or legitimacy.
- **Analysis History:** Stores each signed-in user's submitted analysis input, result, and timestamp in SQLite; history can be filtered and paginated.
- **Accounts:** Registration, login, logout, and optional local password reset. Passwords are stored as hashes.

## Technology

- Python 3.10+
- Flask
- scikit-learn, pandas, and joblib
- SQLite
- HTML and CSS
- Docker and Gunicorn for the container deployment

## Project Files

- `app.py` - Flask routes, authentication, and feature integration.
- `analyzer.py` - Loads the trained job-classification pipeline and combines its output with rule-based warning checks.
- `email_verifier.py` - Email syntax check and public-provider/domain-specific classification.
- `website_verifier.py` - URL parsing and HTTPS classification; does not make network requests.
- `privacy_analyzer.py` - Pattern-based sensitive-data scan of pasted resume text.
- `history_db.py` - SQLite account and analysis-history operations.
- `train_model.py` - Trains and evaluates the TF-IDF and Logistic Regression pipeline using `data/emscad_dataset.csv`.
- `models/scam_pipeline.joblib` - Trained model loaded by the application.
- `static/careershield-logo.svg` - Shield logo SVG asset.
- `static/style.css` - Application styles.
- `tests/` - Unit tests for analyzers and verification modules.
- `Dockerfile` - Runs the application with Gunicorn on port 7860.

## Run Locally

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

4. Set a unique secret key before running the app:

   ```powershell
   $env:CAREERSHIELD_SECRET_KEY = "replace-with-a-long-random-secret"
   ```

5. Optionally enable local password reset by setting a separate reset key:

   ```powershell
   $env:CAREERSHIELD_RESET_KEY = "replace-with-a-separate-long-random-key"
   ```

6. Start the development server:

   ```powershell
   python app.py
   ```

7. Open <http://127.0.0.1:5000> and register an account.

The app creates `history.db` in its working directory. Analysis history includes the submitted input, so avoid using real sensitive resume or account information for demonstrations. `history.db` is excluded from Git.

## Train the Job Model

The repository includes a trained model at `models/scam_pipeline.joblib`, so training is not required for normal use. To retrain it, ensure `data/emscad_dataset.csv` is available and run:

```powershell
python train_model.py
```

The script reports evaluation metrics and saves the resulting pipeline to `models/scam_pipeline.joblib`.

## Run Tests

```powershell
python -m unittest discover -s tests -v
```

## Docker

Build and run the container from the project root:

```powershell
docker build -t careershield-ai .
docker run --rm -p 7860:7860 `
  -e CAREERSHIELD_SECRET_KEY="replace-with-a-long-random-secret" `
  careershield-ai
```

Then open <http://127.0.0.1:7860>. For persistent history between container runs, configure a persistent volume for `history.db`.

## Routes

| Route | Feature |
|---|---|
| `/` | Home dashboard (requires login) |
| `/analyze` | Job Scam Detection |
| `/privacy` | Resume Privacy Analysis |
| `/email` | Recruiter Email Verification |
| `/website` | Website Verification |
| `/history` | Analysis History |
| `/register` | Account registration |
| `/login` | Login |
| `/reset-password` | Optional local password reset |
| `/logout` | Sign out |

## System Design

- [System Design - DFD and Flowchart](docs/system-design-dfd-flowchart.md)
- [System Design - UML and ER Diagram](docs/system-design-uml-er.md)
- [DFD and Flowchart SVG preview](static/system_design_flow.svg)
- [UML and ER SVG preview](static/system_design_uml_er.svg)
- [Testing Workflow diagram](docs/testing-workflow.svg)

## Future Scope

Possible future enhancements include resume file uploads, more advanced website checks, multilingual analysis, a larger training dataset, and additional job-source integrations.
