import models
import views
import constantes


class ContractView:
    def input_contract_management(self):
        print(constantes.LOG_OUT, "- Exit")
        print(
            constantes.MANAGER_CREATE_NEW_CONTRACT, "- Create a new Contract"
        )
        print(constantes.MANAGER_UPDATE_CONTRACT, "- Update a Contract")
        selection = -1
        while selection < 0 or selection > 2:
            try:

                selection = int(input("Select an action : "))
                if selection > 2 or selection < 0:
                    raise ValueError
            except ValueError:
                print("bad input")
        return selection

    def input_contract_amount(self):

        return input("Total amount : ")

    def input_contract_remaining_amount(self, remaining_amount, total_amount):
        print(f"remaining on bill: {remaining_amount}")

        new_remaining_amount = ""
        while new_remaining_amount == "":
            try:
                new_remaining_amount = int(
                    input("Insert the new amount remaining to be paid : ")
                )
                if new_remaining_amount > total_amount:
                    print("ERROR_REMAINING AMOUNT_TO_BIG")
                    new_remaining_amount = ""
                    continue
                continue
            except ValueError:
                print("bad input")
                continue
        return new_remaining_amount

    def input_contract_signed(self):

        int_signed = -1
        while int_signed == -1:
            user_input = input(
                "Contract already signed ? (0  for NO / 1 for YES) : "
            )
            if user_input != "0" and user_input != "1":
                print("bad input")
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
        return print(
            f"Customer : \n"
            f"First name : {contract.customer.first_name} \n "
            f"Last name  : {contract.customer.last_name} \n"
            f"Contact : \n"
            f"Username  : {contract.user.username}\n "
            f"Fullname  : {contract.user.full_name} \n"
            f"Is signed : {contract.is_signed} \n"
            f"Remaining amount : {contract.remaining_amount} \n"
            f"Created date     : {contract.creation_date} \n"
        )

    def input_list_contracts_filters(self):
        print("-- List contracts Filters --")
        print(constantes.MANAGER_LIST_CONTRACT_NO_FILTER, " - No filters")
        print(
            constantes.MANAGER_LIST_CONTRACT_NOT_SIGNED,
            " - contracts not signed",
        )
        print(
            constantes.MANAGER_LIST_CONTRACT_NOT_TOTAL_PAID,
            " - contracts not totally paid",
        )
        list_contract_filter = ""
        while list_contract_filter == "":
            try:
                list_contract_filter = int(input())
                if list_contract_filter < 1 or list_contract_filter > 3:
                    list_contract_filter = ""
                    print("BAD MENU INPUT")
                    continue
                continue
            except ValueError:
                print("BAD MENU INPUT")
                continue
        return list_contract_filter

    def display_new_contract_validation(self):
        return print("Contract successfully created")

    def display_update_contract_validation(self):
        return print("Contract successfully updated")
