import models
import getpass
import views
import constantes
from rich.panel import Panel
from rich.rule import Rule


class UserView(views.BaseView):
    """
    The UserView class is responsible for managing the user-related views in the application.

    Methods:
        input_email(self):
            Prompts the user to input their email address.

        input_password(self):
            Prompts the user to input their password.

        display_user_menu(self, role_name):
            Displays the user menu based on the user's role.

        display_management_menu(self):
            Displays the management menu options.

        input_user_management(self):
            Displays the user management menu options.

        display_new_user_panel(self):
            Displays a panel with the title "New user Management".

        input_new_user(self):
            Prompts the user to input the new user's information.

        input_user_role(self):
            Prompts the user to select the role for the new user.

        input_username(self):
            Prompts the user to input their username.

        input_full_name(self):
            Prompts the user to input their full name.

        display_new_user_validation(self):
            Displays a success message indicating that the new user was successfully created.

        input_phone_number(self):
            Prompts the user to input their phone number.

        input_update_user(self):
            Displays a panel with the title "Update user Management".

        display_update_user_validation(self):
            Displays a success message indicating that the user was successfully updated.

        display_user_information(self, user):
            Displays the user's information.

        display_delete_user_validation(self):
            Displays a success message indicating that the user was successfully deleted.

        display_sales_menu(self):
            Displays the sales menu options.

        display_support_menu(self):
            Displays the support menu options.

        display_admin_menu(self):
            Displays the admin menu options.

        display_support_on_event(self):
            Displays a message asking the user to enter the email of the support to assign to the event.

        login_menu(self):
            Displays the login menu.
        display_update_user(self):
            Displays the update user menu.

        display_delete_user(self):
            Displays the delete user menu.

        display_token_expire(self):
            Displays an error message indicating that the token is expired.

        display_token_invalide(self):
            Displays an error message indicating that the token is invalid.

    """

    def input_email(self):
        """
        Prompts the user to input their email address.

        Returns:
            str: The user's email address.
        """
        self.console.print("Entrez votre email : ", style="input")
        return input()

    def input_password(self):
        """
        Prompts the user to input their password.

        Returns:
            str: The user's password.
        """
        self.console.print("Entrez votre mot de passe : ", style="input")
        return getpass.getpass()

    def display_user_menu(self, role_name, user_name):
        """
        Displays the user menu based on the user's role.

        Args:
            role_name (str): The name of the user's role.
        """
        self.console.print(
            Panel(
                f" --- Menu {role_name}   --- {user_name} --- ", expand=True
            ),
            style="menu_text",
        )
        self.console.print(
            "[menu_choice]" + constantes.LOG_OUT + " - Logout [/] "
        )
        self.console.print(
            "[menu_choice]"
            + constantes.LIST_CUSTOMERS
            + " - List Customers [/]"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.LIST_CONTRACTS
            + " - List Contracts [/]"
        )
        self.console.print(
            "[menu_choice]" + constantes.LIST_EVENTS + " - List Events [/]"
        )
        match role_name:
            case constantes.ROLE_MANAGER:
                self.display_management_menu()
            case constantes.ROLE_SALES:
                self.display_sales_menu()
            case constantes.ROLE_SUPPORT:
                self.display_support_menu()
            case constantes.ROLE_ADMIN:
                self.display_admin_menu()
            case _:
                self.console.print("[error]Rôle non reconnu[/]")
        self.console.print("Choisissez une option : ", style="input")
        return input()

    def display_management_menu(self):
        """
        Displays the management menu options.
        """
        self.console.print(
            "[menu_choice]"
            + constantes.LIST_MANAGER_ASSIGN_EVENT
            + "- Assign a support to an event [/]",
        )
        self.console.print(
            "[menu_choice]"
            + constantes.LIST_MANAGER_MANAGE_USER
            + "- Manage users [/]"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.LIST_MANAGER_MANAGE_CONTRACT
            + "- Manage Contract [/]"
        )

    def input_user_management(self):
        """
        Displays the user management menu options.
        """
        self.console.print(
            Panel("--- MANAGE USERS MENU --- ", expand=True), style="menu_text"
        )

        self.console.print(
            "[menu_choice]" + constantes.LOG_OUT + " - Exit [/]"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.MANAGER_CREATE_NEW_USER
            + " - Create a new user [/]"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.MANAGER_UPDATE_USER
            + " - Update a user [/]"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.MANAGER_DELETE_USER
            + " - Delete a user [/]"
        )
        selection = -1
        while selection not in [
            constantes.MANAGER_CREATE_NEW_USER,
            constantes.MANAGER_UPDATE_USER,
            constantes.MANAGER_DELETE_USER,
        ]:
            self.console.print("Choisissez une option : ", style="input")
            selection = input()

        return selection

    def display_new_user_panel(self):
        """
        Displays a panel with the title "New user Management".
        """
        return self.console.print(
            Panel("--- New user Management ---", expand=True),
            style="menu_text",
        )

    def input_new_user(self):
        """
        Prompts the user to input the new user's information.

        Returns:
            dict: A dictionary containing the new user's information.
        """
        username = self.input_username()
        full_name = self.input_full_name()
        role = self.input_user_role()
        return {" username": username, "full_name": full_name, "role": role}

    def input_user_role(self):
        """
        Prompts the user to select the role for the new user.

        Returns:
            int: The selected role as an integer.
        """
        self.console.print(f"[menu_choice]1 - {constantes.ROLE_MANAGER} [/]")
        self.console.print(f"[menu_choice]2 - {constantes.ROLE_SALES} [/]")
        self.console.print(f"[menu_choice]3 - {constantes.ROLE_SUPPORT} [/]")

        role_selection = 0
        while role_selection <= 0 or role_selection > 3:
            try:
                self.console.print(
                    "Role of new User: (enter the digit value)", style="input"
                )
                role_selection = int(input())
                if role_selection > 3:
                    raise ValueError
            except ValueError:
                self.console.print("[error]input invalid[/]")
        return role_selection

    def input_username(self):
        """
        Prompts the user to input their username.

        Returns:
            str: The user's username.
        """
        self.console.print("Username : ", style="input")
        return input()

    def input_full_name(self):
        """
        Prompts the user to input their full name.

        Returns:
            str: The user's full name.
        """
        self.console.print("Full name : ", style="input")
        return input()

    def display_new_user_validation(self):
        """
        Displays a success message indicating that the new user was successfully created.
        """
        self.console.print("[success]New user correctly created[/]")
        self.wait_for_key_press()

    def display_new_user_error(self):
        """
        Displays an error message indicating that the new user was not created.
        """
        self.console.print("[error]New user not created[/]")

    def input_phone_number(self):
        """
        Prompts the user to input their phone number.

        Returns:
            str: The user's phone number.
        """
        self.console.print(
            "phone number: (must start with +33) : ", style="input"
        )
        return input()

    def input_update_user(self):
        """
        Displays a panel with the title "Update user Management".
        """
        self.console.print(
            Panel("---   Update user Management   ---", expand=True),
            style="menu_text",
        )
        username = self.input_username()
        full_name = self.input_full_name()
        email = self.input_email()
        phone_number = self.input_phone_number()
        role_id = self.input_user_role()
        return {
            "username": username,
            "full_name": full_name,
            "email": email,
            "phone_number": phone_number,
            "role_id": role_id,
        }

    def display_update_user_validation(self):
        """
        Displays a success message indicating that the user was successfully updated.
        """
        self.console.print("[success]User successfully updated[/]")
        self.wait_for_key_press()

    def display_user_information(self, user):
        """
        Displays the user's information.

        Args:
            user (User): The user object.
        """
        self.console.print("[menu_choice]User information : [/]")
        self.console.print(f"[menu_choice]Username : {user.username} [/]")
        self.console.print(f"[menu_choice]Fullname : {user.full_name} [/]")
        self.console.print(f"[menu_choice]Email : {user.email} [/]")
        self.console.print(
            f"[menu_choice]Phone number : {user.phone_number} [/]"
        )
        self.console.print(f"[menu_choice]Role : {user.role.name} [/]")

    def display_delete_user_validation(self):
        """
        Displays a success message indicating that the user was successfully deleted.
        """
        self.console.print("[success]User successfully deleted[/]")
        self.wait_for_key_press()

    def display_sales_menu(self):
        """
        Displays the sales menu options.
        """
        self.console.print(
            "[menu_choice]"
            + constantes.LIST_SALES_CREATE_NEW_CUSTOMER
            + " - Create a new Customer [/]"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.LIST_SALES_UPDATE_CUSTOMER
            + " - Update your Customer information [/]"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.LIST_SALES_UPDATE_CONTRACT
            + " - Update your Customer Contract [/]"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.LIST_SALES_CREATE_EVENT
            + " - Create an Event for a Customer [/]"
        )

    def display_support_menu(self):
        """
        Displays the support menu options.
        """
        self.console.print(
            "[menu_choice]"
            + constantes.LIST_SUPPORT_CREATE_EVENT
            + " - Manage your Events [/]"
        )

    def display_admin_menu(self):
        """
        Displays the admin menu options.
        """
        self.console.print(
            "[menu_choice]"
            + constantes.ADMIN_CREATE_NEW_USER
            + " - Create user [/]"
        )

    def display_support_on_event(self):
        """
        Displays a message asking the user to enter the email of the support to assign to the event.
        """
        self.console.print("Enter Email support to assign : ", style="input")

    def login_menu(self):
        """
        Displays the login menu.
        """
        self.console.print(
            Panel("--- Login Menu ---", expand=True),
            style="menu_text",
        )

    def display_update_user(self):
        """
        Displays the update user menu.
        """
        self.console.print(
            Panel("---   UPDATE USERS MENU   ---", expand=True),
            style="menu_text",
        )

    def display_delete_user(self):
        """
        Displays the delete user menu.
        """
        self.console.print(
            Panel("---   DELETE USER MENU   ---", expand=True),
            style="menu_text",
        )

    def display_token_expire(self):
        """
        Displays an error message indicating that the token is expired.
        """
        self.console.print("[error] Token expiré [/]")

    def display_token_invalide(self):
        """
        Displays an error message indicating that the token is invalid.
        """
        self.console.print("[error] Token invalide [/]")

    def display_error(self, message):
        """
        Displays an error message.
        """
        self.console.print(f"[error] {message} [/]")
