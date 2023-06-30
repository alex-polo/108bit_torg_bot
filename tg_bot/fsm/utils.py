def is_float(text: str) -> bool:
    try:
        float(text)
        return True
    except Exception:
        return False
