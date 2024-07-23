from unittest import TestCase
from unittest.mock import patch, MagicMock
import os
import bcrypt
import models
from tests.config_test import new_mock_customer_controller
import constantes
import validators

salt = os.getenv("salt")
secret_key = os.getenv("secret_key")


class CustomerController(TestCase):
    def setUp(self):
        self.controller = new_mock_customer_controller()

    def test_create_customer(self):
        customer_data = {
            "first_name": "Test",
            "last_name": "Customer",
            "compagny_name": "Test Company",
        }
        self.controller.view.input_customer_information.return_value = (
            customer_data
        )
        self.controller.user = models.User(
            username="test_user",
            full_name="Test User",
            email="test@example.com",
            phone_number="+33110203040",
            role_id=2,
        )
        with patch.object(
            self.controller, "set_new_customer_email"
        ) as mock_set_email, patch.object(
            self.controller, "set_customer_phone"
        ) as mock_set_phone:

            mock_set_email.return_value = "test@customer.com"
            mock_set_phone.return_value = "+33110203040"

            self.controller.create_customer()

            self.assertEqual(self.controller.session.commit.call_count, 1)

    def test_update_customer(self):
        customer_data = {
            "first_name": "Updated",
            "last_name": "Customer",
            "compagny_name": "Updated Company",
        }
        self.controller.view.input_customer_information.return_value = (
            customer_data
        )
        self.controller.user = models.User(
            username="test_user",
            full_name="Test User",
            email="test@example.com",
            phone_number="+33110203040",
            role_id=2,
        )
        with patch.object(
            self.controller, "set_new_customer_email"
        ) as mock_set_email, patch.object(
            self.controller, "set_customer_phone"
        ) as mock_set_phone:

            mock_set_email.return_value = "updated@customer.com"
            mock_set_phone.return_value = "+33110203041"

            self.controller.update_customer()

            self.assertEqual(self.controller.session.commit.call_count, 1)

    def test_get_customer(self):
        # Créer un objet Customer factice pour simuler la récupération depuis la base de données
        self.controller.user = models.User(
            username="test_user",
            full_name="Test User",
            email="test@example.com",
            phone_number="+33110203040",
            role_id=2,
        )
        mock_customer = models.Customer(
            first_name="Test",
            last_name="Customer",
            email="test@customer.com",
            phone_number="+33110203040",
            compagny_name="Test Company",
            sales_id=self.controller.user.id,
        )

        # Configurer le mock de la session pour retourner l'objet Customer factice
        self.controller.session.query().filter_by().first.return_value = (
            mock_customer
        )

        # Appeler la méthode get_customer
        retrieved_customer = self.controller.get_customer(self.controller.user)

        # Vérifier que les attributs de l'objet Customer sont corrects
        self.assertEqual(retrieved_customer.first_name, "Test")
        self.assertEqual(retrieved_customer.last_name, "Customer")
        self.assertEqual(retrieved_customer.email, "test@customer.com")
        self.assertEqual(retrieved_customer.phone_number, "+33110203040")
        self.assertEqual(retrieved_customer.compagny_name, "Test Company")

    def test_list_customer(self):

        self.controller.user = models.User(
            username="test_user",
            full_name="Test User",
            email="test@example.com",
            phone_number="+33110203040",
            role_id=2,
        )  # Configurer le mock de la session pour retourner une liste d'objets Customer factices
        mock_customers = [
            models.Customer(
                first_name="Test1",
                last_name="Customer1",
                email="test1@customer.com",
                phone_number="+33110203041",
                compagny_name="Test Company1",
                sales_id=self.controller.user.id,
            ),
            models.Customer(
                first_name="Test2",
                last_name="Customer2",
                email="test2@customer.com",
                phone_number="+33110203042",
                compagny_name="Test Company2",
                sales_id=self.controller.user.id,
            ),
        ]
        self.controller.session.query().all.return_value = mock_customers
        with patch.object(
            self.controller.view, "display_customer_not_found"
        ) as mock_display_not_found, patch.object(
            self.controller.view, "display_customer_information"
        ) as mock_display_info:

            self.controller.list_customers()

            # Vérifier que les méthodes d'affichage sont appelées correctement
            mock_display_info.assert_called_once_with(mock_customers)
            mock_display_not_found.assert_not_called()
