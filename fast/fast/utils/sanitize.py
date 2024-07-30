def sanitize(string):
    alpha = ''.join(
        char for char in string if char.isalnum() or char.isspace()
    )
    sanitized = ' '.join(alpha.split()).lower()
    return sanitized
