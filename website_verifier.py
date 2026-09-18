
from urllib.parse import urlparse


def verify_website(url):
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)

    result = {
        "url": url,
        "valid_format": False,
        "uses_https": parsed.scheme == "https",
        "domain": parsed.netloc,
        "message": ""
    }

    if not parsed.netloc or "." not in parsed.netloc:
        result["message"] = "Invalid website URL."
        return result

    result["valid_format"] = True

    if result["uses_https"]:
        result["message"] = (
            "Valid URL with HTTPS. "
            "HTTPS does not prove company authenticity."
        )
    else:
        result["message"] = (
            "Website does not use HTTPS. "
            "Avoid sharing sensitive information."
        )

    return result