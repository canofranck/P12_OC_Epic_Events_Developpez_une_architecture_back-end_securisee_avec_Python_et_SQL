import models

import views
import constantes


class UserView:
    def input_email(self):
        return input("Entrez votre email : ")

    def input_password(self):
        return input("Entrez votre mot de passe : ")

    def display_user_menu(self, role: models.UserRole):
        print(constantes.LOG_OUT, "- Logout")
        print(constantes.LIST_CUSTOMERS, "- List Customers")
        print(constantes.LIST_DEALS, "- List Contracts")
        print(constantes.LIST_EVENTS, "- List Events")
        match role:
            case models.UserRole.MANAGER:
                self.display_management_menu()
                pass
            case models.UserRole.SALES:
                self.display_sales_menu()
                pass
            case models.UserRole.SUPPORT:
                # self.display_support_menu()
                pass
            case models.UserRole.ADMIN:
                # self.display_admin_menu()
                pass

        return input(
            " je suis dans display user menu Choisissez une option : "
        )

    def display_management_menu(self):
        print(
            constantes.LIST_MANAGER_ASSIGN_EVENT,
            "- Assign a support to an event",
        )
        print(constantes.LIST_MANAGER_MANAGE_USER, "- Manage users")
        print(constantes.LIST_MANAGER_MANAGE_CONTRACT, "- Manage Contract")

    def input_user_management(self):
        print("0 - Exit")
        print("1 - Create a new user")
        print("2 - Update a user")
        print("3 - Delete a user")
        selection = -1
        while selection < 0 or selection > 3:
            try:

                selection = int(input("Select an action:"))
                if selection > 3 or selection < 0:
                    raise ValueError
            except ValueError:
                print("input invalide")
        return selection

    def display_new_user_panel(self):
        return print("--- New user Management ---")

    def input_new_user(self):
        username = self.input_username()
        full_name = self.input_full_name()
        role = self.input_user_role()
        return {" username": username, "full_name": full_name, "role": role}

    def input_email(self):

        return input("email : ")

    def input_password(self):

        return input("password : ")

    def input_user_role(self):
        print(f"1 - {models.UserRole.MANAGER}")
        print(f"2 - {models.UserRole.SALES}")
        print(f"3 - {models.UserRole.SUPPORT}")

        role_selection = 0
        while role_selection <= 0 or role_selection > 3:
            try:

                role_selection = int(
                    input("Role of new User: (enter the digit value)")
                )
                if role_selection > 3:
                    raise ValueError
            except ValueError:
                print("input invalid")
        match role_selection:
            case 1:
                return models.UserRole.MANAGER
            case 2:
                return models.UserRole.SALES
            case _:
                return models.UserRole.SUPPORT

    def input_username(self):

        return input("Username : ")

    def input_full_name(self):

        return input("Full name : ")

    def display_new_user_validation(self):
        print("New user correctly created")

    def input_phone_number(self):

        return input("phone number: (must start with +33) : ")

    def input_update_user(self):
        print("--- Update user Management ---")
        username = self.input_username()
        full_name = self.input_full_name()
        email = self.input_email()
        phone_number = self.input_phone_number()
        role = self.input_user_role()
        return {
            "username": username,
            "full_name": full_name,
            "email": email,
            "phone_number": phone_number,
            "role": role,
        }

    def display_update_user_validation(self):
        print("User successfully updated")

    def display_user_information(self, user):

        print(f"Username : {user.username} \n")
        print(f"Fullname : {user.full_name} \n")
        print(f"Email : {user.email} \n")
        print(f"Phone number : {user.phone_number} \n")
        print(f"Role : {user.role} \n")

    def display_delete_user_validation(self):
        print("User successfully deleted")

    def display_sales_menu(self):
        print(
            constantes.LIST_SALES_CREATE_NEW_CUSTOMER,
            " - Create a new Customer",
        )
        print(
            constantes.LIST_SALES_UPDATE_CUSTOMER,
            " - Update your Customer information",
        )
        print(
            constantes.LIST_SALES_UPDATE_CONTRACT,
            " - Update your Customer Deal",
        )
        print(
            constantes.LIST_MANAGER_ASSIGN_EVENT,
            " - Create an Event for a Customer",
        )
