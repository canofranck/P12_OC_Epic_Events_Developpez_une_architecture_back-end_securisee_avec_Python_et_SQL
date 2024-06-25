import re


EMAIL_REGEX = r"[^@]+@[^@]+\.[^@]+"
REG_EX_PHONE = r"^\+33[1-9][0-9]{8}$"


def validate_email(email):
    if not re.match(EMAIL_REGEX, email):
        raise ValueError("email not valid")
    return email


def validate_password(password):
    if password == "":
        raise ValueError("emai not valid")
    return password


def validate_phone(phone):
    if not re.match(REG_EX_PHONE, phone):
        raise ValueError("Phone number not valid")
    return phone


def validate_date(start_date, end_date):
    if start_date > end_date:
        raise ValueError("period not valid")
    return start_date, end_date
