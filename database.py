from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, registry
import configparser
import mysql.connector
from models.base import Base
from models.user import User, UserRole
from models.customers import Customer
from models.contract import Contract
from models.event import Event
import logging

# logging.basicConfig()
# logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

config = configparser.ConfigParser()
config.read("config.ini")

DATABASE_USERNAME = config.get("database", "username")
DATABASE_PASSWORD = config.get("database", "password")
DATABASE_HOST = config.get("database", "host")
DATABASE_NAME = config.get("database", "database_name")

DATABASE_URL = f"mysql+mysqlconnector://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"


def database_exists():
    connection = None  # Définir la variable connection en dehors du bloc try
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
    connection = None  # Définir la variable connection en dehors du bloc try
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


def init_db():
    if not database_exists():
        create_database()
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()
