import models

import validators
import views
from datetime import datetime
from rich.console import Console
from rich.table import Table


class CustomerController:
    def __init__(self, session, view: views.CustomerView, user=None):
        self.session = session
        self.view = view
        self.user = user

    def create_customer(self):
        if self.user is None:
            print("No user is currently logged in.")

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
            print("error", err)

    def set_new_customer_email(self):
        email = ""
        while email == "":
            try:
                email_input = self.view.input_email()
                validators.validate_email(email_input)
                self.is_email_in_database(email_input)
                email = email_input
                continue
            except ValueError as err:
                print("error", err)
                continue
        return email

    def is_email_in_database(self, email):
        if (
            self.session.query(models.User).filter_by(email=email).first()
            is not None
        ):
            raise print("EMAIL ALREADY EXISTS")

    def set_customer_phone(self):
        phone = ""
        while phone == "":
            try:
                phone_input = self.view.input_phone_number()
                validators.validate_phone(phone_input)
                phone = phone_input
                continue
            except ValueError as err:
                print("error", err)
                continue
        return phone

    def update_customer(self):
        try:
            customer = self.get_customer(self.user)
            self.view.display_customer_information(customer)

            update_customer_input = self.view.input_customer_information()
            customer.phone_number = self.set_customer_phone()
            customer.first_name = update_customer_input["first_name"]
            customer.last_name = update_customer_input["last_name"]
            customer.compagny_name = update_customer_input["compagny_name"]
            customer.last_contact_date = datetime.now()
            self.session.commit()
        except ValueError as err:
            print("error", err)

    def get_customer(self, user: models.User = None):
        email = self.view.input_email()
        filters = {"email": email}
        if user is not None:
            filters["sales_id"] = user.id

        customer = (
            self.session.query(models.Customer).filter_by(**filters).first()
        )
        if customer is None:
            raise ValueError("CUSTOMER_NOT_FOUND")
        return customer

    def list_customers(self):

        customers = self.session.query(models.Customer).all()
        if len(customers) == 0:
            return print(" Customer not found")

        table = Table(title="Liste des Clients")
        table.add_column("Prénom", justify="left", style="input", no_wrap=True)
        table.add_column("Nom", justify="left", style="input", no_wrap=True)
        table.add_column("Email", justify="left", style="input", no_wrap=True)
        table.add_column(
            "Téléphone", justify="left", style="input", no_wrap=True
        )
        table.add_column(
            "Nom de l'entreprise", justify="left", style="input", no_wrap=True
        )
        table.add_column(
            "ID de vente", justify="left", style="input", no_wrap=True
        )

        for customer in customers:
            table.add_row(
                customer.first_name,
                customer.last_name,
                customer.email,
                customer.phone_number,
                customer.compagny_name,
                str(customer.sales_id),
            )
        for customer in customers:
            self.view.display_customer_information(customer)
