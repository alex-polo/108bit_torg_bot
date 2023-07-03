def point_deletion(text: str) -> str:
    if len(text) > 0 and text[-1] == '.':
        return text[:-1]
    else:
        return text
