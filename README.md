# CareerShield AI

An Intelligent Career Safety Platform for Recruitment Fraud Detection Using Explainable Artificial Intelligence (XAI)

Explainable AI Based Recruitment Fraud Detection System.

## Modules
- Job Scam Detection: Genuine / Suspicious / Likely Scam
- Recruiter Email Verification
- Resume Privacy Analyzer
- Explainable Risk Score
- Analysis History
- PDF Offer Letter Verification
- LinkedIn/Job URL Analysis
- Company Website Verification
- WhatsApp/Telegram Screenshot OCR
- AI Chat Assistant

## Stack
Python 3.10+, Flask, scikit-learn, pandas, joblib, PyMuPDF, Pillow, pytesseract, dnspython, requests, BeautifulSoup.

## Model
The supplied documents specify NLP, ML and XAI but do not prescribe a particular algorithm or dataset. This prototype therefore uses an interpretable TF-IDF + Logistic Regression classifier trained on a small project seed dataset. XAI is provided by showing influential TF-IDF features, while a transparent rule engine detects payment, OTP/password, sensitive-data, urgency and similar signals. The final risk score combines ML class information with rule signals.

## Install
1. Install Python 3.10+.
2. `python -m venv .venv`
3. Windows: `.venv\\Scripts\\activate` (PowerShell: `.\\.venv\\Scripts\\Activate.ps1`)
4. `pip install -r requirements.txt`
5. `python scripts/train_model.py`
6. `python run.py`
7. Open http://127.0.0.1:5000

### OCR
Screenshot analysis additionally needs Tesseract OCR installed on the OS and available on PATH. No separate SQL server is required; SQLite is built into Python.

## Academic scope note
The source documents list Browser Extension and Multi-language Support as future enhancements. They are not implemented here because the documents do not provide implementation details for them. The AI Chat Assistant is a safety-focused rule assistant, not a claimed large language model.
