from models.user import User, UserRole, create_hash_password
from views.main_view import MainView

from controllers.user_controller import UserController

# from controllers.report_controller import ReportController
# from controllers.tournament_controller import TournamentController
import constantes


class MainController:
    """Contrôleur principal de l'application."""

    def __init__(self, session):
        self.session = session

        # self.user_controller = UserController()

    def run(self):
        """Lance l'application principale.
        Cette méthode démarre l'application et affiche le menu principal.
        En fonction du choix de l'utilisateur, elle dirige vers d'autres
        fonctionnalités telles que le menu des joueurs, le menu des tournois,
        le menu de rapports ou termine l'application.
        Args:
            Aucun argument requis.
        Returns:
            Aucune valeur de retour.
        Raises:
            Aucune exception n'est levée.
        """

        while True:
            self.main_view.clear_screen()
            choice = self.main_view.display_main_menu()

            if choice == constantes.MAIN_MENU_LOGIN:
                self.user_controller.run_login_menu()
            elif choice == constantes.MAIN_MENU_QUIT:
                print("Au revoir !")
                break
            else:
                self.main_view.display_invalid_option_message()

    def create_admin(self):
        # Vérifier si l'utilisateur Admin existe déjà
        print("je suis dans CREATE ADMINNNNNNNNNNNNNNNNNNNNN")
        admin_user = (
            self.session.query(User).filter_by(username="Admin").first()
        )
        if admin_user:
            print("L'utilisateur Admin existe déjà.")
            return

        # Créer l'utilisateur Admin avec le rôle MANAGER
        admin = User(
            username="Admin",
            password=create_hash_password("adminoc"),
            full_name="Admin User",
            email="admin@example.com",
            phone_number="1234567890",
            role=UserRole.MANAGER,
        )

        self.session.add(admin)
        self.session.commit()
        print("Utilisateur Admin créé avec succès.")
