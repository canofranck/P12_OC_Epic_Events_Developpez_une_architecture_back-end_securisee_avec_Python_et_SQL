# from models.user import User, UserRole
# from views.main_view import MainView
# from views.user_view import UserView
# from controllers.user_controller import UserController

# from controllers.report_controller import ReportController
# from controllers.tournament_controller import TournamentController
import constantes

# import logging
import models
import controllers
import views


# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


class MainController:
    """Contrôleur principal de l'application."""

    def __init__(self, session, salt, secret_key, console):
        self.session = session
        self.salt = salt
        self.secret_key = secret_key
        self.view = views.MainView(console)
        self.user_controller = controllers.UserController(
            session, salt, secret_key, view=views.UserView(console)
        )
        self.customer_controller = controllers.CustomerController(
            session, view=views.CustomerView(console)
        )
        self.contract_controller = controllers.ContractController(
            session=session, view=views.ContractView(console)
        )
        self.event_controller = controllers.EventController(
            session=session, view=views.EventView(console)
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
        self.view.clear_screen()
        while True:

            choice = self.view.display_main_menu()

            if choice == constantes.MAIN_MENU_LOGIN:
                user = self.user_controller.run_login_menu()
                self.set_user_to_controllers(user)
                self.view.clear_screen()
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
            manager_role = (
                self.session.query(models.Role)
                .filter_by(name="MANAGER")
                .first()
            )
            if not manager_role:
                raise ValueError(
                    "Role 'MANAGER' does not exist in the database."
                )
            admin = models.User(
                username="Admin",
                full_name="Admin User",
                email="admin@example.com",
                phone_number="1234567890",
                role_id=manager_role.id,
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
            role_name = self.user.role.name
            menu_selection = self.user_controller.view.display_user_menu(
                role_name
            )

            if menu_selection == 0:
                break
            match role_name:
                case constantes.ROLE_MANAGER:
                    self.process_manager_action(menu_selection)
                case constantes.ROLE_SALES:
                    self.process_sales_action(menu_selection)
                case constantes.ROLE_SUPPORT:
                    self.process_support_action(menu_selection)
                case constantes.ROLE_ADMIN:
                    self.process_admin_action(menu_selection)
                case _:
                    print("error")
                    running = False
                    continue

    def process_manager_action(self, menu_selection):

        match menu_selection:
            case constantes.LIST_CUSTOMERS:
                self.view.clear_screen()
                self.customer_controller.list_customers()
            case constantes.LIST_CONTRACTS:
                self.view.clear_screen()
                self.contract_controller.list_contracts()
            case constantes.LIST_EVENTS:
                self.view.clear_screen()
                self.event_controller.list_events()
            case constantes.LIST_MANAGER_ASSIGN_EVENT:
                self.view.clear_screen()
                self.set_support_on_event()
            case constantes.LIST_MANAGER_MANAGE_USER:
                self.view.clear_screen()
                self.user_controller.manage_user()
            case constantes.LIST_MANAGER_MANAGE_CONTRACT:
                self.view.clear_screen()
                self.manage_contract()
            case _:
                print("input invalide")

    def process_sales_action(self, menu_selection):

        match menu_selection:
            case constantes.LIST_CUSTOMERS:
                self.view.clear_screen()
                self.customer_controller.list_customers()
            case constantes.LIST_CONTRACTS:
                self.view.clear_screen()
                self.contract_controller.list_contracts()
            case constantes.LIST_EVENTS:
                self.view.clear_screen()
                self.event_controller.list_events()
            case constantes.LIST_SALES_CREATE_NEW_CUSTOMER:
                self.view.clear_screen()
                self.customer_controller.create_customer()
            case constantes.LIST_SALES_UPDATE_CUSTOMER:
                self.view.clear_screen()
                self.customer_controller.update_customer()
            case constantes.LIST_SALES_UPDATE_CONTRACT:
                self.view.clear_screen()
                self.update_customer_contract_sales()
            case constantes.LIST_SALES_CREATE_EVENT:
                self.view.clear_screen()
                self.create_event_sales()

            case _:
                print("input invalide")

    def process_support_action(self, menu_selection):
        match menu_selection:
            case constantes.LIST_CUSTOMERS:
                self.customer_controller.list_customers()
            case constantes.LIST_CONTRACTS:
                self.contract_controller.list_contracts()
            case constantes.LIST_EVENTS:
                self.event_controller.list_events()
            case constantes.SUPPORT_MANAGE_EVENT:
                self.event_controller.sales_manager_events(
                    support_user=None,
                    assigned_support=self.user,
                )
            case _:
                print("input invalide")

    def manage_contract(self):

        self.view.display_manage_contract()
        try:
            customer_to_manage = self.customer_controller.get_customer()
            return self.contract_controller.manage_contracts(
                customer_to_manage
            )
        except ValueError as err:
            print("error", err)

    def update_customer_contract_sales(self):
        self.view.display_update_contract()
        try:
            customer_to_manage = self.customer_controller.get_customer(
                self.user
            )
            self.contract_controller.update_contract(customer_to_manage)
        except ValueError as err:
            print("error", err)

    def create_event_sales(self):
        self.view.display_create_event()

        try:
            customer_to_manage = self.customer_controller.get_customer(
                self.user
            )
            contract_to_manage = self.contract_controller.get_contract(
                customer_to_manage
            )
            if not contract_to_manage:
                print("Aucun contrat trouvé pour ce client.")
                return
            return self.event_controller.create_event(
                customer_to_manage, contract_to_manage
            )
        except ValueError as err:
            print("error", err)

    def set_support_on_event(self):
        self.view.display_set_support_on_event()
        try:
            self.user_controller.view.display_support_on_event()
            support_user = self.user_controller.get_user()
            support_user_role = (
                self.session.query(models.Role)
                .filter_by(id=support_user.role_id)
                .first()
            )
            if support_user_role.name != constantes.ROLE_SUPPORT:
                return self.view.display_not_support_user()

            return self.event_controller.update_event(
                support_user=support_user,
                assigned_support=None,
            )
        except ValueError as err:
            return print("error", err)
