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
            session, view=views.CustomerView()
        )
        self.contract_controller = controllers.ContractController(
            session=session, view=views.ContractView()
        )
        self.event_controller = controllers.EventController(
            session=session, view=views.EventView()
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
        self.customer_controller.user = user
        self.contract_controller.user = user
        self.event_controller.user = user

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
            case constantes.LIST_CUSTOMERS:
                self.customer_controller.list_customers()
            case constantes.LIST_CONTRACTS:
                self.contract_controller.list_contracts()
            case constantes.LIST_EVENTS:
                self.event_controller.list_events()
            case constantes.LIST_MANAGER_ASSIGN_EVENT:
                self.set_support_on_event()
            case constantes.LIST_MANAGER_MANAGE_USER:
                print("j ai fait choix 5")
                self.user_controller.manage_user()
                pass
            case constantes.LIST_MANAGER_MANAGE_CONTRACT:
                print("j ai fait choix 6")
                self.manage_contract()
            case _:
                print("input invalide")

    def process_sales_action(self, menu_selection):
        print("je suis dans le menu sales")
        match menu_selection:
            case constantes.LIST_CUSTOMERS:
                self.customer_controller.list_customers()
            case constantes.LIST_CONTRACTS:
                self.contract_controller.list_contracts()
            case constantes.LIST_EVENTS:
                self.event_controller.list_events()
            case constantes.LIST_SALES_CREATE_NEW_CUSTOMER:
                self.customer_controller.create_customer()
            case constantes.LIST_SALES_UPDATE_CUSTOMER:
                self.customer_controller.update_customer()
            case constantes.LIST_SALES_UPDATE_CONTRACT:
                self.update_customer_contract_sales()
            case constantes.LIST_SALES_CREATE_EVENT:
                self.create_event_sales()

            case _:
                print("input invalide")

    def process_support_action(self, menu_selection):
        match menu_selection:
            case 1:
                self.customer_controller.list_customers()
            case 2:
                self.contract_controller.list_contracts()
            case constantes.LIST_EVENTS:
                self.event_controller.list_events()
            case 4:
                pass
            case _:
                print("input invalide")

    def manage_contract(self):
        try:
            customer_to_manage = self.customer_controller.get_customer()
            return self.contract_controller.manage_contracts(
                customer_to_manage
            )
        except ValueError as err:
            print("error", err)

    def update_customer_contract_sales(self):
        try:
            customer_to_manage = self.customer_controller.get_customer(
                self.user
            )
            self.contract_controller.update_contract(customer_to_manage)
        except ValueError as err:
            print("error", err)

    def create_event_sales(self):
        try:
            customer_to_manage = self.customer_controller.get_customer(
                self.user
            )
            contract_to_manage = self.contract_controller.get_contract(
                customer_to_manage
            )
            return self.event_controller.create_event(
                customer_to_manage, contract_to_manage
            )
        except ValueError as err:
            print("error", err)

    def set_support_on_event(self):
        try:
            support_user = self.user_controller.get_user()
            if support_user.role != models.UserRole.SUPPORT:
                return print("NOT SUPPORT USER")

            return self.event_controller.update_event(
                support_user=support_user,
                assigned_support=None,
            )
        except ValueError as err:
            return print("error", err)
