from sqlalchemy import and_, or_
import models
import views
from datetime import datetime
import validators
from rich.table import Table
import logging
import constantes

logger = logging.getLogger(__name__)


class EventController:
    """
    The EventController class is responsible for managing events within the application.

    Attributes:
        session: The database session used for database operations.
        view: The view associated with event operations.
        user: The currently logged-in user.

    Methods:
        __init__(self, session, view, user=None):
            Initializes the EventController with the given parameters.

        create_event(self, customer, contract):
            Creates a new event for a given customer and contract.

        update_event(self, support_user=None, assigned_support=None):
            Updates an existing event with new information or assigns a support user.

        get_event(self, assigned_support):
            Retrieves the event associated with the given support user.

        set_new_event(self):
            Sets the start and end dates for a new event.

        list_events(self):
            Lists all events in the database.

        sales_manager_events(self, support_user=None, assigned_support=None):
            Displays the events managed by the sales manager.
    """

    def __init__(self, session, view: views.EventView, user=None):
        """
        Initializes the EventController with the given parameters.

        Args:
            session: The database session used for database operations.
            view: The view associated with event operations.
            user: The currently logged-in user (default is None).
        """
        self.session = session
        self.view = view
        self.user = user

    def create_event(
        self, customer: models.Customer, contract: models.Contract
    ):
        """
        Creates a new event for a given customer and contract.

        Args:
            customer: The customer associated with the event.
            contract: The contract associated with the event.

        Returns:
            A message indicating the success or failure of the event creation.
        """
        # Vérifier si le contrat est signé
        if not contract.is_signed:
            return self.view.display_contract_not_signed()

        self.view.display_new_event_panel()
        start_date, end_date = self.set_new_event()

        new_event = models.Event(
            event_name=self.view.input_event_name(),
            customer_name=customer.compagny_name,
            customer_contact=customer.user.full_name,
            start_date=start_date,
            end_date=end_date,
            location=self.view.input_event_location(),
            nb_attendees=self.view.input_event_nb_attendees(),
            notes=self.view.input_event_notes(),
            contract=contract,
        )

        try:
            self.session.add(new_event)
            self.session.commit()
            return self.view.display_new_event_validation()
        except Exception as err:
            self.session.rollback()
            self.view.display_error(f"Error Exception : {err}")
            logger.info("Error Exception " + str(err))
            return

    def update_event(self, support_user=None, assigned_support=None):
        """
        Updates an existing event with new information or assigns a support user.

        Args:
            support_user: The support user to assign to the event (default is None).
            assigned_support: The support user currently assigned to the event (default is None).

        Returns:
            A message indicating the success or failure of the event update.
        """
        if support_user is not None and assigned_support is not None:
            return self.view.display_error(
                constantes.EVENT_CONTROLLER_SUPPORT_ALREADY_DEFINE
            )

        try:
            event_to_update = self.get_event(assigned_support)
            if event_to_update is None:
                return
            if support_user is not None:
                event_to_update.user = support_user
            else:
                start_date, end_date = self.set_new_event()
                event_to_update.location = self.view.input_event_location()
                event_to_update.nb_attendees = (
                    self.view.input_event_nb_attendees()
                )
                event_to_update.notes = self.view.input_event_notes()
                event_to_update.start_date = start_date
                event_to_update.end_date = end_date

            self.session.commit()
            table = Table(title="Liste des events")
            table.add_column("Event Name")
            table.add_column("Event ID")
            table.add_column("Contract ID")
            table.add_column("Customer Name")
            table.add_column("Sales Contact")
            table.add_column("Event Start Date")
            table.add_column("Event End Date")
            table.add_column("Event Location")
            table.add_column("Number of attendees")
            table.add_column("Event Notes")
            table.add_column("Support")
            support_email = (
                event_to_update.user.email if event_to_update.user else ""
            )
            manager_id = (
                self.session.query(models.Contract.manager_id)
                .filter(models.Contract.id == event_to_update.contract_id)
                .scalar()
            )
            sales_contact_name = (
                self.session.query(models.User.full_name)
                .filter(models.User.id == manager_id)
                .scalar()
                if manager_id
                else ""
            )
            table.add_row(
                str(event_to_update.event_name),
                str(event_to_update.id),
                str(event_to_update.contract_id),
                str(event_to_update.customer_name),
                str(sales_contact_name),
                str(event_to_update.start_date),
                str(event_to_update.end_date),
                str(event_to_update.location),
                str(event_to_update.nb_attendees),
                str(event_to_update.notes),
                str(support_email),
            )
            self.view.display_event(event_to_update, table)
            return self.view.display_update_event_validation()
        except ValueError as err:
            self.view.display_error(f"ValueError : {err}")
            logger.info("ValueError " + str(err))

    def set_new_event(self):
        """
        Sets the start and end dates for a new event.

        Returns:
            start_date: The start date of the event.
            end_date: The end date of the event.
        """
        start_date = None
        end_date = None
        while start_date is None and end_date is None:
            try:
                start_date = self.set_new_event_date(is_start_date=True)
                end_date = self.set_new_event_date(is_start_date=False)
                validators.validate_date(start_date, end_date)
                continue
            except ValueError as err:
                self.view.display_error(f"ValueError : {err}")
                logger.info("ValueError " + str(err))
                start_date = None
                end_date = None
                continue
        return start_date, end_date

    def set_new_event_date(self, is_start_date):
        """
        Sets the start or end date for a new event.

        Args:
            is_start_date: A boolean indicating whether to set the start date (True) or end date (False).

        Returns:
            new_date: The start or end date of the event.
        """
        date_format = "%d-%m-%y"
        new_date = ""
        while new_date == "":
            if is_start_date:
                new_date_input = self.view.input_event_start_date()
            else:
                new_date_input = self.view.input_event_end_date()
            try:
                new_date = datetime.strptime(new_date_input, date_format)
                continue
            except ValueError as err:
                self.view.display_error(f"Format invalide")
                logger.info("ValueError : " + str(err))
                continue
        return new_date

    def get_event(self, assigned_support: models.User = None) -> models.Event:
        """
        Retrieves the event associated with the given support user.

        Args:
            assigned_support: The support user currently assigned to the event (default is None).

        Returns:
            event: The event associated with the given support user.
        """
        event_name = self.view.input_event_name()
        filters = {"event_name": event_name}
        if assigned_support is not None:
            filters["user"] = assigned_support
        event = self.session.query(models.Event).filter_by(**filters).first()
        if event is None:
            self.view.display_error(
                constantes.EVENT_CONTROLLER_EVENT_NOT_FOUND
            )
            return
        return event

    def list_events(self):
        """
        Lists all events in the database.

        Returns:
            None
        """
        event_filters_input = self.view.input_list_events_filters()
        filters = []
        if event_filters_input == 1:

            filters = []
        elif event_filters_input == 2:
            filters.append(
                or_(
                    models.Event.contract.has(manager_id=self.user.id),
                    models.Event.support_id == self.user.id,
                )
            )
        elif event_filters_input == 3:
            filters.append(
                models.Event.support_id == None,
            )

        if filters:
            events = self.session.query(models.Event).filter(*filters).all()
        else:
            events = self.session.query(models.Event).all()

        if len(events) == 0:
            return self.view.display_no_events_found()
        table = Table(title="Liste des events")
        table.add_column("Event Name")
        table.add_column("Event ID")
        table.add_column("Contract ID")
        table.add_column("Customer Name")
        table.add_column("Sales Contact")
        table.add_column("Event Start Date")
        table.add_column("Event End Date")
        table.add_column("Event Location")
        table.add_column("Number of attendees")
        table.add_column("Event Notes")
        table.add_column("Support")
        for event_item in events:

            support_email = event_item.user.email if event_item.user else ""
            manager_id = (
                self.session.query(models.Contract.manager_id)
                .filter(models.Contract.id == event_item.contract_id)
                .scalar()
            )
            sales_contact_name = (
                self.session.query(models.User.full_name)
                .filter(models.User.id == manager_id)
                .scalar()
                if manager_id
                else ""
            )
            table.add_row(
                event_item.event_name,
                str(event_item.id),
                str(event_item.contract_id),
                event_item.customer_name,
                sales_contact_name,
                str(event_item.start_date),
                str(event_item.end_date),
                event_item.location,
                str(event_item.nb_attendees),
                event_item.notes,
                support_email,
            )
        self.view.display_event(events, table)
        views.BaseView.wait_for_key_press(self)

    def sales_manager_events(self, support_user=None, assigned_support=None):
        """
        Displays the events managed by the sales manager.

        Args:
            support_user: The support user to assign to the event (default is None).
            assigned_support: The support user currently assigned to the event (default is None).

        Returns:
            None
        """
        views.MainView.clear_screen(self)
        self.view.display_support_manage_events()
        self.update_event(
            support_user=None,
            assigned_support=self.user,
        )

    def delete_event(self):
        """
        Deletes an existing customer from the system.

        This method displays the delete event menu and handles the event's selection.
        Depending on the event's choice, it either deletes the event or returns to the previous menu.

        Returns:
            None
        """
        self.view.display_delete_event()
        try:
            event = self.get_event()
            self.session.delete(event)
            self.session.commit()
            self.view.display_delete_event_validation()
            if event:
                logger.info("Delete event : " + event.event_name + " success")
            return
        except ValueError:
            self.view.display_new_event_error()
            if event:
                logger.info("Delete event : " + event.event_name + " failed")
            return
