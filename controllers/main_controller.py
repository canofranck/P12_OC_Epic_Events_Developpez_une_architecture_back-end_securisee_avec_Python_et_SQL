import os
import constantes
import logging
import models
import controllers
import views
import sentry_sdk
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()


class MainController:
    """
    MainController is the central controller for the application.
    It initializes various controllers and views, and manages the main flow of the application.

    Attributes:
        session: The database session used for database operations.
        salt: The salt used for hashing passwords.
        secret_key: The secret key used for encoding and decoding JWT tokens.
        view: The main view of the application.
        user_controller: The controller responsible for user-related operations.
        customer_controller: The controller responsible for customer-related operations.
        contract_controller: The controller responsible for contract-related operations.
        event_controller: The controller responsible for event-related operations.
        user: The currently logged-in user.

    Methods:
        __init__(self, session, salt, secret_key, console):
            Initializes the MainController with the given parameters.

        run(self):
            Runs the main loop of the application, displaying the main menu and handling user input.

        create_admin(self):
            Creates an admin user if it does not already exist.

        set_user_to_controllers(self, user):
            Sets the user for the main controller and its associated controllers.

        get_user_main_menu(self):
            Displays the main menu for the logged-in user and processes their selection.
    """

    def __init__(self, session, salt, secret_key, console):
        """
        Initializes the MainController with the given parameters.

        Args:
            session: The database session used for database operations.
            salt: The salt used for hashing passwords.
            secret_key: The secret key used for encoding and decoding JWT tokens.
            console: The console object used for displaying views.

        Attributes:
            session: The database session used for database operations.
            salt: The salt used for hashing passwords.
            secret_key: The secret key used for encoding and decoding JWT tokens.
            view: The main view of the application.
            user_controller: The controller responsible for user-related operations.
            customer_controller: The controller responsible for customer-related operations.
            contract_controller: The controller responsible for contract-related operations.
            event_controller: The controller responsible for event-related operations.
            user: The currently logged-in user.
        """
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
        """
        Runs the main loop of the application, displaying the main menu and handling user input.

        The method continuously displays the main menu and waits for the user to select an option.
        Depending on the user's choice, it either initiates the login process, quits the application,
        or displays an invalid option message. If an error occurs during the execution, it captures
        the exception and logs the error.

        Raises:
            Exception: If an error occurs during the execution of the main loop.
        """

        self.view.clear_screen()
        while True:
            try:
                choice = self.view.display_main_menu()

                if choice == constantes.MAIN_MENU_LOGIN:
                    user = self.user_controller.run_login_menu()
                    self.set_user_to_controllers(user)
                    self.view.clear_screen()
                    self.view.input_welcome_user(user)
                    self.get_user_main_menu()

                elif choice == constantes.MAIN_MENU_QUIT:
                    self.view.display_error(
                        constantes.MAIN_CONTROLLER_ERR_QUIT
                    )
                    break
                else:
                    self.view.display_invalid_option_message()

            except Exception as e:
                sentry_sdk.capture_exception(e)
                self.view.display_error(
                    f"Une erreur est survenue. Veuillez consulter les logs pour plus de détails. {e}"
                )
                logger.info("Error exception : " + str(e))

    def create_admin(self):
        """
        Creates an admin user if it does not already exist.

        This method checks if an admin user with the username "Admin" exists in the database.
        If not, it creates a new admin user with the role "MANAGER" and default credentials.
        """
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

            admin_first_name = os.getenv("ADMIN_FIRST_NAME")
            admin_last_name = os.getenv("ADMIN_LAST_NAME")
            admin_email = os.getenv("ADMIN_EMAIL")
            admin_phone = os.getenv("ADMIN_PHONE")
            admin_password = os.getenv("ADMIN_PASSWORD")
            admin = models.User(
                username=admin_first_name,
                full_name=admin_last_name,
                email=admin_email,
                phone_number=admin_phone,
                role_id=manager_role.id,
            )
            admin.set_password(admin_password)
            self.session.add(admin)
            self.session.commit()

    def set_user_to_controllers(self, user):
        """
        Sets the user for the main controller and its associated controllers.

        This method assigns the given user to the main controller as well as to the
        customer_controller, contract_controller, and event_controller.

        Args:
            user (models.User): The user to be set for the controllers.
        """
        self.user = user
        self.customer_controller.user = user
        self.contract_controller.user = user
        self.event_controller.user = user

    def get_user_main_menu(self):
        """
        Displays the main menu for the logged-in user and processes their selection.

        This method retrieves the role of the currently logged-in user and displays the
        appropriate menu options based on their role. It then processes the user's menu
        selection and performs the corresponding actions.

        The method continues to display the menu and process selections until the user
        chooses to log out or an invalid input is encountered.

        Returns:
            None
        """

        running = True
        while running:
            role_name = self.user.role.name
            user_name = self.user.username
            menu_selection = self.user_controller.view.display_user_menu(
                role_name, user_name
            )

            if menu_selection == "0":
                self.logout()
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
                    self.view.display_error(
                        constantes.MAIN_CONTROLLER_ERR_INPUT
                    )
                    running = False
                    continue

    def process_manager_action(self, menu_selection):
        """
        Process the menu selection for a manager.

        This method processes the menu selection made by a manager and performs the
        corresponding action. It handles various options such as listing customers,
        contracts, events, assigning support to an event, managing users, and managing
        contracts.

        Args:
            menu_selection (str): The menu option selected by the manager.

        Returns:
            None
        """

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
                self.view.display_error(constantes.MAIN_CONTROLLER_ERR_INPUT)

    def process_sales_action(self, menu_selection):
        """
        Process the menu selection for a sales representative.

        This method processes the menu selection made by a sales representative and performs the
        corresponding action. It handles various options such as listing customers, contracts, events,
        creating and updating customers, updating contracts, and creating events.

        Args:
            menu_selection (str): The menu option selected by the sales representative.

        Returns:
            None
        """

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
                self.view.display_error(constantes.MAIN_CONTROLLER_ERR_INPUT)

    def process_support_action(self, menu_selection):
        """
        Process the menu selection for a support representative.

        This method processes the menu selection made by a support representative and performs the
        corresponding action. It handles various options such as listing customers, contracts, events,
        and managing events.

        Args:
            menu_selection (str): The menu option selected by the support representative.

        Returns:
            None
        """
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
                self.view.display_error(constantes.MAIN_CONTROLLER_ERR_INPUT)

    def manage_contract(self):
        """
        Manage contracts for a customer.

        This method displays the contract management interface and allows the user to manage contracts
        for a selected customer. It handles the process of selecting a customer and then managing their
        contracts.

        Returns:
            None
        """

        self.view.display_manage_contract()
        try:
            customer_to_manage = self.customer_controller.get_customer()
            return self.contract_controller.manage_contracts(
                customer_to_manage
            )
        except ValueError as err:
            self.view.display_error(f"error : {err}")
            logger.info("ValueError : " + str(err))

    def update_customer_contract_sales(self):
        """
        Update the sales information for a customer's contract.

        This method displays the interface for updating the sales information of a customer's contract.
        It handles the process of selecting a customer and then updating their contract with the new
        sales information.

        Returns:
            None
        """
        self.view.display_update_contract()
        try:
            customer_to_manage = self.customer_controller.get_customer(
                self.user
            )
            self.contract_controller.update_contract(customer_to_manage)
        except ValueError as err:
            self.view.display_error(f"error : {err}")
            logger.info("ValueError : " + str(err))

    def create_event_sales(self):
        """
        Create a new event for a customer's contract.

        This method displays the interface for creating a new event for a customer's contract.
        It handles the process of selecting a customer and their contract, and then creating
        a new event associated with that contract.

        Returns:
            None
        """
        self.view.display_create_event()

        try:
            customer_to_manage = self.customer_controller.get_customer(
                self.user
            )
            contract_to_manage = self.contract_controller.get_contract(
                customer_to_manage
            )
            if not contract_to_manage:

                return
            return self.event_controller.create_event(
                customer_to_manage, contract_to_manage
            )
        except ValueError as err:
            self.view.display_error(f"error : {err}")
            logger.info("ValueError : " + str(err))

    def set_support_on_event(self):
        """
        Set support user on an event.

        This method displays the interface for setting a support user on an event.
        It handles the process of selecting a support user and assigning them to an event.

        Returns:
            None
        """
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
            self.view.display_error(f"error : {err}")
            logger.info("ValueError : " + str(err))
            return

    def logout(self):
        """
        Logout the current user.

        This method handles the process of logging out the current user. It asks the user if they want to keep the token on the PC or delete it.
        If the user chooses to keep the token, the program will flush Sentry and exit.
        If the user chooses to delete the token, the token file will be removed, the session will be cleared, and the program will exit.

        Returns:
            None
        """

        choice = self.view.display_logout()
        if choice == "y":
            sentry_sdk.flush()
            exit()
        # delete token

        filename = f"token.txt"
        if os.path.exists(filename):
            os.remove(filename)
        # clear session
        self.session.close()
        self.user = None
        self.user_controller.user = None
        self.customer_controller.user = None
        self.contract_controller.user = None
        self.event_controller.user = None
        # exit
        sentry_sdk.flush()
        exit()
