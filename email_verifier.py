
import re


def verify_email(email):
    email = email.strip().lower()

    result = {
        "email": email,
        "valid_format": False,
        "email_type": "Unknown",
        "message": ""
    }

    # Check email format
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.match(pattern, email):
        result["message"] = "Invalid email format."
        return result

    result["valid_format"] = True

    # Extract domain
    domain = email.split("@")[1]

    # Common free email providers
    free_providers = [
        "gmail.com",
        "yahoo.com",
        "outlook.com",
        "hotmail.com"
    ]

    if domain in free_providers:
        result["email_type"] = "Free Email Provider"
        result["message"] = (
            "Recruiter uses a free email provider. "
            "Verify the company independently."
        )
    else:
        result["email_type"] = "Business Domain"
        result["message"] = (
            "Business domain detected. "
            "Domain ownership and company authenticity "
            "still require independent verification."
        )

    return result