import models
import views
import constantes
from rich.panel import Panel


class ContractView(views.BaseView):
    def input_contract_management(self):
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
        self.console.print("Total amount : ", style="input")
        return input()

    def input_contract_remaining_amount(self, remaining_amount, total_amount):
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
        total_amount_input = self.input_contract_amount()
        is_signed_input = self.input_contract_signed()
        return {
            "total_amount": total_amount_input,
            "is_signed": is_signed_input,
        }

    def display_contract_informations(self, contract: models.Contract):
        return self.console.print(
            f"[menu_text]First name :[/] {contract.customer.first_name} \n"
            f"[menu_text]Last name  :[/] {contract.customer.last_name} \n"
            f"[menu_text]Contact : [/]\n"
            f"[menu_text]Username  :[/] {contract.user.username} \n"
            f"[menu_text]Fullname  :[/] {contract.user.full_name} \n"
            f"[menu_text]Is signed :[/] {contract.is_signed} \n"
            f"[menu_text]Remaining amount :[/] {contract.remaining_amount} \n"
            f"[menu_text]Created date     :[/] {contract.creation_date} \n"
        )

    def input_list_contracts_filters(self):
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
                continue
        return list_contract_filter

    def display_new_contract_validation(self):
        self.console.print("[success]Contract successfully created[/]")
        self.wait_for_key_press()

    def display_update_contract_validation(self):
        self.console.print("[success]Contract successfully updated[/]")
        self.wait_for_key_press()

    def display_no_contract_found(self):
        return self.console.print("[error]No contract found[/]")
