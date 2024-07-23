import unittest
from unittest.mock import patch, MagicMock
import models
import constantes
from views import CustomerView
from rich.panel import Panel


class TestCustomerView(unittest.TestCase):

    def setUp(self):
        self.console = MagicMock()

        self.view = CustomerView(self.console)

    @patch("builtins.input", side_effect=["fisrt name"])
    def test_input_input_first_name(self, mock_input):
        result = self.view.input_first_name()
        self.assertEqual(result, "fisrt name")
        self.console.print("First name : ", style="input")

    @patch("builtins.input", side_effect=["last name"])
    def test_input_last_name(self, mock_input):
        result = self.view.input_last_name()
        self.assertEqual(result, "last name")
        self.console.print("Last name : ", style="input")

    @patch("builtins.input", side_effect=["test@free.fr"])
    def test_input_email(self, mock_input):
        result = self.view.input_email()
        self.assertEqual(result, "test@free.fr")
        self.console.print("email customer : ", style="input")

    @patch("builtins.input", side_effect=["+33110203040"])
    def test_input_phone_number(self, mock_input):
        result = self.view.input_phone_number()
        self.assertEqual(result, "+33110203040")
        self.console.print(
            "phone number: (must start with +33) : ", style="input"
        )

    @patch("builtins.input", side_effect=["compagny test"])
    def test_input_customer_information(self, mock_input):
        result = self.view.input_compagny_name()
        self.assertEqual(result, "compagny test")
        self.console.print("Compagny name : ", style="input")

    def test_display_new_customer_validation(self):
        with patch("views.CustomerView.wait_for_key_press"):
            self.view.display_new_customer_validation()
            self.console.print.assert_called_with(
                "[success]New customer correctly created[/]"
            )

    def test_display_update_customer_validation(self):
        with patch("views.CustomerView.wait_for_key_press"):
            self.view.display_update_customer_validation()
            self.console.print.assert_called_with(
                "Customer successfully updated", style="success"
            )

    def test_display_customer_not_found(self):
        with patch("views.CustomerView.wait_for_key_press"):
            self.view.display_customer_not_found()
            self.console.print.assert_called_with(
                "Customer not found", style="error"
            )

    def test_display_not_your_customer(self):
        with patch("views.CustomerView.wait_for_key_press"):
            self.view.display_not_your_customer()
            self.console.print.assert_called_with(
                "the customer is not assigned to you", style="error"
            )

    def test_display_error(self, message="test"):
        with patch("views.CustomerView.wait_for_key_press"):
            self.view.display_error(message)
            self.console.print.assert_called_with(f"[error] {message} [/]")
