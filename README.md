# CareerShield AI

An Intelligent Career Safety Platform for Recruitment Fraud Detection Using Explainable Artificial Intelligence (XAI).

## Implemented Modules

- Job Scam Detection: TF-IDF and Logistic Regression prediction, rule-based warnings, risk score, and explanations.
- Resume Privacy Analyzer: detects phone, email, PAN, Aadhaar, passport, and bank-account information.
- Recruiter Email Verification: validates email format and identifies free or business domains.
- Website Verification: validates URLs and checks HTTPS availability.
- Analysis History: stores and displays previous analyses with pagination and filters.

The application also provides user registration, password login, logout, and user-specific analysis history.

## Technology Stack

- Python 3.10+
- Flask
- scikit-learn
- pandas
- joblib
- SQLite
- HTML and CSS

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

5. Start the application:

	```powershell
	python app.py
	```

6. Open http://127.0.0.1:5000 and create an account.

SQLite is included with Python. The local `history.db` file stores users and analysis history and is excluded from Git.

## Application Routes

- `/` - Home dashboard
- `/analyze` - Job Scam Detection
- `/privacy` - Resume Privacy Analyzer
- `/email` - Recruiter Email Verification
- `/website` - Website Verification
- `/history` - Analysis History
- `/login` - User login
- `/register` - Account registration
- `/logout` - Sign out

## Future Scope

PDF offer-letter verification, LinkedIn and job-URL analysis, WhatsApp or Telegram screenshot OCR, multilingual support, browser extension support, and an AI chat assistant can be added in future versions.
