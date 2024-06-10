from sqlalchemy import create_engine, exc, inspect
from sqlalchemy.orm import sessionmaker
import configparser
import mysql.connector
from models.base import Base
from models.user import User
from models.customers import Customer
from models.contract import Contract
from models.event import Event

import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

config = configparser.ConfigParser()
config.read("config.ini")

DATABASE_USERNAME = config.get("database", "username")
DATABASE_PASSWORD = config.get("database", "password")
DATABASE_HOST = config.get("database", "host")
DATABASE_NAME = config.get("database", "database_name")

DATABASE_URL = f"mysql+mysqlconnector://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}"


def create_database_if_not_exists():
    try:
        connection = mysql.connector.connect(
            host=DATABASE_HOST,
            user=DATABASE_USERNAME,
            password=DATABASE_PASSWORD,
        )
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print(f"Base de données '{DATABASE_NAME}' créée avec succès.")
    except mysql.connector.Error as e:
        print(f"Erreur lors de la création de la base de données : {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


# Initialiser la base de données
def init_db():
    # Crée la base de données si elle n'existe pas
    create_database_if_not_exists()

    # Connexion avec la base de données spécifiée
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal
