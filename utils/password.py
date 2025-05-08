import string


def strong_password_check(password):
    """
        Return True if password has ascii lower, upper, digit and punctuation. \n
        Otherwise return False.
    """
    has_lower = any(char in string.ascii_lowercase for char in password)
    has_upper = any(char in string.ascii_uppercase for char in password)
    has_digit = any(char in string.digits for char in password)
    has_punctuation = any(char in string.punctuation for char in password)

    if has_lower and has_upper and has_digit and has_punctuation:
        return True

    return False
