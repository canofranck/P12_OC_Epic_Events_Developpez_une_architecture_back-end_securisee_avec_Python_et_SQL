import models

import views
from rich.panel import Panel
from rich.table import Table


class CustomerView(views.BaseView):

    def input_first_name(self):
        self.console.print("First name : ", style="input")
        return input()

    def input_last_name(self):
        self.console.print("Last name : ", style="input")
        return input()

    def input_email(self):

        self.console.print("email customer : ", style="input")
        return input()

    def input_phone_number(self):
        self.console.print(
            "phone number: (must start with +33) : ", style="input"
        )

        return input()

    def input_compagny_name(self):
        self.console.print("Compagny name : ", style="input")

        return input()

    def input_customer_information(self):
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
        self.console.print("[success]New customer correctly created[/]")
        self.wait_for_key_press()

    def display_customer_information(self, customer: models.Customer):
        self.console.print(
            Panel("---   LIST CUSTOMERS   ---", expand=True),
            style="menu_text",
        )
        table = Table(
            title=f" Client: {customer.first_name} {customer.last_name}"
        )

        table.add_column("Champ", justify="left", style="cyan", no_wrap=True)
        table.add_column("Valeur", justify="left", style="cyan", no_wrap=True)

        table.add_row("Prénom", customer.first_name)
        table.add_row("Nom", customer.last_name)
        table.add_row("Téléphone", customer.phone_number)
        table.add_row("Email", customer.email)
        table.add_row("Nom de l'entreprise", customer.compagny_name)
        table.add_row("Contact commercial", customer.user.full_name)
        table.add_row("Date de création", str(customer.creation_date))
        table.add_row("Dernier contact", str(customer.last_contact_date))

        self.console.print(table)
        self.wait_for_key_press()

    def input_update_customer(self):
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
        print("Customer successfully updated", style="success")
        self.wait_for_key_press()
