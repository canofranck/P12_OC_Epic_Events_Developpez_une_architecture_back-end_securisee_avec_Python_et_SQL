import models
import views
from datetime import datetime
from sqlalchemy import and_
import constantes


class ContractController:
    def __init__(self, session, view: views.ContractView, user=None):
        self.session = session
        self.view = view
        self.user = user

    def manage_contracts(self, customer: models.Customer):
        contract_to_manage = self.get_contract(customer)
        if contract_to_manage is not None:
            self.view.display_contract_informations(contract_to_manage)

        menu_selection = self.view.input_contract_management()
        match menu_selection:
            case 0:
                return
            case 1:
                return self.create_contract(customer)
            case 2:
                return self.update_contract(customer)
            case _:
                print("BAD MENU INPUT")

    def create_contract(self, customer: models.Customer):
        input_new_contract = self.view.input_new_contract()
        contract = models.Contract(
            customer=customer,
            user=customer.user,
            total_amount=input_new_contract["total_amount"],
            remaining_amount=input_new_contract["total_amount"],
            is_signed=input_new_contract["is_signed"],
        )
        try:
            self.session.add(contract)
            self.session.commit()
            return self.view.display_new_contract_validation()
        except Exception as err:
            self.session.rollback()
            print("error", err)

    def update_contract(self, customer: models.Customer):
        try:
            contract_to_manage = self.get_contract(customer)
            self.view.display_contract_informations(contract_to_manage)

            if (
                contract_to_manage.is_signed
                and contract_to_manage.remaining_amount == 0
            ):
                return print("CONTRACT UPDATE ERROR")

            if not contract_to_manage.is_signed:
                contract_to_manage.is_signed = (
                    self.view.input_contract_signed()
                )

            if contract_to_manage.remaining_amount > 0:
                contract_to_manage.remaining_amount = (
                    self.view.input_contract_remaining_amount(
                        contract_to_manage.remaining_amount,
                        contract_to_manage.total_amount,
                    )
                )
            contract_to_manage.creation_date = datetime.now()
            self.session.commit()
            return self.view.display_update_contract_validation()
        except ValueError as err:
            print("error", err)
        except Exception as err:
            self.session.rollback()
            print("error", err)

    def get_contract(self, customer: models.Customer) -> models.Contract:
        contract = (
            self.session.query(models.Contract)
            .filter_by(customer=customer)
            .first()
        )
        if contract is None:
            self.view.display_no_contract_found()
        return contract

    def list_contracts(self):
        filters_input = self.view.input_list_contracts_filters()
        filters = []
        if filters_input == constantes.MANAGER_LIST_CONTRACT_NOT_SIGNED:
            filters.append(models.Contract.is_signed == False)
        if filters_input == constantes.MANAGER_LIST_CONTRACT_NOT_TOTAL_PAID:
            filters.append(models.Contract.remaining_amount > 0)

        contracts = (
            self.session.query(models.Contract).filter(and_(*filters)).all()
        )

        for contract in contracts:
            self.view.display_contract_informations(contract)
