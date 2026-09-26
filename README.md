# CareerShield AI

An Intelligent Career Safety Platform for Recruitment Fraud Detection Using Explainable Artificial Intelligence (XAI).

## Abstract

CareerShield AI is a web-based platform that helps job seekers recognize warning signs in job advertisements and protect sensitive information in resumes. It combines TF-IDF text processing, machine learning, and rule-based checks to provide risk assessments and explanations. The platform also performs basic recruiter email-format and domain-category checks, along with website URL and HTTPS checks. Its results are intended as guidance and do not guarantee that a job, recruiter, or website is legitimate.

## Implemented Modules

- Job Scam Detection: TF-IDF and Logistic Regression prediction, rule-based warnings, risk score, and explanations.
- Resume Privacy Analyzer: detects phone, email, PAN, Aadhaar, passport, and bank-account information.
- Recruiter Email Verification: validates email format and identifies free or business domains.
- Website Verification: validates URLs and checks HTTPS availability.
- Analysis History: stores and displays previous analyses with pagination and filters.

The application also provides user registration, password login, logout, and user-specific analysis history.

## Python Files

- `app.py` - Starts the Flask web application and defines routes for registration, login, local password reset, job analysis, resume privacy analysis, recruiter email checks, website checks, and user history.
- `analyzer.py` - Loads the trained job-classification pipeline and combines its prediction with rule-based warning checks to produce risk scores and explanations.
- `email_verifier.py` - Checks email address format and classifies the address as a common free-provider or business domain; it does not verify the sender or detect phishing.
- `history_db.py` - Creates and accesses the SQLite `users` and `analysis_history` tables, including user creation, password updates, and per-user history.
- `privacy_analyzer.py` - Searches resume text for patterns resembling phone numbers, email addresses, PAN, Aadhaar, passport, and bank-account details, then calculates a privacy score.
- `train_model.py` - Loads and prepares the EMSCAD dataset, trains and evaluates the TF-IDF and Logistic Regression pipeline, and saves it to `models/scam_pipeline.joblib`.
- `website_verifier.py` - Parses website URLs and checks their format and HTTPS scheme; it does not contact the site or confirm domain ownership.

## Technology Stack

- Python 3.10+
- Flask
- scikit-learn
- pandas
- joblib
- SQLite
- HTML and CSS

## UI Background

The app uses a two-tone light blue-to-white page background defined in `static/style.css`; no background image is required.

## System Design Diagrams

- [System Design - DFD and Flowchart](docs/system-design-dfd-flowchart.md)
- [System Design - UML and ER Diagram](docs/system-design-uml-er.md)
- [DFD and Flowchart SVG preview](static/system_design_flow.svg)
- [UML and ER SVG preview](static/system_design_uml_er.svg)
- [Testing Workflow diagram](docs/testing-workflow.svg)

## Job Analysis Method

1. TF-IDF converts the job advertisement into numerical text features.
2. Logistic Regression produces the original ML prediction: `Genuine` or `Likely Scam`.
3. Transparent security rules detect payment requests, urgency, OTPs, credentials, personal documents, messaging-app recruitment, and other warning signals.
4. The ML prediction, confidence, and rule-based score are combined into the final prediction: `Genuine`, `Suspicious`, or `Likely Scam`.

## Installation

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

4. Train the model if the model file needs to be regenerated:

	```powershell
	python train_model.py
	```

5. To enable local password reset, set an admin key in PowerShell. Keep this value private and use a long random value:

	```powershell
	$env:CAREERSHIELD_RESET_KEY = "replace-with-a-long-random-key"
	```

6. Start the application in the same PowerShell session:

	```powershell
	python app.py
	```

7. Open http://127.0.0.1:5000 and create an account.

SQLite is included with Python. The local `history.db` file stores users and analysis history and is excluded from Git.

## Application Routes

- `/` - Home dashboard
- `/analyze` - Job Scam Detection
- `/privacy` - Resume Privacy Analyzer
- `/email` - Recruiter Email Verification
- `/website` - Website Verification
- `/history` - Analysis History
- `/login` - User login
- `/reset-password` - Local admin-key password reset
- `/register` - Account registration
- `/logout` - Sign out

## Future Scope

PDF offer-letter verification, LinkedIn and job-URL analysis, WhatsApp or Telegram screenshot OCR, multilingual support, browser extension support, and an AI chat assistant can be added in future versions.
