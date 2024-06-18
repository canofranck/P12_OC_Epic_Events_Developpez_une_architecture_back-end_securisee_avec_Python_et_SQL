# from models.user import User, UserRole
# from views.main_view import MainView
# from views.user_view import UserView
# from controllers.user_controller import UserController

# from controllers.report_controller import ReportController
# from controllers.tournament_controller import TournamentController
import constantes
import logging
import models
import controllers
import views


# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


class MainController:
    """Contrôleur principal de l'application."""

    def __init__(self, session):
        self.session = session
        self.view = views.MainView()
        self.user_controller = controllers.UserController(
            session, view=views.UserView()
        )
        self.customer_controller = controllers.CustomerController(
            session=session, view=views.CustomerView()
        )
        self.user = None

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
            # self.main_view.clear_screen()
            choice = self.view.display_main_menu()

            if choice == constantes.MAIN_MENU_LOGIN:
                user = self.user_controller.run_login_menu()
                self.set_user_to_controllers(user)
                self.view.input_welcome_user(user)
                self.get_user_main_menu()
            elif choice == constantes.MAIN_MENU_QUIT:
                print("Au revoir !")
                break
            else:
                self.view.display_invalid_option_message()

    def create_admin(self):

        admin_user = (
            self.session.query(models.User).filter_by(username="Admin").first()
        )
        if not admin_user:

            admin = models.User(
                username="Admin",
                full_name="Admin User",
                email="admin@example.com",
                phone_number="1234567890",
                role=models.UserRole.MANAGER,
            )
            admin.set_password("adminoc")
            self.session.add(admin)
            self.session.commit()

    def set_user_to_controllers(self, user):
        self.user = user
        # self.customer_controller.collaborator = collaborator
        # self.deal_controller.collaborator = collaborator
        # self.event_controller.collaborator = collaborator

    def get_user_main_menu(self):
        running = True
        while running:
            menu_selection = self.user_controller.view.display_user_menu(
                self.user.role
            )
            print("retour display user menu , menu_selection=", menu_selection)
            if menu_selection == 0:
                break
            match self.user.role:
                case models.UserRole.MANAGER:
                    self.process_manager_action(menu_selection)
                case models.UserRole.SALES:
                    self.process_sales_action(menu_selection)
                case models.UserRole.SUPPORT:
                    self.process_support_action(menu_selection)
                case _:
                    print("error")
                    running = False
                    continue

    def process_manager_action(self, menu_selection):

        match menu_selection:
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case constantes.LIST_MANAGER_MANAGE_USER:
                print("j ai fait choix 5")
                self.user_controller.manage_user()

            case constantes.LIST_MANAGER_MANAGE_CONTRACT:
                print("j ai fait choix 6")
                self.user_controller.manage_contract()
            case _:
                print("input invalide")

    def process_sales_action(self, menu_selection):
        print("je suis dans le menu sales")
        match menu_selection:
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case constantes.LIST_SALES_CREATE_NEW_CUSTOMER:
                self.customer_controller.create_customer()
            case 5:
                pass
            case 6:
                pass
            case 7:
                pass
            case _:
                print("input invalide")

    def process_support_action(self, choice):
        pass
