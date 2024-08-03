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
from constantes import ROLES
import os

DATABASE_USERNAME = os.getenv("username")
DATABASE_PASSWORD = os.getenv("password")
DATABASE_HOST = os.getenv("host")
DATABASE_NAME = os.getenv("database_name")
DATABASE_PORT = os.getenv("port")
DATABASE_URL = f"mysql+mysqlconnector://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"


def database_exists():
    """
    Checks if the database exists.

    Returns:
        bool: True if the database exists, False otherwise.
    """

    connection = None
    try:
        connection = mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USERNAME,
            password=DATABASE_PASSWORD,
            database=DATABASE_NAME,
            port=DATABASE_PORT,
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

    connection = None
    try:
        connection = mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USERNAME,
            password=DATABASE_PASSWORD,
            port=DATABASE_PORT,
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


def init_db():
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

    for role_name in ROLES:
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
