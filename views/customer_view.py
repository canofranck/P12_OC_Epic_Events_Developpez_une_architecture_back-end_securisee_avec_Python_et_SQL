import models

import views
from rich.panel import Panel
from rich.table import Table


class CustomerView(views.BaseView):
    """
    The CustomerView class is responsible for managing the customer-related views in the application.

    Methods:
        input_first_name(self):
            Prompts the user to input the first name of a customer.

        input_last_name(self):
            Prompts the user to input the last name of a customer.

        input_email(self):
            Prompts the user to input the email address of a customer.

        input_phone_number(self):
            Prompts the user to input the phone number of a customer.

        input_compagny_name(self):
            Prompts the user to input the company name of a customer.

        input_customer_information(self):
            Prompts the user to input the first name, last name, and company name of a customer.

        display_new_customer_validation(self):
            Displays a success message indicating that a new customer has been created.

        display_customer_information(self, customer: models.Customer):
            Displays the information of a customer.

        input_update_customer(self):
            Prompts the user to input the updated information of a customer.

        display_update_customer_validation(self):
            Displays a success message indicating that a customer has been updated.
    """

    def input_first_name(self):
        """
        Prompts the user to input the first name of a customer.

        Returns:
            str: The first name of the customer.
        """
        self.console.print("First name : ", style="input")
        return input()

    def input_last_name(self):
        """
        Prompts the user to input the last name of a customer.

        Returns:
            str: The last name of the customer.
        """
        self.console.print("Last name : ", style="input")
        return input()

    def input_email(self):
        """
        Prompts the user to input the email address of a customer.

        Returns:
            str: The email address of the customer.
        """
        self.console.print("email customer : ", style="input")
        return input()

    def input_phone_number(self):
        """
        Prompts the user to input the phone number of a customer.

        Returns:
            str: The phone number of the customer.
        """
        self.console.print(
            "phone number: (must start with +33) : ", style="input"
        )

        return input()

    def input_compagny_name(self):
        """
        Prompts the user to input the company name of a customer.

        Returns:
            str: The company name of the customer.
        """
        self.console.print("Compagny name : ", style="input")

        return input()

    def input_customer_information(self):
        """
        Prompts the user to input the first name, last name, and company name of a customer.

        Returns:
            dict: A dictionary containing the first name, last name, and company name of the customer.
        """
        self.console.print(
            Panel("---   Customer Management   ---", expand=True),
            style="menu_text",
        )

        fist_name = self.input_first_name()
        last_name = self.input_last_name()
        compagny_name = self.input_compagny_name()

        return {
            "first_name": fist_name,
            "last_name": last_name,
            "compagny_name": compagny_name,
        }

    def display_new_customer_validation(self):
        """
        Displays a success message indicating that a new customer has been created.
        """
        self.console.print("[success]New customer correctly created[/]")
        self.wait_for_key_press()

    def display_customer_information(self, customers: models.Customer):
        """
        Displays the information of a customer.

        Args:
            customer (models.Customer): The customer object to display.
        """

        table = Table(title="Listing clients")
        table.add_column("First name", style="menu_choice")
        table.add_column("Last name", style="menu_choice")
        table.add_column("Phone number", style="menu_choice")
        table.add_column("Email", style="menu_choice")
        table.add_column("Company name", style="menu_choice")
        table.add_column("Commercial contact", style="menu_choice")
        table.add_column("Creation date", style="menu_choice")
        table.add_column("Last contact", style="menu_choice")
        try:
            iter(customers)
        except TypeError:
            # Si customers n'est pas itérable, considérez-le comme un seul objet
            customer = customers
            table.add_row(
                customer.first_name,
                customer.last_name,
                customer.phone_number,
                customer.email,
                customer.compagny_name,
                customer.user.full_name,
                str(customer.creation_date),
                str(customer.last_contact_date),
            )
            table.column_widths = "auto"
            self.console.print(table)

        else:
            # customers est itérable
            for customer in customers:
                table.add_row(
                    customer.first_name,
                    customer.last_name,
                    customer.phone_number,
                    customer.email,
                    customer.compagny_name,
                    customer.user.full_name,
                    str(customer.creation_date),
                    str(customer.last_contact_date),
                )
            table.column_widths = "auto"
            self.console.print(table)
            self.wait_for_key_press()

    def input_update_customer(self):
        """
        Prompts the user to input the updated information of a customer.

        Returns:
            dict: A dictionary containing the updated information of the customer.
        """
        self.console.print(
            Panel("--- Update Customer Management ---", expand=True),
            style="menu_text",
        )
        first_name = self.input_first_name()
        last_name = self.input_last_name()
        email = self.input_email()
        phone_number = self.input_phone_number()
        compagny_name = self.input_compagny_name()
        return {
            "first_name": first_name,
            "last_name": last_name,
            "compagny_name": compagny_name,
            "email": email,
            "phone": phone_number,
        }

    def display_update_customer_validation(self):
        """
        Displays a success message indicating that a customer has been updated.
        """
        self.console.print("Customer successfully updated", style="success")
        self.wait_for_key_press()

    def display_customer_not_found(self):
        """
        Displays a message indicating that a customer was not found.
        """
        self.console.print("Customer not found", style="error")

    def display_not_your_customer(self):
        """
        Displays a message indicating that a customer was not found.
        """
        self.console.print(
            "the customer is not assigned to you", style="error"
        )
        self.wait_for_key_press()

    def display_error(self, message):
        """
        Displays an error message.
        """
        self.console.print(f"[error] {message} [/]")
