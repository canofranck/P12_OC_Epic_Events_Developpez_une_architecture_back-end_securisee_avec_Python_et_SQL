from unittest import TestCase
from unittest.mock import patch, MagicMock
import os
import bcrypt
import models
from tests.config_test import new_mock_contract_controller
import constantes
import validators
from datetime import datetime

salt = os.getenv("salt")
secret_key = os.getenv("secret_key")


class UserContract(TestCase):
    def setUp(self):
        self.controller = new_mock_contract_controller()

    def test_create_contract(self):
        user_test = models.User(
            username="test",
            email="test@free.fr",
            password=bcrypt.hashpw(
                "goodpw".encode("utf-8"), salt.encode("utf-8")
            ).decode("utf-8"),
            full_name="test",
            phone_number="+33110203040",
            role_id=1,
        )
        self.controller.user = user_test
        customer = models.Customer(
            first_name="Test Customer",
            last_name="Customer",
            email="customer@test.com",
            phone_number="+33110203041",
            compagny_name="Test Company",
            sales_id=user_test.id,
        )
        # Créer un objet Contract factice pour simuler la création d'un contrat
        contract = models.Contract(total_amount=100, remaining_amount=50)

        # Appeler la méthode create_contract() avec le customer factice
        self.controller.create_contract(customer)

        # Vérifier que l'ID de l'utilisateur dans le contrat est correct
        self.assertEqual(contract.manager_id, user_test.id)

    @patch(
        "controllers.contract_controller.datetime"
    )  # Assurez-vous de patcher le module où datetime.now() est appelé
    def test_update_contract(self, mock_datetime):
        # Préparer les données de test
        mock_datetime.now.return_value = datetime(2023, 12, 31, 23, 59, 59)

        user_test = models.User(
            username="test",
            email="test@free.fr",
            full_name="Test User",
            phone_number="+33110203040",
            role_id=1,
        )
        self.controller.user = user_test

        customer = models.Customer(
            first_name="Test",
            last_name="Customer",
            email="customer@test.com",
            phone_number="+33110203041",
            compagny_name="Test Company",
            sales_id=user_test.id,
        )

        contract = models.Contract(
            customer=customer,
            total_amount=1000,
            remaining_amount=500,
            is_signed=False,
        )
        contract.creation_date = datetime(2023, 1, 1)
        # Mock des méthodes et attributs nécessaires
        self.controller.session.query.return_value.filter_by.return_value.first.return_value = (
            contract
        )
        self.controller.view.input_contract_signed.return_value = True
        self.controller.view.input_contract_remaining_amount.return_value = 0
        self.controller.view.display_update_contract_validation = MagicMock()
        self.controller.view.display_contract_informations = MagicMock()
        self.controller.view.display_error = MagicMock()
        self.controller.view.display_no_contract_found = MagicMock()

        # Appel de la méthode à tester
        self.controller.update_contract(customer)

        # Vérifications des assertions
        self.controller.view.display_contract_informations.assert_called_once_with(
            contract
        )
        self.assertTrue(contract.is_signed)
        self.assertEqual(contract.remaining_amount, 0)
        self.assertEqual(
            contract.creation_date, datetime(2023, 12, 31, 23, 59, 59)
        )
        self.controller.session.commit.assert_called_once()

    def test_update_contract_not_found(self):
        customer = models.Customer(
            first_name="Test",
            last_name="Customer",
            email="customer@test.com",
            phone_number="+33110203041",
            compagny_name="Test Company",
            sales_id=1,
        )

        self.controller.session.query.return_value.filter_by.return_value.first.return_value = (
            None
        )
        self.controller.view.display_no_contract_found = MagicMock()

        self.controller.update_contract(customer)

        self.controller.view.display_no_contract_found.assert_called_once()
        self.controller.session.commit.assert_not_called()

    def test_update_contract_already_signed_and_paid(self):
        customer = models.Customer(
            first_name="Test",
            last_name="Customer",
            email="customer@test.com",
            phone_number="+33110203041",
            compagny_name="Test Company",
            sales_id=1,
        )

        contract = models.Contract(
            customer=customer,
            total_amount=1000,
            remaining_amount=0,
            is_signed=True,
        )

        self.controller.session.query.return_value.filter_by.return_value.first.return_value = (
            contract
        )
        self.controller.view.display_contract_informations = MagicMock()
        self.controller.view.display_error = MagicMock()

        self.controller.update_contract(customer)

        self.controller.view.display_contract_informations.assert_called_once_with(
            contract
        )
        self.controller.view.display_error.assert_called_once_with(
            constantes.CONTRACT_CONTROLLER_CONTRACT_SIGNED_PAID
        )
        self.controller.session.commit.assert_not_called()
