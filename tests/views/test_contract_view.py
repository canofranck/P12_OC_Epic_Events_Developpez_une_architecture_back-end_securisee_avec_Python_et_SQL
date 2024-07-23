import unittest
from unittest.mock import patch, MagicMock
import models
import constantes
from views import ContractView


class TestContractView(unittest.TestCase):

    def setUp(self):
        self.console = MagicMock()

        self.view = ContractView(self.console)

    @patch("builtins.input", side_effect=["1"])
    def test_input_contract_management(self, mock_input):
        result = self.view.input_contract_management()
        self.assertEqual(result, 1)
        self.console.print.assert_any_call(
            "[menu_choice]" + constantes.LOG_OUT + " - Exit[/]"
        )
        self.console.print.assert_any_call(
            "[menu_choice]"
            + constantes.MANAGER_CREATE_NEW_CONTRACT
            + " - Create a new Contract[/]"
        )
        self.console.print.assert_any_call(
            "[menu_choice]"
            + constantes.MANAGER_UPDATE_CONTRACT
            + " - Update a Contract[/]"
        )

    def test_input_list_contracts_filters_no_filter(self):
        with patch("builtins.input", side_effect=["1"]):
            result = self.view.input_list_contracts_filters()
            self.assertEqual(result, "1")

    def test_input_list_contracts_filters_not_signed(self):
        with patch("builtins.input", side_effect=["2"]):
            result = self.view.input_list_contracts_filters()
            self.assertEqual(result, "2")

    def test_input_list_contracts_filters_not_total_paid(self):
        with patch("builtins.input", side_effect=["3"]):
            result = self.view.input_list_contracts_filters()
            self.assertEqual(result, "3")

    def test_input_list_contracts_filters_invalid_input(self):
        with patch("builtins.input", side_effect=["invalid", "1"]):
            result = self.view.input_list_contracts_filters()
            self.assertEqual(result, "1")

    @patch("builtins.input", side_effect=["1000"])
    def test_input_contract_amount(self, mock_input):
        result = self.view.input_contract_amount()
        self.assertEqual(result, "1000")
        self.console.print.assert_called_with("Total amount : ", style="input")

    @patch("builtins.input", side_effect=["500"])
    def test_input_contract_remaining_amount(self, mock_input):
        result = self.view.input_contract_remaining_amount(200, 1000)
        self.assertEqual(result, 500)
        self.console.print.assert_any_call(
            "Insert the new amount remaining to be paid : ", style="input"
        )

    @patch("builtins.input", side_effect=["1"])
    def test_input_contract_signed(self, mock_input):
        result = self.view.input_contract_signed()
        self.assertTrue(result)
        self.console.print.assert_called_with(
            "Contract already signed ? (0  for NO / 1 for YES) : ",
            style="input",
        )

    def test_display_contract_informations(self):
        contract = models.Contract(
            customer=MagicMock(
                first_name="John",
                last_name="Doe",
                user=MagicMock(username="johndoe"),
            ),
            user=MagicMock(full_name="Jane Smith"),
            is_signed=True,
            remaining_amount=1000.00,
            total_amount=2000.00,
        )
        self.view.display_contract_informations(contract)
        self.console.print.assert_called()

    def test_input_contract_management_exit(self):
        with patch("builtins.input", side_effect=["0"]):
            result = self.view.input_contract_management()
            self.assertEqual(result, 0)

    def test_input_contract_management_create_new_contract(self):
        with patch("builtins.input", side_effect=["1"]):
            result = self.view.input_contract_management()
            self.assertEqual(result, 1)

    def test_input_contract_management_update_contract(self):
        with patch("builtins.input", side_effect=["2"]):
            result = self.view.input_contract_management()
            self.assertEqual(result, 2)

    def test_input_contract_management_invalid_input_then_valid(self):
        with patch("builtins.input", side_effect=["invalid", "1"]):
            result = self.view.input_contract_management()
            self.assertEqual(result, 1)

    def test_input_contract_amount_valid_input(self):
        with patch("builtins.input", return_value="1000"):
            result = self.view.input_contract_amount()
            self.assertEqual(result, "1000")

    def test_input_contract_remaining_amount_valid_input(self):
        with patch("builtins.input", side_effect=["500"]):
            result = self.view.input_contract_remaining_amount(200, 1000)
            self.assertEqual(result, 500)

    def test_input_contract_remaining_amount_invalid_then_valid(self):
        with patch("builtins.input", side_effect=["invalid", "600"]):
            result = self.view.input_contract_remaining_amount(200, 1000)
            self.assertEqual(result, 600)

    def test_input_contract_signed_signed(self):
        with patch("builtins.input", return_value="1"):
            result = self.view.input_contract_signed()
            self.assertTrue(result)

    def test_input_contract_signed_not_signed(self):
        with patch("builtins.input", return_value="0"):
            result = self.view.input_contract_signed()
            self.assertFalse(result)

    def test_input_contract_signed_invalid_input_then_valid(self):
        with patch("builtins.input", side_effect=["invalid", "1"]):
            result = self.view.input_contract_signed()
            self.assertTrue(result)

    def test_input_contract_signed_signed(self):
        with patch("builtins.input", return_value="1"):
            result = self.view.input_contract_signed()
            self.assertTrue(result)

    def test_input_contract_signed_not_signed(self):
        with patch("builtins.input", return_value="0"):
            result = self.view.input_contract_signed()
            self.assertFalse(result)

    def test_input_contract_signed_invalid_input_then_valid(self):
        with patch("builtins.input", side_effect=["invalid", "1"]):
            result = self.view.input_contract_signed()
            self.assertTrue(result)

    def test_display_new_contract_validation(self):
        with patch("views.ContractView.wait_for_key_press"):
            self.view.display_new_contract_validation()
            self.console.print.assert_called_with(
                "[success]Contract successfully created[/]"
            )

    def test_display_update_contract_validation(self):
        with patch("views.ContractView.wait_for_key_press"):
            self.view.display_update_contract_validation()
            self.console.print.assert_called_with(
                "[success]Contract successfully updated[/]"
            )

    def test_display_no_contract_found(self):
        with patch("views.ContractView.wait_for_key_press"):
            result = self.view.display_no_contract_found()
            self.console.print.assert_called_with(
                "[error]No contract found[/]"
            )

    def test_display_error(self):
        message = "Custom error message"
        self.view.display_error(message)
        self.console.print.assert_called_with(f"[error] {message} [/]")
