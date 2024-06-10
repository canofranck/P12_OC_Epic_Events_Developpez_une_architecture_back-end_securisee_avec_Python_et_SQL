from controllers.main_controller import MainController
from database import init_db

# Programme principal
if __name__ == "__main__":

    init_db()  # Obtenir une session SQLAlchemy
    main_controller = MainController()

    print("Arrêt du programme")
