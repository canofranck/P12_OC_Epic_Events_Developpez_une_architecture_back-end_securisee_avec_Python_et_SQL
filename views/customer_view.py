import models

import views
from rich.panel import Panel


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
        return self.console.print(
            f"[menu_text]First Name :[/] {customer.first_name} \n"
            f"[menu_text]Last Name :[/] {customer.last_name} \n"
            f"[menu_text]Phone :[/] {customer.phone_number} \n"
            f"[menu_text]Email :[/] {customer.email} \n"
            f"[menu_text]Compagny :[/] {customer.compagny_name} \n"
            f"[menu_text]Contact :[/] {customer.user.full_name} \n"
            f"[menu_text]Creation date :[/] {customer.creation_date} \n"
            f"[menu_text]Last date contact: [/] {customer.last_contact_date} \n"
        )

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
