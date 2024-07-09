import models
import constantes
import validators
import views
from datetime import datetime
from rich.console import Console
from rich.table import Table
import logging

logger = logging.getLogger(__name__)


class CustomerController:
    """
    The CustomerController class is responsible for managing customers within the application.

    Attributes:
        session: The database session used for database operations.
        view: The view associated with customer operations.
        user: The currently logged-in user.

    Methods:
        __init__(self, session, view, user=None):
            Initializes the CustomerController with the given parameters.

        create_customer(self):
            Creates a new customer with the provided information.

        set_new_customer_email(self):
            Sets a new email for the customer after validating it.

        is_email_in_database(self, email):
            Checks if the provided email already exists in the database.

        set_customer_phone(self):
            Sets a new phone number for the customer.

        update_customer(self):
            Updates the customer information.

        get_customer(self, user: models.User = None):
            Retrieves the customer associated with the given user.

        list_customers(self):
            Lists all customers in the database.

    """

    def __init__(self, session, view: views.CustomerView, user=None):
        """
        Initializes the CustomerController with the given parameters.

        Args:
            session: The database session used for database operations.
            view: The view associated with customer operations.
            user: The currently logged-in user (default is None).
        """
        self.session = session
        self.view = view
        self.user = user

    def create_customer(self):
        """
        Creates a new customer with the provided information.

        This method prompts the user to input the details of the new customer,
        creates a new customer object, and saves it to the database. If an error
        occurs during the process, the transaction is rolled back and an error
        message is displayed.

        Returns:
            None
        """
        if self.user is None:
            self.view.display_error(constantes.CUSTOMER_CONTROLLER_NO_USER)

        new_customer_input = self.view.input_customer_information()
        new_customer = models.Customer(
            first_name=new_customer_input["first_name"],
            last_name=new_customer_input["last_name"],
            email=self.set_new_customer_email(),
            phone_number=self.set_customer_phone(),
            compagny_name=new_customer_input["compagny_name"],
            sales_id=self.user.id,
        )
        self.session.add(new_customer)
        try:
            self.session.commit()
            return self.view.display_new_customer_validation()
        except Exception as err:
            self.session.rollback()
            self.view.display_error(f"Error Exception : {err}")
            logger.info("Error Exception " + err)

    def set_new_customer_email(self):
        """
        Sets a new email address for the customer.

        This method prompts the user to input a valid email address,
        validates the email format, and checks if the email already exists
        in the database. If the email is valid and does not exist in the database,
        it is returned. Otherwise, an error message is displayed and the user
        is prompted to input the email again.

        Returns:
            str: The validated email address.
        """
        email = ""
        while email == "":
            try:
                email_input = self.view.input_email()
                validators.validate_email(email_input)
                self.is_email_in_database(email_input)
                email = email_input
                continue
            except ValueError as err:
                self.view.display_error(f"ValueError : {err}")
                logger.info("ValueError " + err)
                continue
        return email

    def is_email_in_database(self, email):
        """
        Checks if the given email address already exists in the database.

        This method queries the database to check if a user with the specified email address
        already exists. If the email address is found in the database, an exception is raised.

        Args:
            email (str): The email address to check.

        Raises:
            ValueError: If the email address already exists in the database.

        Returns:
            None
        """
        if (
            self.session.query(models.User).filter_by(email=email).first()
            is not None
        ):
            self.view.display_error(
                constantes.CUSTOMER_CONTROLLER_EMAIL_EXISTS
            )

    def set_customer_phone(self):
        """
        Sets a new phone number for the customer.

        This method prompts the user to input a valid phone number,
        validates the phone number format, and checks if the phone number already exists
        in the database. If the phone number is valid and does not exist in the database,
        it is returned. Otherwise, an error message is displayed and the user
        is prompted to input the phone number again.

        Returns:
            str: The validated phone number.
        """
        phone = ""
        while phone == "":
            try:
                phone_input = self.view.input_phone_number()
                validators.validate_phone(phone_input)
                phone = phone_input
                continue
            except ValueError as err:
                self.view.display_error(f"ValueError : {err}")
                logger.info("ValueError " + err)
                continue
        return phone

    def update_customer(self):
        """
        Updates the customer information.

        This method retrieves the customer associated with the currently logged-in user,
        displays the current customer information, and prompts the user to input new customer information.
        The customer's phone number, first name, last name, company name, and last contact date are updated
        with the new values provided by the user. The updated information is then committed to the database.

        Raises:
            ValueError: If an error occurs during the update process.

        Returns:
            None
        """
        try:
            customer = self.get_customer(self.user)
            if customer is not None:
                self.view.display_customer_information(customer)

                update_customer_input = self.view.input_customer_information()
                customer.phone_number = self.set_customer_phone()
                customer.first_name = update_customer_input["first_name"]
                customer.last_name = update_customer_input["last_name"]
                customer.compagny_name = update_customer_input["compagny_name"]
                customer.last_contact_date = datetime.now()
                self.session.commit()
                self.view.display_update_customer_validation()
        except ValueError as err:
            self.view.display_error(f"ValueError : {err}")
            logger.info("ValueError " + err)

    def get_customer(self, user: models.User = None):
        """
        Retrieves the customer associated with the given user.

        This method queries the database to find the customer that belongs to the specified user.
        If no customer is found, a ValueError is raised.

        Args:
            user (models.User, optional): The user whose customer is being retrieved. Defaults to None.

        Returns:
            models.Customer: The customer associated with the given user.

        Raises:
            ValueError: If no customer is found.
        """
        email = self.view.input_email()
        filters = {"email": email}
        if user is not None:
            filters["sales_id"] = user.id

        customer = (
            self.session.query(models.Customer).filter_by(**filters).first()
        )
        if customer is None:
            self.view.display_not_your_customer()

        return customer

    def list_customers(self):
        """
        Lists all customers in the database.

        This method retrieves all customers from the database and displays their information
        in a formatted table. If no customers are found, a message is displayed indicating
        that no customers were found.

        Returns:
            None
        """

        customers = self.session.query(models.Customer).all()
        if len(customers) == 0:
            return self.view.display_customer_not_found()

        self.view.display_customer_information(customers)
