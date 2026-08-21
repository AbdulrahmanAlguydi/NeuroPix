from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(plain_password):
    """
    Converts a plain-text password into a secure one-way hash.
    """
    return generate_password_hash(plain_password)


def verify_password(plain_password, password_hash):
    """
    Checks a plain-text password against a previously stored hash.
    Returns True if they match, False otherwise.
    """
    return check_password_hash(password_hash, plain_password)
