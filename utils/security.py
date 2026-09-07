from werkzeug.security import check_password_hash, generate_password_hash

# Password helpers keep plain-text passwords out of the database.


def hash_password(plain_password):
    """Return a one-way hash for a password."""
    # Werkzeug creates a salted hash; the original password is not stored.
    return generate_password_hash(plain_password)


def verify_password(plain_password, password_hash):
    """Check a password against its stored hash."""
    return check_password_hash(password_hash, plain_password)
