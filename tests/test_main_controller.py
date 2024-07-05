# import unittest
# from unittest.mock import patch, MagicMock
# from main import MainController
# from database_test import init_db_test
# import os
# import constantes

# import themes
# import sqlalchemy
# from database_test import create_database

# DATABASE_USERNAME = "root"
# DATABASE_PASSWORD = "Password2325"
# DATABASE_HOST = "localhost"
# DATABASE_NAME = "p12_testrole2_test"
# salt = "$2b$12$QhTfGmCB1FrbuySv8Op4IO"
# secret_key = "#zfhtz-4bpoqens*3jx9p9=hhz(67x#4atd5^5id%kh32kqkb2"


# class TestMainController(unittest.TestCase):

#     @classmethod
#     def setUpClass(cls):
#         # Créer la base de données de test avant tous les tests
#         pass

#     @patch("themes.theme_console")
#     @patch("sentry_sdk.init")
#     def setUp(self, mock_sentry, mock_theme):
#         self.mock_session = MagicMock()
#         self.mock_console = MagicMock()
#         self.mock_view = MagicMock()
#         self.mock_user_controller = MagicMock()
#         self.mock_customer_controller = MagicMock()
#         self.mock_contract_controller = MagicMock()
#         self.mock_event_controller = MagicMock()

#         with patch("views.MainView", return_value=self.mock_view):
#             with patch(
#                 "controllers.UserController",
#                 return_value=self.mock_user_controller,
#             ):
#                 with patch(
#                     "controllers.CustomerController",
#                     return_value=self.mock_customer_controller,
#                 ):
#                     with patch(
#                         "controllers.ContractController",
#                         return_value=self.mock_contract_controller,
#                     ):
#                         with patch(
#                             "controllers.EventController",
#                             return_value=self.mock_event_controller,
#                         ):
#                             self.main_controller = MainController(
#                                 session=self.mock_session,
#                                 salt=salt,
#                                 secret_key=secret_key,
#                                 console=self.mock_console,
#                             )

#     @patch("models.User")
#     @patch("models.Role")
#     def test_create_admin(self, MockRole, MockUser):
#         # Configurer les mocks pour les requêtes de la base de données
#         mock_admin_user = None
#         mock_manager_role = MockRole(name="MANAGER", id=1)

#         self.mock_session.query().filter_by().first.side_effect = [
#             mock_admin_user,
#             mock_manager_role,
#         ]

#         # Configurer le mock pour l'utilisateur admin
#         mock_user_instance = MockUser.return_value
#         mock_user_instance.username = "Admin"
#         mock_user_instance.email = "admin@example.com"
#         mock_user_instance.role_id = mock_manager_role.id

#         # Appeler la méthode create_admin
#         self.main_controller.create_admin()

#         # Vérifier que self.session.add a été appelé une fois
#         self.mock_session.add.assert_called_once()
#         self.mock_session.commit.assert_called_once()

#         # Vérifier que l'utilisateur admin a été créé avec les bonnes valeurs
#         created_admin = self.mock_session.add.call_args[0][0]
#         print(
#             f"Admin créé : {created_admin.username}, {created_admin.email}, {created_admin.role_id}"
#         )
#         self.assertEqual(created_admin.username, "Admin")
#         self.assertEqual(created_admin.email, "admin@example.com")
#         self.assertEqual(created_admin.role_id, mock_manager_role.id)

#     def test_run_login(self):
#         # Simuler l'entrée de l'utilisateur pour le login
#         self.mock_view.display_main_menu.return_value = (
#             constantes.MAIN_MENU_LOGIN
#         )
#         mock_user = MagicMock(username="test_user")
#         self.mock_user_controller.run_login_menu.return_value = mock_user

#         # Appeler la méthode run
#         with patch("builtins.print"):
#             self.main_controller.run()

#         # Vérifier que les méthodes appropriées ont été appelées
#         self.mock_view.clear_screen.assert_called()
#         self.mock_view.display_main_menu.assert_called()
#         self.mock_user_controller.run_login_menu.assert_called_once()
#         self.mock_view.input_welcome_user.assert_called_once_with(mock_user)
#         self.mock_view.clear_screen.assert_called()
#         self.mock_view.display_main_menu.assert_called()

#     def test_run_quit(self):
#         # Simuler l'entrée de l'utilisateur pour quitter
#         self.mock_view.display_main_menu.return_value = (
#             constantes.MAIN_MENU_QUIT
#         )

#         # Appeler la méthode run
#         with patch("builtins.print"):
#             self.main_controller.run()

#         # Vérifier que les méthodes appropriées ont été appelées
#         self.mock_view.clear_screen.assert_called()
#         self.mock_view.display_main_menu.assert_called()
#         self.mock_view.display_main_menu.assert_called()
#         self.mock_view.display_main_menu.assert_called()

#     def tearDownClass(cls):

#         pass


# if __name__ == "__main__":
#     unittest.main()
