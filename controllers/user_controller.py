import models
import bcrypt
import constantes

# import logging
import validators
import jwt
import os
from datetime import datetime, timedelta

import views

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)


class UserController:
    """Contrôleur pour la gestion des joueurs."""

    def __init__(self, session, salt, secret_key, view, user=None):
        self.session = session
        self.salt = salt
        self.secret_key = secret_key
        self.view = view
        self.user = user

    def run_login_menu(self):
        views.MainView.clear_screen(self)
        self.view.login_menu()
        email = self.view.input_email()
        token = self.load_token(email)
        if token and self.is_token_valid(token):
            self.user = self.get_user_from_token(token)
            return self.user

        user = self.session.query(models.User).filter_by(email=email).first()
        if user is None:
            print(constantes.ERR_USER_NOT_FOUND)
            return

        while True:
            password = self.view.input_password()
            if not self.is_password_correct(password, user):
                print("Bad password. Please try again.")
                continue
            self.user = user
            self.save_token(self.generate_token(user), email)
            return user

    def manage_user(self):
        selection_menu = self.view.input_user_management()

        match selection_menu:
            case 0:
                return
            case constantes.MANAGER_CREATE_NEW_USER:
                views.MainView.clear_screen(self)
                self.create_user()
            case constantes.MANAGER_UPDATE_USER:
                views.MainView.clear_screen(self)
                self.update_user()
            case constantes.MANAGER_DELETE_USER:
                views.MainView.clear_screen(self)
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
            role_id=self.view.input_user_role(),
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

        while True:
            try:
                phone_input = self.view.input_phone_number()
                validators.validate_phone(phone_input)
                return phone_input

            except ValueError as err:
                print("error", err)

    def update_user(self):
        self.view.display_update_user()
        try:
            user = self.get_user()
            self.view.display_user_information(user)
            update_user_input = self.view.input_update_user()

            user.username = update_user_input["username"]
            user.full_name = update_user_input["full_name"]
            user.email = update_user_input["email"]
            user.phone_number = update_user_input["phone_number"]
            user.role_id = update_user_input["role_id"]
            self.session.commit()
            return self.view.display_update_user_validation()
        except ValueError as err:
            print("error", err)

    def delete_user(self):
        self.view.display_delete_user()
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
        # print("salt : ", self.salt)
        input_bytes = input_password.encode("utf-8")
        hash_input_password = bcrypt.hashpw(
            input_bytes, self.salt.encode("utf-8")
        )
        # logger.debug(f"h input password: {input_bytes}")
        # logger.debug(f"Mot de passe bd: {user.password}")
        # logger.debug(f"Mot de passe user crypt : {hash_input_password}")
        is_correct = hash_input_password == user.password.encode("utf-8")

        # logger.debug(f"Le mot de passe saisi est correct: {is_correct}")
        return is_correct

    def generate_token(self, user):
        payload = {
            "user_id": user.id,
            "exp": datetime.utcnow()
            + timedelta(hours=1),  # Token valide pour 1 heure
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def save_token(self, token, email):
        filename = f"token_{email}.txt"
        with open(filename, "w") as file:
            file.write(token)

    def load_token(self, email):
        filename = f"token_{email}.txt"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                return file.read()
        return None

    def is_token_valid(self, token):
        try:
            jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return True
        except jwt.ExpiredSignatureError:
            self.view.display_token_expire()
        except jwt.InvalidTokenError:
            self.view.display_token_invalide()
        return False

    def get_user_from_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            user_id = payload["user_id"]
            return (
                self.session.query(models.User).filter_by(id=user_id).first()
            )
        except jwt.InvalidTokenError:
            return None
