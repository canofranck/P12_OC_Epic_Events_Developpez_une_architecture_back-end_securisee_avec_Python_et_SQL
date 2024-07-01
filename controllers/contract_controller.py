import models
import views
from datetime import datetime
from sqlalchemy import and_
import constantes
from rich.table import Table


class ContractController:
    """
    The ContractController class is responsible for managing contracts within the application.

    Attributes:
        session: The database session used for database operations.
        view: The view associated with contract operations.
        user: The currently logged-in user.

    Methods:
        __init__(self, session, view, user=None):
            Initializes the ContractController with the given parameters.

        manage_contracts(self, customer):
            Manages contracts for a given customer, displaying contract information and handling user input.

        create_contract(self, customer):
            Creates a new contract for a given customer.

        update_contract(self, customer):
            Updates an existing contract for a given customer.

        get_contract(self, customer):
            Retrieves the contract associated with a given customer.

        list_contracts(self):
            Lists all contracts in the database.
    """

    def __init__(self, session, view: views.ContractView, user=None):
        """
        Initializes the ContractController with the given parameters.

        Args:
            session: The database session used for database operations.
            view: The view associated with contract operations.
            user: The currently logged-in user (default is None).
        """
        self.session = session
        self.view = view
        self.user = user

    def manage_contracts(self, customer: models.Customer):
        """
        Manages contracts for a given customer, displaying contract information and handling user input.

        Args:
            customer (models.Customer): The customer for whom the contracts are being managed.

        Returns:
            None
        """
        contract_to_manage = self.get_contract(customer)
        if contract_to_manage is not None:
            table = Table(title="Liste Contrat")
            table.add_column(
                "First name:", justify="left", style="input", no_wrap=True
            )
            table.add_column(
                "Last name:", justify="left", style="input", no_wrap=True
            )
            table.add_column(
                "Contact:", justify="left", style="input", no_wrap=True
            )
            table.add_column(
                "Username:", justify="left", style="input", no_wrap=True
            )
            table.add_column(
                "Fullname:", justify="left", style="input", no_wrap=True
            )
            table.add_column(
                "Is signed:", justify="left", style="input", no_wrap=True
            )
            table.add_column(
                "Remaining amount:",
                justify="left",
                style="input",
                no_wrap=True,
            )
            table.add_column(
                "Creation date:", justify="left", style="input", no_wrap=True
            )
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
        """
        Creates a new contract for the given customer.

        This method prompts the user to input the details of the new contract,
        creates a new contract object, and saves it to the database. If an error
        occurs during the process, the transaction is rolled back and an error
        message is displayed.

        Args:
            customer (models.Customer): The customer for whom the contract is being created.

        Returns:
            None
        """
        self.view.display_new_contract()
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
        """
        Updates an existing contract for the given customer.

        This method retrieves the contract associated with the given customer,
        displays its information, and allows the user to update its details.
        If the contract is already signed and fully paid, a message is displayed
        indicating that no further updates are needed. Otherwise, the user can
        update the contract's signed status and remaining amount. The contract's
        creation date is also updated to the current date and time. If an error
        occurs during the process, the transaction is rolled back and an error
        message is displayed.

        Args:
            customer (models.Customer): The customer whose contract is being updated.

        Returns:
            None
        """

        try:
            contract_to_manage = self.get_contract(customer)
            self.view.display_contract_informations(contract_to_manage)

            if (
                contract_to_manage.is_signed
                and contract_to_manage.remaining_amount == 0
            ):
                return print("CONTRACT ALREADY SIGNED AND PAID")

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
        """
        Retrieves the contract associated with the given customer.

        This method queries the database to find the contract that belongs to the specified customer.
        If no contract is found, a message is displayed indicating that no contract was found.

        Args:
            customer (models.Customer): The customer whose contract is being retrieved.

        Returns:
            models.Contract: The contract associated with the given customer, or None if no contract is found.
        """
        contract = (
            self.session.query(models.Contract)
            .filter_by(customer=customer)
            .first()
        )
        if contract is None:
            self.view.display_no_contract_found()
        return contract

    def list_contracts(self):
        """
        Lists contracts based on user-selected filters.

        This method allows the user to list contracts by applying various filters.
        The available filters include listing contracts that are not signed,
        contracts that are not fully paid, or listing all contracts without any filters.
        The method retrieves the contracts from the database based on the selected filters
        and displays the contract information.

        Returns:
            None
        """
        filters_input = self.view.input_list_contracts_filters()
        filters = []
        if filters_input == constantes.MANAGER_LIST_CONTRACT_NOT_SIGNED:
            filters.append(models.Contract.is_signed.is_(False))
        elif filters_input == constantes.MANAGER_LIST_CONTRACT_NOT_TOTAL_PAID:
            filters.append(models.Contract.remaining_amount > 0)
        elif filters_input == constantes.MANAGER_LIST_CONTRACT_NO_FILTER:
            filters = []

        if filters:
            contracts = (
                self.session.query(models.Contract)
                .filter(and_(*filters))
                .all()
            )
        else:
            contracts = self.session.query(models.Contract).all()

        for contract in contracts:
            self.view.display_contract_informations(contract)
