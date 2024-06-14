import bcrypt
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def create_hash_password(password: str) -> str:
    bytes_password = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(bytes_password, salt)
    return hash_password.decode("utf-8")


def is_password_correct(input_password, db_password):
    input_bytes = input_password.encode("utf-8")
    db_bytes = db_password.encode("utf-8")
    return bcrypt.checkpw(input_bytes, db_bytes)


def test_password_hashing():
    original_password = "adminoc"
    hashed_password = create_hash_password(original_password)
    logger.debug(f"Mot de passe original: {original_password}")
    logger.debug(f"Mot de passe haché: {hashed_password}")
    is_correct = is_password_correct(original_password, hashed_password)
    logger.debug(f"Le mot de passe est correct: {is_correct}")


if __name__ == "__main__":
    test_password_hashing()
