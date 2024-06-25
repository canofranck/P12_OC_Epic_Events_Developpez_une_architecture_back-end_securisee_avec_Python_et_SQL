from os import name, system
import constantes
import views


class MainView:

    def display_main_menu(self):
        """
        Affiche le menu principal.
        Returns:
            str: Le choix de l'utilisateur.
        """

        print("--- Welcome to Epic Events CRM ---")
        print("\nMenu :")
        print(constantes.MAIN_MENU_LOGIN, "Login")
        print(constantes.MAIN_MENU_QUIT, "Quitter")
        return input("Choisissez une option : ")

    def display_invalid_option_message():
        """
        Affiche un message indiquant qu'une option invalide a été sélectionnée.
        """
        print("Option invalide. Veuillez choisir une option valide.")

    def clear_screen(self):
        """Clear the terminal"""
        # for windows

        if name == "nt":
            _ = system("cls")
        # for mac and linux

        else:
            _ = system("clear")

    def input_welcome_user(self, user):
        print(f"--- Welcome Back {user.full_name} ---")
