from controllers.main_controller import MainController
from database import init_db, database_exists, create_database
import models
import models.user

# Programme principal
if __name__ == "__main__":
    session = init_db()
    if not database_exists():
        create_database()

    main_controller = MainController(session)
    main_controller.create_admin()

    main_controller.run()
    print("Arrêt du programme")
    session.close()
