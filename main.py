from controllers.main_controller import MainController
from database import init_db, database_exists, create_database

# Programme principal
if __name__ == "__main__":
    session = init_db()
    if not database_exists():
        create_database()

    main_controller = MainController(session)
    main_controller.create_admin()

    print("Arrêt du programme")
    session.close()
