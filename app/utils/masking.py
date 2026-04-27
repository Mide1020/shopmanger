def mask_email(email: str) -> str:
    """Return a privacy-safe version of an email for logging.

    Examples:
        john@example.com  →  j***@example.com
        ab@example.com    →  a***@example.com
        a@example.com     →  ***@example.com
    """
    try:
        local, domain = email.split("@", 1)
        masked_local = (local[0] + "***") if len(local) > 1 else "***"
        return f"{masked_local}@{domain}"
    except Exception:
        return "***@***"
