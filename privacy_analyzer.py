
import re


def analyze_resume(text):
    findings = []

    patterns = {
        "Phone Number": r"\b\d{10}\b",
        "Email Address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "PAN Number": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
        "Aadhaar Number": r"\b\d{4}\s?\d{4}\s?\d{4}\b",
        "Passport Number": r"\b[A-Z][0-9]{7}\b",
        "Bank Account Number": r"(?i)(?:account number|a/c number|bank account)[:\s-]*\d{9,18}\b",
    }

    for category, pattern in patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)

        if matches:
            findings.append({
                "type": category,
                "count": len(matches),
                "message": f"Possible {category} detected."
            })

    privacy_score = min(len(findings) * 15, 100)

    return {
        "privacy_score": privacy_score,
        "findings": findings
    }