import unittest
from unittest.mock import patch, MagicMock
import models
import constantes
from views import UserView


class TestUserView(unittest.TestCase):

    def setUp(self):
        self.console = MagicMock()

        self.view = UserView(self.console)

    @patch("builtins.input", side_effect=["test@free.fr"])
    def test_input_email(self, mock_input):
        result = self.view.input_email()
        self.assertEqual(result, "test@free.fr")
        self.console.print("Enter email : ", style="input")

    @patch("builtins.input", side_effect=["test@free.fr"])
    def test_input_email(self, mock_input):
        result = self.view.input_email()
        self.assertEqual(result, "test@free.fr")
        self.console.print("Enter email : ", style="input")

    @patch("builtins.input", side_effect=["username"])
    def test_input_username(self, mock_input):
        result = self.view.input_username()
        self.assertEqual(result, "username")
        self.console.print("Username : ", style="input")

    @patch("builtins.input", side_effect=["username"])
    def test_input_full_name(self, mock_input):
        result = self.view.input_full_name()
        self.assertEqual(result, "username")
        self.console.print("Full name : ", style="input")

    def test_display_new_user_validation(self):
        with patch("views.CustomerView.wait_for_key_press"):
            self.view.display_new_user_validation()
            self.console.print("[success]New user correctly created[/]")

    def test_display_new_user_error(self):
        with patch("views.CustomerView.wait_for_key_press"):
            self.view.display_new_user_error()
            self.console.print("[error]New user not created[/]")

    @patch("builtins.input", side_effect=["+33110203040"])
    def test_input_phone_number(self, mock_input):
        result = self.view.input_phone_number()
        self.assertEqual(result, "+33110203040")
        self.console.print(
            "phone number: (must start with +33) : ", style="input"
        )

    def test_display_update_user_validation(self):
        with patch("views.CustomerView.wait_for_key_press"):
            self.view.display_update_user_validation()
            self.console.print("[success]User successfully updated[/]")

    def test_display_delete_user_validation(self):
        with patch("views.CustomerView.wait_for_key_press"):
            self.view.display_delete_user_validation()
            self.console.print("[success]User successfully deleted[/]")

    def test_display_support_on_event(self):
        with patch("views.CustomerView.wait_for_key_press"):
            self.view.display_support_on_event()
            self.console.print(
                "Enter Email support to assign : ", style="input"
            )
