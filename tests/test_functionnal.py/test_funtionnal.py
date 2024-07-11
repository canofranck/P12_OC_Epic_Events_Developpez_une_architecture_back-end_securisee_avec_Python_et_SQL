import unittest
from unittest.mock import MagicMock, patch
from controllers import UserController
import models
import constantes
import validators
import jwt
from datetime import datetime, timedelta
import os


class TestUserController(unittest.TestCase):
    def setUp(self):
        # Mocking dependencies
        self.session = MagicMock()
        self.salt = os.getenv("salt")
        self.secret_key = os.getenv("secret_key")
        self.view = MagicMock()
        self.user = None
        # Création de l'instance de UserController
        self.user_controller = UserController(
            self.session, self.salt, self.secret_key, self.view, self.user
        )

    @patch("models.User")
    @patch("validators.validate_email")
    @patch("validators.validate_password")
    @patch("validators.validate_phone")
    def test_create_user(
        self,
        mock_validate_phone,
        mock_validate_password,
        mock_validate_email,
        mock_user,
    ):
        # Mock des valeurs d'entrée
        self.view.input_email.return_value = "test@example.com"
        self.view.input_password.return_value = "password"
        self.view.input_user_role.return_value = 1
        self.view.input_username.return_value = "username"
        self.view.input_full_name.return_value = "full name"
        self.view.input_phone_number.return_value = "+33110203040"

        # Configuration des valeurs de retour du mock
        mock_user_instance = MagicMock()
        mock_user_instance.email = "test@example.com"
        mock_user_instance.password = "password"
        mock_user_instance.role_id = 1
        mock_user_instance.username = "username"
        mock_user_instance.full_name = "full name"
        mock_user_instance.phone_number = "+33110203040"
        mock_user.return_value = mock_user_instance

        # Appel de la méthode create_user
        self.user_controller.create_user()

        # Assertions
        self.view.display_new_user_panel.assert_called_once()
        self.session.add.assert_called_once_with(mock_user_instance)
        self.session.commit.assert_called_once()
        self.view.display_new_user_validation.assert_called_once()
        self.assertEqual(mock_user_instance.email, "test@example.com")
        self.assertEqual(mock_user_instance.password, "password")
        self.assertEqual(mock_user_instance.role_id, 1)
        self.assertEqual(mock_user_instance.username, "username")
        self.assertEqual(mock_user_instance.full_name, "full name")
        self.assertEqual(mock_user_instance.phone_number, "+33110203040")

    @patch("models.User")
    def test_update_user(self, mock_user):
        # Mock des valeurs d'entrée
        self.view.input_email.return_value = "test@example.com"
        self.view.input_update_user.return_value = {
            "username": "new_username",
            "full_name": "new full name",
            "email": "new_test@example.com",
            "phone_number": "+33110203040",
            "role_id": 2,
        }

        # Configuration des valeurs de retour du mock
        mock_user_instance = MagicMock()
        mock_user_instance.email = "test@example.com"
        mock_user_instance.password = "password"
        mock_user_instance.role_id = 1
        mock_user_instance.username = "username"
        mock_user_instance.full_name = "full name"
        mock_user_instance.phone_number = "+33110203040"
        self.session.query().filter_by().first.return_value = (
            mock_user_instance
        )

        # Appel de la méthode update_user
        self.user_controller.update_user()

        # Assertions
        self.view.display_update_user.assert_called_once()
        self.session.commit.assert_called_once()
        self.view.display_update_user_validation.assert_called_once()
        self.assertEqual(mock_user_instance.username, "new_username")
        self.assertEqual(mock_user_instance.full_name, "new full name")
        self.assertEqual(mock_user_instance.email, "new_test@example.com")
        self.assertEqual(mock_user_instance.phone_number, "+33110203040")
        self.assertEqual(mock_user_instance.role_id, 2)

    @patch("models.User")
    def test_delete_user(self, mock_user):
        # Mock des valeurs d'entrée
        self.view.input_email.return_value = "test@example.com"

        # Configuration des valeurs de retour du mock
        mock_user_instance = MagicMock()
        mock_user_instance.email = "test@example.com"
        self.session.query().filter_by().first.return_value = (
            mock_user_instance
        )

        # Appel de la méthode delete_user
        self.user_controller.delete_user()

        # Assertions
        self.view.display_delete_user.assert_called_once()
        self.session.delete.assert_called_once_with(mock_user_instance)
        self.session.commit.assert_called_once()
        self.view.display_delete_user_validation.assert_called_once()


class SalesController:
    def __init__(self, session, view):
        self.session = session
        self.view = view

    def create_customer(self):
        self.view.display_new_customer_panel()
        new_customer = models.Customer(
            name=self.view.input_customer_name(),
            email=self.view.input_customer_email(),
            phone=self.view.input_customer_phone(),
            address=self.view.input_customer_address(),
        )
        try:
            self.session.add(new_customer)
            self.session.commit()
            return self.view.display_new_customer_validation()
        except Exception as err:
            self.session.rollback()
            return self.view.display_new_customer_error()

    def update_customer(self, customer_id):
        self.view.display_update_customer()
        customer = (
            self.session.query(models.Customer)
            .filter_by(id=customer_id)
            .first()
        )
        if not customer:
            return self.view.display_error("Customer not found")

        customer.name = self.view.input_customer_name()
        customer.email = self.view.input_customer_email()
        customer.phone = self.view.input_customer_phone()
        customer.address = self.view.input_customer_address()
        try:
            self.session.commit()
            return self.view.display_update_customer_validation()
        except Exception as err:
            self.session.rollback()
            return self.view.display_update_customer_error()


class SalesController:
    def __init__(self, session, view):
        self.session = session
        self.view = view

    def create_customer(self):
        self.view.display_new_customer_panel()
        new_customer = models.Customer(
            name=self.view.input_customer_name(),
            email=self.view.input_customer_email(),
            phone=self.view.input_customer_phone(),
            address=self.view.input_customer_address(),
        )
        try:
            self.session.add(new_customer)
            self.session.commit()
            return self.view.display_new_customer_validation()
        except Exception as err:
            self.session.rollback()
            return self.view.display_new_customer_error()

    def update_customer(self, customer_id):
        self.view.display_update_customer()
        customer = (
            self.session.query(models.Customer)
            .filter_by(id=customer_id)
            .first()
        )
        if not customer:
            return self.view.display_error("Customer not found")

        customer.name = self.view.input_customer_name()
        customer.email = self.view.input_customer_email()
        customer.phone = self.view.input_customer_phone()
        customer.address = self.view.input_customer_address()
        try:
            self.session.commit()
            return self.view.display_update_customer_validation()
        except Exception as err:
            self.session.rollback()
            return self.view.display_update_customer_error()


class TestSalesController(unittest.TestCase):
    def setUp(self):
        self.session = MagicMock()
        self.view = MagicMock()
        self.user_controller = SalesController(self.session, self.view)

    @patch("models.Customer")
    def test_create_customer(self, mock_customer):
        # Mocking the input values
        self.view.input_customer_name.return_value = "Test Customer"
        self.view.input_customer_email.return_value = (
            "test_customer@example.com"
        )
        self.view.input_customer_phone.return_value = "+33110203040"
        self.view.input_customer_address.return_value = "123 Test Street"

        # Setting up mock return values
        mock_customer_instance = MagicMock()
        mock_customer_instance.name = "Test Customer"
        mock_customer_instance.email = "test_customer@example.com"
        mock_customer_instance.phone = "+33110203040"
        mock_customer_instance.address = "123 Test Street"
        mock_customer.return_value = mock_customer_instance

        # Calling create_customer method
        self.user_controller.create_customer()

        # Assertions
        self.view.display_new_customer_panel.assert_called_once()
        self.session.add.assert_called_once_with(mock_customer_instance)
        self.session.commit.assert_called_once()
        self.view.display_new_customer_validation.assert_called_once()
        self.assertEqual(mock_customer_instance.name, "Test Customer")
        self.assertEqual(
            mock_customer_instance.email, "test_customer@example.com"
        )
        self.assertEqual(mock_customer_instance.phone, "+33110203040")
        self.assertEqual(mock_customer_instance.address, "123 Test Street")

    @patch("models.Customer")
    def test_update_customer(self, mock_customer):
        # Mocking the input values
        customer_id = 1
        self.view.input_customer_name.return_value = "Updated Customer"
        self.view.input_customer_email.return_value = (
            "updated_customer@example.com"
        )
        self.view.input_customer_phone.return_value = "+33110203040"
        self.view.input_customer_address.return_value = "321 Updated Street"

        # Setting up mock return values
        mock_customer_instance = MagicMock()
        self.session.query().filter_by().first.return_value = (
            mock_customer_instance
        )

        # Calling update_customer method
        self.user_controller.update_customer(customer_id)

        # Assertions
        self.view.display_update_customer.assert_called_once()
        self.session.commit.assert_called_once()
        self.view.display_update_customer_validation.assert_called_once()
        self.assertEqual(mock_customer_instance.name, "Updated Customer")
        self.assertEqual(
            mock_customer_instance.email, "updated_customer@example.com"
        )
        self.assertEqual(mock_customer_instance.phone, "+33110203040")
        self.assertEqual(mock_customer_instance.address, "321 Updated Street")
