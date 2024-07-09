from os import name, system
import constantes
import views
from rich.panel import Panel
from rich.rule import Rule


class MainView(views.BaseView):
    """
    The MainView class is responsible for managing the main view of the application.

    Methods:
        display_main_menu(self):
            Displays the main menu and prompts the user to choose an option.

        display_invalid_option_message(self):
            Displays a message indicating that an invalid option was selected.

        clear_screen(self):
            Clears the terminal screen.

        input_welcome_user(self, user):
            Displays a welcome message for the user.

        display_manage_contract(self):
            Displays a panel with the title "Manage Contract".

        display_set_support_on_event(self):
            Displays a panel with the title "Set Support on Event".

        display_not_support_user(self):
            Displays an error message indicating that the user is not a support user.

        display_create_event(self):
            Displays a panel with the title "Create Event".

        display_update_contract(self):
            Displays a panel with the title "Update Contract management".

        display_logout(self):
            Displays a panel with the title "Logout".

    """

    def display_main_menu(self):
        """
        Displays the main menu and prompts the user to choose an option.

        Returns:
            str: The user's choice.
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
        Displays a message indicating that an invalid option was selected.
        """
        self.console.print(
            "[error]Invalid option. Please choose a valid option.[/]"
        )

    def clear_screen(self):
        """
        Clears the terminal screen.
        """
        # for windows

        if name == "nt":
            _ = system("cls")
        # for mac and linux

        else:
            _ = system("clear")

    def input_welcome_user(self, user):
        """
        Displays a welcome message for the user.

        Args:
            user (User): The user object.
        """
        self.console.print(
            Panel(f"--- Welcome Back {user.full_name} ---", expand=True),
            style="panel",
            justify="center",
        )

    def display_manage_contract(self):
        """
        Displays a panel with the title "Manage Contract".
        """
        self.console.print(
            Panel("---   Manage Contract   ---", expand=True),
            style="menu_text",
        )

    def display_set_support_on_event(self):
        """
        Displays a panel with the title "Set Support on Event".
        """
        self.console.print(
            Panel("---   Set Support on Event   ---", expand=True),
            style="menu_text",
        )

    def display_not_support_user(self):
        """
        Displays an error message indicating that the user is not a support user.
        """
        self.console.print("[error]Not support user[/]")

    def display_create_event(self):
        """
        Displays a panel with the title "Create Event".
        """
        self.console.print(
            Panel("---   Create Event   ---", expand=True),
            style="menu_text",
        )

    def display_update_contract(self):
        """
        Displays a panel with the title "Update Contract management".
        """
        self.console.print(
            Panel("---   Update Contract management   ---", expand=True),
            style="menu_text",
        )

    def display_logout(self):
        """
        Displays a panel with the title "Logout".
        """
        self.console.print(
            Panel("---   Logout   ---", expand=True),
            style="menu_text",
        )
        self.console.print(
            "Do you want to logout and keep credentials  Yes or No?"
        )
        return input()

    def display_error(self, message):
        """
        Displays an error message.
        """
        self.console.print(f"[error] {message} [/]")
