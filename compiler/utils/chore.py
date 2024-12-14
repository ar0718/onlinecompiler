def is_valid_email(email :str) -> bool:
    at = 0
    dot = 0
    for char in email:
        if char == '@':
            at += 1

        if char == '.':
            if at == 1:
                dot += 1
            else:
                return False
    
    return at == 1 and dot == 1
        