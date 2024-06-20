import models
import bcrypt


import constantes
import logging
import validators

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

salt = b"$2b$12$QhTfGmCB1FrbuySv8Op4IO"


class UserController:
    """Contrôleur pour la gestion des joueurs."""

    def __init__(self, session, view, user=None):
        self.session = session
        self.view = view
        self.user = user

    def run_login_menu(self):
        while True:
            email = self.view.input_email()

            user = (
                self.session.query(models.User).filter_by(email=email).first()
            )
            if user is None:
                print(constantes.ERR_USER_NOT_FOUND)
                continue
            while True:
                password = self.view.input_password()
                if not self.is_password_correct(password, user):
                    print("Bad password. Please try again.")
                    continue
                self.user = user
                return user

    def manage_user(self):
        selection_menu = self.view.input_user_management()
        print(
            "retour affichage de input user management selection=",
            selection_menu,
        )
        match selection_menu:
            case 0:
                return
            case constantes.MANAGER_CREATE_NEW_USER:
                print("choix 1 create user")
                self.create_user()
            case constantes.MANAGER_UPDATE_USER:
                self.update_user()
            case constantes.MANAGER_DELETE_USER:
                self.delete_user()
            case _:
                print("input invalide")
                self.create_user()
        return

    def create_user(self):
        self.view.display_new_user_panel()
        new_user = models.User(
            email=self.set_new_user_email(),
            password=self.set_new_user_password(),
            role=self.view.input_user_role(),
            username=self.view.input_username(),
            full_name=self.view.input_full_name(),
            phone_number=self.set_user_phone(),
        )
        try:
            self.session.add(new_user)
            self.session.commit()
            return self.view.display_new_user_validation()
        except Exception as err:
            self.session.rollback()
            return print("error", err)

    def set_new_user_email(self):
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
            print("email already exist")

    def set_new_user_password(self):
        password = ""
        while password == "":
            try:
                password_input = self.view.input_password()
                validators.validate_password(password_input)
                password = password_input
                continue
            except ValueError as err:
                self.view.display_error(err)
                continue
        return password

    def set_user_phone(self):
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

    def update_user(self):
        try:
            user = self.get_user()
            self.view.display_user_information(user)
            update_user_input = self.view.input_update_user()

            user.username = update_user_input["username"]
            user.full_name = update_user_input["full_name"]
            user.email = update_user_input["email"]
            user.phone_number = update_user_input["phone_number"]
            user.role = update_user_input["role"]
            self.session.commit()
            return self.view.display_update_user_validation()
        except ValueError as err:
            print("error", err)

    def delete_user(self):
        try:
            user = self.get_user()
            self.session.delete(user)
            self.session.commit()
            return self.view.display_delete_user_validation()
        except ValueError:
            return

    def get_user(self):
        email = self.view.input_email()
        user = self.session.query(models.User).filter_by(email=email).first()

        print("sql user", user)
        if user is None:
            print("user NOTFOUND")
        return user

    def is_password_correct(self, input_password, user):
        input_bytes = input_password.encode("utf-8")
        hash_input_password = bcrypt.hashpw(input_bytes, salt)
        # logger.debug(f"h input password: {input_bytes}")
        # logger.debug(f"Mot de passe bd: {user.password}")
        # logger.debug(f"Mot de passe user crypt : {hash_input_password}")
        is_correct = hash_input_password == user.password.encode("utf-8")

        # logger.debug(f"Le mot de passe saisi est correct: {is_correct}")
        return is_correct
