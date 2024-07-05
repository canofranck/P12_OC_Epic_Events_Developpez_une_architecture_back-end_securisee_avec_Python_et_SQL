from controllers.main_controller import MainController
from database import init_db
import models
import models.user

import os
import themes
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
import logging


sentry_sdk.init(
    dsn=os.getenv("sentry_url"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

# configure the logging module to send messages only to Sentry
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Remove all existing handlers
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# Add a Sentry handler
sentry_handler = sentry_sdk.integrations.logging.EventHandler()
sentry_handler.setLevel(logging.DEBUG)
logger.addHandler(sentry_handler)

# Main program
if __name__ == "__main__":

    username = os.getenv("username")
    password = os.getenv("password")
    host = os.getenv("host")
    database_name = os.getenv("database_name")
    salt = os.getenv("salt")
    secret_key = os.getenv("secret_key")
    # Check if the salt is correctly loaded
    if not salt or not salt.startswith("$2b$"):
        raise ValueError("The salt is invalid or missing in the .env file")

    session = init_db()

    main_controller = MainController(
        session, salt, secret_key, console=themes.theme_console()
    )

    try:

        logger.debug("Starting admin creation and running the main controller")

        main_controller.create_admin()
        main_controller.run()
        logger.debug("Program stopped")
    except Exception as e:
        sentry_sdk.capture_exception(e)
        logger.error("An error occurred: %s", e)
    finally:
        sentry_sdk.flush()
        session.close()
