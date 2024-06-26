import models
import getpass
import views
import constantes
from rich.panel import Panel
from rich.rule import Rule


class UserView(views.BaseView):
    def input_email(self):
        self.console.print("Entrez votre email : ", style="input")
        return input()

    def input_password(self):
        self.console.print("Entrez votre mot de passe : ", style="input")
        return getpass.getpass()

    def display_user_menu(self, role_name):
        self.console.print(
            Panel(f" --- Menu {role_name} --- ", expand=True),
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
        return self.console.print(
            Panel("--- New user Management ---", expand=True),
            style="menu_text",
        )

    def input_new_user(self):
        username = self.input_username()
        full_name = self.input_full_name()
        role = self.input_user_role()
        return {" username": username, "full_name": full_name, "role": role}

    # def input_email(self):

    #     return input("email : ")

    # def input_password(self):

    #     return getpass.getpass("password : ")

    def input_user_role(self):
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
        self.console.print("Username : ", style="input")
        return input()

    def input_full_name(self):
        self.console.print("Full name : ", style="input")
        return input()

    def display_new_user_validation(self):
        self.console.print("[success]New user correctly created[/]")
        self.wait_for_key_press()

    def input_phone_number(self):
        self.console.print(
            "phone number: (must start with +33) : ", style="input"
        )
        return input()

    def input_update_user(self):
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
        self.console.print("[success]User successfully updated[/]")
        self.wait_for_key_press()

    def display_user_information(self, user):
        self.console.print("[menu_choice]User information : [/]")
        self.console.print(f"[menu_choice]Username : {user.username} [/]")
        self.console.print(f"[menu_choice]Fullname : {user.full_name} [/]")
        self.console.print(f"[menu_choice]Email : {user.email} [/]")
        self.console.print(
            f"[menu_choice]Phone number : {user.phone_number} [/]"
        )
        self.console.print(f"[menu_choice]Role : {user.role.name} [/]")

    def display_delete_user_validation(self):
        self.console.print("[success]User successfully deleted[/]")
        self.wait_for_key_press()

    def display_sales_menu(self):
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
        self.console.print(
            "[menu_choice]"
            + constantes.LIST_SUPPORT_CREATE_EVENT
            + " - Manage your Events [/]"
        )

    def display_admin_menu(self):
        self.console.print(
            "[menu_choice]"
            + constantes.ADMIN_CREATE_NEW_USER
            + " - Create user [/]"
        )

    def display_support_on_event(self):
        print("Enter Email support to assign : ")

    def login_menu(self):
        self.console.print(
            Panel("--- Login Menu ---", expand=True),
            style="menu_text",
        )

    def display_update_user(self):
        self.console.print(
            Panel("---   UPDATE USERS MENU   ---", expand=True),
            style="menu_text",
        )

    def display_delete_user(self):
        self.console.print(
            Panel("---   DELETE USER MENU   ---", expand=True),
            style="menu_text",
        )

    def display_token_expire(self):
        self.console.print("[error] Token expiré [/]")

    def display_token_invalide(self):
        self.console.print("[error] Token invalide [/]")
