from unittest import TestCase
from unittest.mock import patch, MagicMock
import os
import bcrypt
import models
from tests.config_test import new_mock_user_controller
import constantes
import validators

salt = os.getenv("salt")
secret_key = os.getenv("secret_key")


class UserControllerLogin(TestCase):
    def setUp(self):
        self.controller = new_mock_user_controller(salt, secret_key)

    def test_login_user_not_found(self):
        self.controller.view.input_email.return_value = "test@free.fr"
        self.controller.view.input_password.return_value = "notgood"
        (
            self.controller.session.query.return_value.filter_by.return_value.first
        ).return_value = None
        with self.assertRaises(ValueError) as error:
            self.controller.run_login_menu()
            self.assertEqual(
                str(error.exception), constantes.ERR_USER_NOT_FOUND
            )

    def test_login_is_password_not_correct(self):
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

        self.controller.view.input_email.return_value = "test@free.fr"
        self.controller.view.input_password.return_value = "notgoodpw"
        self.controller.is_password_correct = MagicMock(return_value=False)
        self.controller.session.query.return_value.filter_by.return_value.first.return_value = (
            user_test
        )
        user = self.controller.run_login_menu()
        self.assertEqual(user, user_test)
        self.assertEqual(user, self.controller.user)

    def test_login_normal_behavior(self):
        user_test = models.User(
            username="test",
            email="test@free.fr",
            password="goodpw",
            full_name="test",
            phone_number="+33110203040",
            role_id=1,
        )
        self.controller.view.input_email.return_value = "test@free.fr"
        self.controller.view.input_password.return_value = "goodpw"
        self.controller.is_password_correct = MagicMock(return_value=True)
        (
            self.controller.session.query.return_value.filter_by.return_value.first
        ).return_value = user_test
        user = self.controller.run_login_menu()
        self.assertEqual(user, user_test)
        self.assertEqual(user, self.controller.user)

    def test_password_hashing(self):
        password = "goodpw"
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), salt.encode("utf-8")
        ).decode("utf-8")
        self.assertNotEqual(password, hashed_password)
        self.assertTrue(
            bcrypt.checkpw(
                password.encode("utf-8"), hashed_password.encode("utf-8")
            )
        )


class UserControllerManageusers(TestCase):

    def setUp(self):
        self.controller = new_mock_user_controller(salt, secret_key)

    def test_manage_users_not_good_input(self):

        self.controller.view.input_user_management.return_value = 4
        with patch.object(
            self.controller.view, "display_error"
        ) as mock_display_error:
            self.controller.manage_user()
            mock_display_error.assert_called_with(
                constantes.MAIN_CONTROLLER_ERR_INPUT
            )

    def test_manage_users_create(self):
        self.controller.view.input_user_management.return_value = (
            constantes.MANAGER_CREATE_NEW_USER
        )
        with patch.object(self.controller, "create_user") as mock_create_user:
            self.controller.manage_user()
            mock_create_user.assert_called_once()

    def test_manage_users_update(self):
        self.controller.view.input_user_management.return_value = (
            constantes.MANAGER_UPDATE_USER
        )
        with patch.object(self.controller, "update_user") as mock_update_user:
            self.controller.manage_user()
            mock_update_user.assert_called_once()

    def test_manage_users_delete(self):
        self.controller.view.input_user_management.return_value = (
            constantes.MANAGER_DELETE_USER
        )
        with patch.object(self.controller, "delete_user") as mock_delete_user:
            self.controller.manage_user()
            mock_delete_user.assert_called_once()

    def test_back_action(self):
        self.controller.view.input_user_management.return_value = 0
        with patch.object(self.controller, "create_user") as mock_create:
            with patch.object(self.controller, "update_user") as mock_update:
                with patch.object(
                    self.controller, "delete_user"
                ) as mock_delete:
                    self.controller.manage_user()
                    mock_create.assert_not_called()
                    mock_update.assert_not_called()
                    mock_delete.assert_not_called()
                    self.controller.view.display_error.assert_not_called()


class TestUserControllerCrud(TestCase):
    def setUp(self):
        self.controller = new_mock_user_controller(salt, secret_key)

    def test_create_user(self):
        self.controller.view.input_username.return_value = "test"
        self.controller.view.input_email.return_value = "test@free.fr"
        self.controller.view.input_password.return_value = "goodpw"
        self.controller.view.input_full_name.return_value = "test"
        self.controller.view.input_phone_number.return_value = "+33110203040"
        self.controller.view.input_role_id.return_value = 1
        self.controller.create_user()
        self.controller.session.add.assert_called_once()
        self.controller.session.commit.assert_called_once()
        self.controller.view.display_new_user_validation.assert_called_once()
        self.controller.view.display_new_user_error.assert_not_called()

    def test_get_user_bad_email(self):
        self.controller.view.input_email.return_value = "notgood@free.fr"
        self.controller.session.query.return_value.filter_by.return_value.first.return_value = (
            None
        )
        with self.assertRaises(ValueError) as err:
            self.controller.get_user()
        self.assertEqual(str(err.exception), constantes.ERR_USER_NOT_FOUND)

    def test_get_user(self):

        user_test = models.User(
            username="test",
            email="test@free.fr",
            password="goodpw",
            full_name="test",
            phone_number="1234567890",
            role_id=1,
        )
        self.controller.view.input_email.return_value = "test@free.fr"
        (
            self.controller.session.query.return_value.filter_by.return_value.first
        ).return_value = user_test
        user = self.controller.get_user()
        self.assertEqual(user_test, user)

    def test_update_user(self):

        user_test = models.User(
            username="test",
            email="test@free.fr",
            password="goodpw",
            full_name="test",
            phone_number="1234567890",
            role_id=1,
        )

        self.controller.session.query.return_value.filter_by.return_value.first.return_value = (
            user_test
        )
        self.controller.view.input_email.return_value = "test@free.fr"
        self.controller.view.input_update_user.return_value = {
            "username": "updated_test",
            "full_name": "updated_test",
            "email": "updated_test@free.fr",
            "phone_number": "+33110203040",
            "role_id": 2,
        }
        self.controller.update_user()

        self.assertEqual(user_test.username, "updated_test")
        self.assertEqual(user_test.full_name, "updated_test")
        self.assertEqual(user_test.email, "updated_test@free.fr")
        self.assertEqual(user_test.phone_number, "+33110203040")
        self.assertEqual(user_test.role_id, 2)
        self.controller.session.commit.assert_called_once()
        self.controller.view.display_update_user_validation.assert_called_once()

    def test_delete_user_valid(self):
        user_test = models.User(
            username="test",
            email="test@free.fr",
            password="goodpw",
            full_name="test",
            phone_number="33110203040",
            role_id=1,
        )

        self.controller.session.query.return_value.filter_by.return_value.first.return_value = (
            user_test
        )
        self.controller.view.input_email.return_value = "test@free.fr"
        self.controller.delete_user()

        self.controller.session.delete.assert_called_once_with(user_test)
        self.controller.session.commit.assert_called_once()
        self.controller.view.display_delete_user_validation.assert_called_once()
        self.controller.view.display_delete_user_error.assert_not_called()

    def test_get_user_bad_email(self):
        self.controller.view.input_email.return_value = "notgood@free.fr"
        self.controller.session.query.return_value.filter_by.return_value.first.return_value = (
            None
        )

        with self.assertRaises(ValueError) as err:
            self.controller.get_user()
            self.controller.view.display_error.assert_called_once_with(
                constantes.ERR_USER_NOT_FOUND
            )
            raise ValueError("USER not found")
