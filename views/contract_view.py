import models
import views
import constantes
from rich.panel import Panel
from rich.table import Table


class ContractView(views.BaseView):
    """
    The ContractView class is responsible for managing the contract-related views in the application.

    Methods:
        input_contract_management(self):
            Displays the contract management menu and handles user input for selecting an action.

        input_contract_amount(self):
            Prompts the user to input the total amount for a contract.

        input_contract_remaining_amount(self, remaining_amount, total_amount):
            Prompts the user to input the new remaining amount to be paid on a contract.
    """

    def input_contract_management(self):
        """
        Displays the contract management menu and handles user input for selecting an action.

        This method presents the user with a menu of contract management options, including exiting the menu,
        creating a new contract, and updating an existing contract. The user is prompted to select an action
        by entering a number corresponding to the desired option. The method validates the user's input and
        returns the selected action.

        Returns:
            int: The number corresponding to the selected action.
        """
        self.console.print("[menu_choice]" + constantes.LOG_OUT + " - Exit[/]")
        self.console.print(
            "[menu_choice]"
            + constantes.MANAGER_CREATE_NEW_CONTRACT
            + " - Create a new Contract[/]"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.MANAGER_UPDATE_CONTRACT
            + " - Update a Contract[/]"
        )
        selection = -1
        while selection < 0 or selection > 2:
            try:
                self.console.print("Select an action : ", style="input")
                selection = int(input())
                if selection > 2 or selection < 0:
                    raise ValueError
            except ValueError:
                self.console.print("[error]bad input[/]")
        return selection

    def input_contract_amount(self):
        """
        Prompts the user to input the total amount for a contract.

        This method displays a message asking the user to input the total amount for a contract. The user's input
        is returned as a string.

        Returns:
            str: The total amount for the contract.
        """
        self.console.print("Total amount : ", style="input")
        return input()

    def input_contract_remaining_amount(self, remaining_amount, total_amount):
        """
        Prompts the user to input the new remaining amount to be paid on a contract.

        This method displays a message asking the user to input the new remaining amount to be paid on a contract.
        The user's input is returned as an integer.

        Returns:
            int: The new remaining amount to be paid on a contract.
        """
        self.console.print(
            f"[menu_text]remaining on bill: {remaining_amount}[/]"
        )

        new_remaining_amount = ""
        while new_remaining_amount == "":
            try:
                self.console.print(
                    "Insert the new amount remaining to be paid : ",
                    style="input",
                )
                new_remaining_amount = int(input())
                if new_remaining_amount > total_amount:
                    self.console.print(
                        "[error]ERROR_REMAINING AMOUNT_TO_BIG[/]"
                    )
                    new_remaining_amount = ""
                    continue
                continue
            except ValueError:
                self.console.print("[error]bad input[/]")
                continue
        return new_remaining_amount

    def input_contract_signed(self):
        """
        Prompts the user to input if the contract is already signed.

        This method displays a message asking the user to input if the contract is already signed. The user's input
        is returned as a boolean.

        Returns:
            bool: True if the contract is signed, False otherwise.
        """
        int_signed = -1
        while int_signed == -1:
            self.console.print(
                "Contract already signed ? (0  for NO / 1 for YES) : ",
                style="input",
            )
            user_input = input()
            if user_input != "0" and user_input != "1":
                self.console.print("[error]bad input[/]")
                continue
            int_signed = user_input
            continue
        if int_signed == "0":
            return False
        return True

    def input_new_contract(self):
        """
        Prompts the user to input the total amount and if the contract is already signed.

        This method displays a message asking the user to input the total amount for a contract. The user's input
        is returned as a string.

        Returns:
            str: The total amount for the contract.
        """
        total_amount_input = self.input_contract_amount()
        is_signed_input = self.input_contract_signed()
        return {
            "total_amount": total_amount_input,
            "is_signed": is_signed_input,
        }

    def display_contract_informations(self, contracts: models.Contract):

        table = Table(title="Liste Contrat")

        table.add_column("Client First Name")
        table.add_column("Client Last Name")
        table.add_column("Commercial Contact Username")
        table.add_column("Commercial contact Fullname")
        table.add_column("Is signed")
        table.add_column("Remaining amount")
        table.add_column("Creation date")
        try:
            iter(contracts)
        except TypeError:
            contract = contracts
            table.add_row(
                contract.customer.first_name,
                contract.customer.last_name,
                contract.customer.user.username,
                contract.user.full_name,
                "Yes" if contract.is_signed else "No",
                "{:.2f}".format(contract.remaining_amount),
                str(contract.creation_date),
            )
            table.column_widths = "auto"
            self.console.print(table)

        else:
            for contract in contracts:
                table.add_row(
                    contract.customer.first_name,
                    contract.customer.last_name,
                    contract.customer.user.username,
                    contract.user.full_name,
                    "Yes" if contract.is_signed else "No",
                    "{:.2f}".format(contract.remaining_amount),
                    str(contract.creation_date),
                )
            table.column_widths = "auto"
            self.console.print(table)
            self.wait_for_key_press()

    def input_list_contracts_filters(self):
        """
        Displays the list contracts filters menu and handles user input for selecting a filter.

        This method presents the user with a menu of list contracts filters options, including no filters, contracts not signed, and contracts not totally paid. The user is prompted to select a filter
        by entering a number corresponding to the desired option. The method validates the user's input and
        returns the selected filter.

        Returns:
            int: The number corresponding to the selected filter.
        """
        self.console.print(
            Panel("--   List contracts Filters   --", expand=True),
            style="menu_text",
        )

        self.console.print(
            "[menu_choice]"
            + constantes.MANAGER_LIST_CONTRACT_NO_FILTER
            + " - No filters[/]"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.MANAGER_LIST_CONTRACT_NOT_SIGNED
            + " - contracts not signed[/]"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.MANAGER_LIST_CONTRACT_NOT_TOTAL_PAID
            + " - contracts not totally paid[/]"
        )
        list_contract_filter = ""
        while list_contract_filter == "":
            try:
                list_contract_filter = int(input())
                if list_contract_filter < 1 or list_contract_filter > 3:
                    list_contract_filter = ""
                    self.console.print("[error]BAD MENU INPUT[/]")
                    continue
                continue
            except ValueError:
                self.console.print("[error]BAD MENU INPUT[/]")
                list_contract_filter = ""
                continue
        return str(list_contract_filter)

    def display_new_contract_validation(self):
        """
        Displays a success message indicating that a new contract has been created.
        """
        self.console.print("[success]Contract successfully created[/]")
        self.wait_for_key_press()

    def display_update_contract_validation(self):
        """
        Displays a success message indicating that a contract has been updated.
        """
        self.console.print("[success]Contract successfully updated[/]")
        self.wait_for_key_press()

    def display_no_contract_found(self):
        """
        Displays an error message indicating that no contract was found.
        """
        self.console.print("[error]No contract found[/]")
        return self.wait_for_key_press()

    def display_new_contract(self):
        """
        Displays a panel indicating that a new contract is being created.
        """
        self.console.print(
            Panel("---   New Contract management   ---", expand=True),
            style="menu_text",
        )

    def display_error(self, message):
        """
        Displays an error message.
        """
        self.console.print(f"[error] {message} [/]")
