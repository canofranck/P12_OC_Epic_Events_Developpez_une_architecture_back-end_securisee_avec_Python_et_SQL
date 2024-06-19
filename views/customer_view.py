import models
import views


class CustomerView:

    def input_first_name(self):

        return input("First name : ")

    def input_last_name(self):

        return input("Last name : ")

    def input_email(self):

        return input("email customer : ")

    def input_phone_number(self):

        return input("phone number: (must start with +33) : ")

    def input_compagny_name(self):

        return input("Compagny name : ")

    def input_customer_information(self):
        print("---Customer Management ---")
        fist_name = self.input_first_name()
        last_name = self.input_last_name()
        compagny_name = self.input_compagny_name()

        return {
            "first_name": fist_name,
            "last_name": last_name,
            "compagny_name": compagny_name,
        }

    def display_new_customer_validation(self):
        print("New customer correctly created")

    def display_customer_information(self, customer: models.Customer):
        return print(
            f"First Name : {customer.first_name} \n"
            f"Last Name : {customer.last_name} \n"
            f"Phone : {customer.phone_number} \n"
            f"Email : {customer.email} \n"
            f"Compagny : {customer.compagny_name} \n"
            f"Contact : {customer.user.full_name} \n"
            f"Creation date : {customer.creation_date} \n"
            f"Last date contact: {customer.last_contact_date} \n"
            "--------------- \n"
        )

    def input_update_customer(self):
        print("--- Update Customer Management ---")
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
