import models

import validators
import views
from datetime import datetime


class CustomerController:
    def __init__(self, session, view: views.CustomerView, user=None):
        self.session = session
        self.view = view
        self.user = user

    def create_customer(self):
        email = self.set_new_customer_email()
        phone = self.set_customer_phone()
        new_customer_input = self.view.input_customer_information()
        new_customer = models.Customer(
            first_name=new_customer_input["first_name"],
            last_name=new_customer_input["last_name"],
            email=email,
            phone_number=phone,
            compagny_name=new_customer_input["compagny_name"],
            contact=self.user,
        )
        self.session.add(new_customer)
        try:
            self.session.commit()
            return self.view.display_new_customer_validation()
        except Exception as err:
            self.session.rollback()
            return self.view.display_error(err)

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
                self.view.display_error(err)
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
