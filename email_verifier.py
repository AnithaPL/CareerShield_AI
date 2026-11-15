
import re


PUBLIC_EMAIL_DOMAINS = {
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "hotmail.com",
}


def verify_email(email):
    email = email.strip().lower()

    result = {
        "email": email,
        "domain": "",
        "valid_format": False,
        "email_type": "Unknown",
        "message": ""
    }

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(pattern, email):
        result["message"] = "Invalid email format."
        return result

    domain = email.rsplit("@", 1)[1]
    result["domain"] = domain

    if domain in PUBLIC_EMAIL_DOMAINS:
        result["email_type"] = "Public Email Provider"
        result["message"] = (
            "Invalid for recruiter domain verification: this address uses "
            "a public email provider. Use the organization's domain instead."
        )
    else:
        result["valid_format"] = True
        result["email_type"] = "Domain-Specific Email"
        result["message"] = (
            "This address uses a domain-specific email address. This does "
            "not prove the sender owns the company or is legitimate; verify "
            "the domain through an official source."
        )

    return result