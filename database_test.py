from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry
import configparser
import mysql.connector
from models.base import Base
from models.role import Role
from models.user import User
from models.customers import Customer
from models.contract import Contract
from models.event import Event
from dotenv import load_dotenv
import os

DATABASE_USERNAME = "root"
DATABASE_PASSWORD = "Password2325"
DATABASE_HOST = "localhost"
DATABASE_NAME = "p12_testrole2_test"
salt = "$2b$12$QhTfGmCB1FrbuySv8Op4IO"
secret_key = "#zfhtz-4bpoqens*3jx9p9=hhz(67x#4atd5^5id%kh32kqkb2"

print(
    f"Initialisation de la base de données avec : {DATABASE_USERNAME}, {DATABASE_PASSWORD}, {DATABASE_HOST}, {DATABASE_NAME}"
)

DATABASE_URL = f"mysql+mysqlconnector://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"


def database_exists():
    """
    Checks if the database exists.

    Returns:
        bool: True if the database exists, False otherwise.
    """
    connection = None
    print(
        f"Initialisation de la base de données avec : {DATABASE_USERNAME}, {DATABASE_PASSWORD}, {DATABASE_HOST}, {DATABASE_NAME}"
    )
    try:
        connection = mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USERNAME,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME,
        )
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE()")
        result = cursor.fetchone()
        return result is not None
    except mysql.connector.Error as e:
        return False
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def create_database():
    """
    Creates the database.

    This function connects to the MySQL server and creates a new database with the name specified
    in the DATABASE_NAME variable. If the database already exists, it does nothing.
    """
    print(" baseeeeeeeeeeeeeeeeeeeeeeee", DATABASE_HOST, DATABASE_NAME)
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USERNAME,
            password=DATABASE_PASSWORD,
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")
        print(f"Base de données '{DATABASE_NAME}' créée avec succès.")
    except mysql.connector.Error as e:
        print(f"Erreur lors de la création de la base de données : {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


def init_db_test():
    """
    Initializes the database.

    This function checks if the database exists, and if not, creates it.
    It then creates all the tables defined in the SQLAlchemy models and initializes
    the default roles in the database.

    Returns:
        SessionLocal: The SQLAlchemy session factory.
    """
    if not database_exists():
        create_database()
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Initialize default roles after creating the tables
    session = SessionLocal()
    roles = ["MANAGER", "SALES", "SUPPORT", "ADMIN"]
    for role_name in roles:
        existing_role = session.query(Role).filter_by(name=role_name).first()
        if not existing_role:
            role = Role(name=role_name)
            session.add(role)

    try:
        session.commit()
        print("Rôles added successfully to the database.")
    except Exception as e:
        session.rollback()
        print(f"Error adding roles to the database: {e}")
    finally:
        session.close()

    return SessionLocal()
