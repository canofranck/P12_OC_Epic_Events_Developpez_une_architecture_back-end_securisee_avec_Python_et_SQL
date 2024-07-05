import re


EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"
REG_EX_PHONE = r"^\+33[1-9][0-9]{8}$"


def validate_email(email):
    """
    Validates an email address using a regular expression.

    This function checks if the provided email address matches the regular expression for a valid email address.
    If the email is not valid, a ValueError is raised.

    Returns:
        email: The validated email address.
    """
    if not re.match(EMAIL_REGEX, email):
        raise ValueError("email not valid")
    return email


def validate_password(password):
    """
    Validates a password.

    This function checks if the provided password is not empty. If the password is empty, a ValueError is raised.

    Returns:
        password: The validated password.
    """
    if password == "":
        raise ValueError("emai not valid")
    return password


def validate_phone(phone):
    """
    Validates a phone number using a regular expression.

    This function checks if the provided phone number matches the regular expression for a valid phone number.
    If the phone number is not valid, a ValueError is raised.

    Returns:
        phone: The validated phone number.
    """
    if not re.match(REG_EX_PHONE, phone):
        raise ValueError("Phone number not valid")
    return phone


def validate_date(start_date, end_date):
    """
    Validates a date range.

    This function checks if the provided start date is before the end date. If the start date is after the end date, a ValueError is raised.

    Returns:
        start_date, end_date: The validated start and end dates.
    """
    if start_date > end_date:
        raise ValueError("period not valid")
    return start_date, end_date
