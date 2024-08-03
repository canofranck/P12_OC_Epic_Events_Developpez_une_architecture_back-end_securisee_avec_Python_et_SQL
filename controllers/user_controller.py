from controllers import main_controller
import models
import bcrypt
import constantes
import validators
import jwt
import os
from datetime import datetime, timedelta
import views
import logging

logger = logging.getLogger(__name__)


class UserController:
    """
    The UserController class is responsible for managing user-related operations within the application.

    Attributes:
        session: The database session used for database operations.
        view: The view associated with user operations.
        user: The currently logged-in user.

    Methods:
        __init__(self, session, view, user=None):
            Initializes the UserController with the given parameters.

        run_login_menu(self):
            Runs the login menu, allowing the user to log in with their email and password.

        manage_user(self):
            Manages user-related operations, such as creating, updating, and deleting users.

        create_user(self):
            Creates a new user in the system.

        set_new_user_email(self):
            Sets a new email for the user after validating it.

        is_email_in_database(self, email):
            Checks if the provided email already exists in the database.

        set_new_user_password(self):
            Sets a new password for the user after validating it.

        set_user_phone(self):
            Sets a new phone number for the user after validating it.

        update_user(self):
            Updates an existing user in the system.

        delete_user(self):
            Deletes an existing user from the system.

        get_user(self):
            Retrieves a user from the database based on their email.

        is_password_correct(self, input_password, user):
            Checks if the provided password is correct for the user.

        generate_token(self, user):
            Generates a JWT token for the user.

        save_token(self, token, email):
            Saves the JWT token for the user to a file.

        load_token(self, email):
            Loads the JWT token for the user from a file.

        is_token_valid(self, token):
            Checks if the provided JWT token is valid.

        get_user_from_token(self, token):
            Retrieves a user from the database based on their ID extracted from the JWT token.
    """

    def __init__(self, session, view, user=None):
        """
        Initializes the UserController with the given parameters.

        Args:
            session: The database session used for database operations.
            view: The view associated with user operations.
            user: The currently logged-in user (default is None).
        """
        self.session = session
        self.secret_key = os.getenv("secret_key")
        self.view = view
        self.user = user

    def run_login_menu(self):
        """
        Runs the login menu, allowing the user to log in with their email and password.

        This method displays the login menu and prompts the user to input their email and password.
        It checks if the user exists in the database and if the provided password is correct.
        If the login is successful, it returns the logged-in user.

        Returns:
            user: The logged-in user.
        """
        views.MainView.clear_screen(self)
        token = self.load_token()
        if token and self.is_token_valid(token):
            self.user = self.get_user_from_token(token)
            if self.user:
                return self.user
        self.view.login_menu()

        email_attempts = 0
        max_email_attempts = constantes.MAX_EMAIL_ATTEMPS
        while email_attempts < max_email_attempts:
            email = self.view.input_email()
            user = (
                self.session.query(models.User).filter_by(email=email).first()
            )
            if user is None:
                email_attempts += 1
                if email_attempts >= max_email_attempts:
                    self.view.display_error(
                        constantes.ERR_TOO_MANY_ATTEMPTS_EMAIL
                    )

                    break

                else:
                    self.view.display_error(constantes.ERR_USER_NOT_FOUND)

                    continue

            password_attempts = 0
            max_password_attempts = constantes.MAX_PASSWORD_ATTEMPS
            while password_attempts < max_password_attempts:
                password = self.view.input_password()
                if not user.is_password_correct(password):
                    password_attempts += 1
                    if password_attempts >= max_password_attempts:
                        self.view.display_error(
                            constantes.ERR_TOO_MANY_ATTEMPTS_PASSWORD
                        )
                        email_attempts = max_email_attempts

                        break

                    else:
                        self.view.display_error(
                            constantes.ERR_USER_BAD_PASSWORD
                        )

                        continue

                self.user = user
                self.save_token(self.generate_token(user))
                return user
        self.view.display_error(constantes.ERR_TOO_MANY_ATTEMPTS)
        raise ValueError(constantes.ERR_TOO_MANY_ATTEMPTS)

    def manage_user(self):
        """
        Manages user-related operations such as creating, updating, and deleting users.

        This method displays the user management menu and handles the user's selection.
        Depending on the user's choice, it either creates a new user, updates an existing user,
        deletes a user, or returns to the previous menu.

        Returns:
            None
        """
        selection_menu = self.view.input_user_management()

        match selection_menu:
            case constantes.MAIN_MENU_BACK:
                views.MainView.clear_screen(self)
                return
            case constantes.MANAGER_CREATE_NEW_USER:
                views.MainView.clear_screen(self)
                self.create_user()
            case constantes.MANAGER_UPDATE_USER:
                views.MainView.clear_screen(self)
                self.update_user()
            case constantes.MANAGER_DELETE_USER:
                views.MainView.clear_screen(self)
                self.delete_user()
            case constantes.MANAGER_LIST_USER:
                views.MainView.clear_screen(self)
                self.list_user()
            case _:
                self.view.display_error(constantes.MAIN_CONTROLLER_ERR_INPUT)

        return

    def create_user(self):
        """
        Creates a new user in the system.

        This method collects user information such as email, password, role, username, full name, and phone number.
        It then attempts to add the new user to the database and commit the transaction. If an error occurs during
        the process, the transaction is rolled back and an error message is displayed.

        Returns:
            None
        """

        self.view.display_new_user_panel()
        new_user = models.User(
            email=self.set_new_user_email(),
            password=self.set_new_user_password(),
            role_id=self.view.input_user_role(),
            username=self.view.input_username(),
            full_name=self.view.input_full_name(),
            phone_number=self.set_user_phone(),
        )
        try:
            self.session.add(new_user)
            self.session.commit()
            logger.info("Create User : " + new_user.full_name + "  success ")

            return self.view.display_new_user_validation()
        except Exception as err:
            logger.info(
                "Create User : " + new_user.full_name + " failed",
            )

            self.session.rollback()
            return self.view.display_new_user_error()

    def set_new_user_email(self):
        """
        Sets a new email for the user after validating it.

        This method prompts the user to input their email and validates it using the validate_email function.
        If the email is valid, it checks if it already exists in the database. If it does, an error message is displayed.
        If the email is valid and unique, it returns the email.

        Returns:
            email: The validated email.
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
                logger.info("ValueError : " + str(err))
                continue
        return email

    def is_email_in_database(self, email):
        """
        Checks if the provided email already exists in the database.

        This method queries the database to check if a user with the provided email exists.
        If the email is found, an error message is displayed.

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

    def set_new_user_password(self):
        """
        Sets a new password for the user after validating it.

        This method prompts the user to input their password and validates it using the validate_password function.
        If the password is valid, it returns the password.

        Returns:
            password: The validated password.
        """
        password = ""
        while password == "":
            try:
                password_input = self.view.input_password()
                validators.validate_password(password_input)
                password = password_input
                continue
            except ValueError as err:
                self.view.display_error(f"ValueError : {err}")
                logger.info("ValueError : " + str(err))
                continue
        return password

    def set_user_phone(self):
        """
        Sets a new phone number for the user after validating it.

        This method prompts the user to input their phone number and validates it using the validate_phone function.
        If the phone number is valid, it returns the phone number.

        Returns:
            phone_number: The validated phone number.
        """
        while True:
            try:
                phone_input = self.view.input_phone_number()
                validators.validate_phone(phone_input)
                return phone_input

            except ValueError as err:
                self.view.display_error(f"ValueError : {err}")
                logger.info("ValueError : " + str(err))

    def update_user(self):
        """
        Updates an existing user in the system.

        This method displays the update user menu and handles the user's selection.
        Depending on the user's choice, it either updates the user's information or returns to the previous menu.

        Returns:
            None
        """

        self.view.display_update_user()
        try:
            user = self.get_user()
            self.view.display_user_information(user)
            update_user_input = self.view.input_update_user()

            user.username = update_user_input["username"]
            user.full_name = update_user_input["full_name"]
            user.email = update_user_input["email"]
            user.phone_number = update_user_input["phone_number"]
            user.role_id = update_user_input["role_id"]
            self.session.commit()
            logger.info("Update user : " + user.full_name + " success")
            return self.view.display_update_user_validation()
        except ValueError as err:
            logger.info("Update user : " + user.full_name + " failed")
            self.view.display_error(f"Valuerror : {err}")

    def delete_user(self):
        """
        Deletes an existing user from the system.

        This method displays the delete user menu and handles the user's selection.
        Depending on the user's choice, it either deletes the user or returns to the previous menu.

        Returns:
            None
        """
        self.view.display_delete_user()
        try:
            user = self.get_user()
            self.session.delete(user)
            self.session.commit()
            self.view.display_delete_user_validation()
            if user:
                logger.info("Delete user : " + user.full_name + " success")
            return
        except ValueError:
            self.view.display_new_user_error()
            if user:
                logger.info("Delete user : " + user.full_name + " failed")
            return

    def get_user(self):
        """
        Retrieves a user from the database based on their email.

        This method prompts the user to input their email and queries the database to find the corresponding user.
        If the user is found, it returns the user. If the user is not found, an error message is displayed.

        Returns:
            user: The user found in the database.
        """
        email = self.view.input_email()
        user = self.session.query(models.User).filter_by(email=email).first()

        if user is None:
            self.view.display_error(constantes.ERR_USER_NOT_FOUND)
            return user == None
        return user

    def generate_token(self, user):
        """
        Generates a JWT token for the user.

        This method creates a payload with the user's ID and sets the token to expire in 1 hour.
        It then encodes the payload using the secret key and returns the token.

        Returns:
            token: The generated JWT token.
        """
        token_validity_period = constantes.TOKEN_VALIDITY_PERIOD

        payload = {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(hours=token_validity_period),
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def save_token(self, token):
        """
        Saves the JWT token for the user to a file.

        This method saves the JWT token for the user to a file named token.txt.
        It opens the file in write mode and writes the token to it.

        Returns:
            None
        """
        filename = f"token.txt"
        with open(filename, "w") as file:
            file.write(token)

    def load_token(self):
        """
        Loads the JWT token for the user from a file.

        This method loads the JWT token for the user from a file named token.txt.
        If the file exists, it reads the token from the file and returns it. Otherwise, it returns None.

        Returns:
            token: The loaded JWT token.
        """
        filename = f"token.txt"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                return file.read()
        return None

    def is_token_valid(self, token):
        """
        Checks if the provided JWT token is valid.

        This method attempts to decode the JWT token using the secret key and returns True if the token is valid.
        If the token is invalid, it returns False.

        Returns:
            is_valid: A boolean indicating whether the token is valid.
        """
        try:
            jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            self.view.display_token_expire()
        except jwt.InvalidTokenError:
            self.view.display_token_invalide()
        return False

    def get_user_from_token(self, token):
        """
        Retrieves a user from the database based on their ID extracted from the JWT token.

        This method attempts to decode the JWT token and extract the user's ID from the payload.
        It then queries the database to find the corresponding user and returns it.

        Returns:
            user: The user found in the database.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            user_id = payload["user_id"]
            return (
                self.session.query(models.User).filter_by(id=user_id).first()
            )
        except jwt.InvalidTokenError:
            return None

    def list_user(self):
        """
        Lists all users in the database.

        This method retrieves all users from the database and displays their information
        in a formatted table. If no users are found, a message is displayed indicating
        that no users were found.

        Returns:
            None
        """

        users = self.session.query(models.User).all()

        if len(users) == 0:
            return self.view.display_user_not_found()
        self.view.display_list_user(users)
