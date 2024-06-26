from controllers.main_controller import MainController
from database import init_db
import models
import models.user
from dotenv import load_dotenv
import os
import themes

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
    main_controller.create_admin()

    main_controller.run()
    print("Arrêt du programme")
    session.close()
