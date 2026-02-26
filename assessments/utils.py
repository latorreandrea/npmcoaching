import hashlib


def session_fingerprint(session_key):
    if not session_key:
        return ""
    return hashlib.sha256(session_key.encode("utf-8")).hexdigest()
