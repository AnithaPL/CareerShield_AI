
from urllib.parse import urlparse


def verify_website(url):
    url = url.strip()

    parsed = urlparse(url)
    if not parsed.scheme:
        url = "https://" + url
        parsed = urlparse(url)

    domain = parsed.netloc
    hostname = parsed.hostname or ""
    uses_https = parsed.scheme.lower() == "https"

    result = {
        "url": url,
        "valid_format": False,
        "uses_https": uses_https,
        "https_disabled": False,
        "domain": domain,
        "message": ""
    }

    if (
        parsed.scheme.lower() not in ("http", "https")
        or not hostname
        or "." not in hostname
    ):
        result["message"] = "Invalid website URL."
        return result

    if not uses_https:
        result["https_disabled"] = True
        result["message"] = (
            "HTTPS is disabled. This URL is invalid for website verification."
        )
        return result

    result["valid_format"] = True
    result["message"] = (
        "Valid URL with HTTPS. "
        "HTTPS does not prove company authenticity."
    )

    return result