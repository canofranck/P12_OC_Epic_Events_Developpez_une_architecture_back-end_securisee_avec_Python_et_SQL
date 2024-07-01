from controllers.main_controller import MainController
from database import init_db
import models
import models.user
from dotenv import load_dotenv
import os
import themes
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import logging

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


sentry_sdk.init(
    dsn="https://f82f0e8920fd9ef37b7199c8313f6262@o4507525543821312.ingest.de.sentry.io/4507526680150096",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

# Configurer le module logging pour envoyer les messages uniquement à Sentry
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Supprimer tous les gestionnaires existants
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Ajouter un gestionnaire de Sentry
sentry_handler = sentry_sdk.integrations.logging.EventHandler()
sentry_handler.setLevel(logging.DEBUG)
logger.addHandler(sentry_handler)
# Programme principal
if __name__ == "__main__":
    load_dotenv()
    username = os.getenv("username")
    password = os.getenv("password")
    host = os.getenv("host")
    database_name = os.getenv("database_name")
    salt = os.getenv("salt")
    secret_key = os.getenv("secret_key")
    # Vérifiez si le sel est correctement chargé
    if not salt or not salt.startswith("$2b$"):
        raise ValueError(
            "Le sel est invalide ou manquant dans le fichier .env"
        )

    session = init_db()

    main_controller = MainController(
        session, salt, secret_key, console=themes.theme_console()
    )

    try:

        logger.debug("Debut creation admin et run main controller")

        main_controller.create_admin()
        main_controller.run()
        logger.debug("Arrêt du programme")
    except Exception as e:
        sentry_sdk.capture_exception(e)
        logger.error("Une erreur est survenue : %s", e)
    finally:
        sentry_sdk.flush()
        session.close()
