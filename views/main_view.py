from os import name, system
import constantes
import views
from rich.panel import Panel
from rich.rule import Rule


class MainView(views.BaseView):

    def display_main_menu(self):
        """
        Affiche le menu principal.
        Returns:
            str: Le choix de l'utilisateur.
        """

        self.console.print(
            Panel("--- Welcome to Epic Events CRM ---", expand=True),
            style="panel",
            justify="center",
        )
        self.console.print()
        self.console.print(
            Panel("---  Menu  ---", expand=True), style="menu_text"
        )

        self.console.print(
            "[menu_choice]" + constantes.MAIN_MENU_QUIT + " - Quitter [/]"
        )
        self.console.print(
            "[menu_choice]" + constantes.MAIN_MENU_LOGIN + " - Login [/]"
        )
        self.console.print()
        self.console.print("Choisissez une option : ", style="input")
        return input()

    def display_invalid_option_message(self):
        """
        Affiche un message indiquant qu'une option invalide a été sélectionnée.
        """
        self.console.print(
            "[error]Option invalide. Veuillez choisir une option valide.[/]"
        )

    def clear_screen(self):
        """Clear the terminal"""
        # for windows

        if name == "nt":
            _ = system("cls")
        # for mac and linux

        else:
            _ = system("clear")

    def input_welcome_user(self, user):

        self.console.print(
            Panel(f"--- Welcome Back {user.full_name} ---", expand=True),
            style="panel",
            justify="center",
        )

    def display_manage_contract(self):
        self.console.print(
            Panel("---   Manage Contract   ---", expand=True),
            style="menu_text",
        )

    def display_set_support_on_event(self):
        self.console.print(
            Panel("---   Set Support on Event   ---", expand=True),
            style="menu_text",
        )

    def display_not_support_user(self):
        self.console.print("[error]Not support user[/]")

    def display_create_event(self):
        self.console.print(
            Panel("---   Create Event   ---", expand=True),
            style="menu_text",
        )

    def display_update_contract(self):
        self.console.print(
            Panel("---   Update Contract management   ---", expand=True),
            style="menu_text",
        )

    def display_logout(self):
        self.console.print(
            Panel("---   Logout   ---", expand=True),
            style="menu_text",
        )
        self.console.print(
            "Do you want to logout and keep credentials  Yes or No?"
        )
        return input()
