from sqlalchemy import and_, or_
import models
import views
from datetime import datetime
import validators
from rich.table import Table


class EventController:
    def __init__(self, session, view: views.EventView, user=None):
        self.session = session
        self.view = view
        self.user = user

    def create_event(
        self, customer: models.Customer, contract: models.Contract
    ):
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
            return print("error", err)

    def update_event(self, support_user=None, assigned_support=None):

        if support_user is not None and assigned_support is not None:
            return print("A USER SUPPORT IS ALREADY DEFINE")

        try:
            event_to_update = self.get_event(assigned_support)
            self.view.display_event(event_to_update)
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
            return self.view.display_update_event_validation()
        except ValueError as err:
            print("error", err)

    def set_new_event(self):
        start_date = None
        end_date = None
        while start_date is None and end_date is None:
            try:
                start_date = self.set_new_event_date(is_start_date=True)
                end_date = self.set_new_event_date(is_start_date=False)
                validators.validate_date(start_date, end_date)
                continue
            except ValueError as err:
                print("error", err)
                start_date = None
                end_date = None
                continue
        return start_date, end_date

    def set_new_event_date(self, is_start_date):
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
                print("error", err)
                continue
        return new_date

    def get_event(self, assigned_support: models.User = None) -> models.Event:
        event_name = self.view.input_event_name()
        filters = {"event_name": event_name}
        if assigned_support is not None:
            filters["user"] = assigned_support
        event = self.session.query(models.Event).filter_by(**filters).first()
        if event is None:
            raise ValueError("EVENT_NOT_FOUND")
        return event

    def list_events(self):
        event_filters_input = self.view.input_list_events_filters()
        filters = []
        if event_filters_input == 1:

            filters.append(True)
        elif event_filters_input == 2:
            # Filtrer les évents de l user
            filters.append(
                or_(
                    models.Event.contract.has(manager_id=self.user.id),
                    models.Event.support_id == self.user.id,
                )
            )
        elif event_filters_input == 3:
            # Filtrer les événements que l'utilisateur gère et les événements sans support
            filters.append(
                or_(
                    models.Event.support_id == self.user.id,
                    models.Event.support_id == None,
                )
            )

        if filters:
            events = self.session.query(models.Event).filter(*filters).all()
        else:
            # Si aucun filtre n'est sélectionné, afficher tous les événements
            events = self.session.query(models.Event).all()

        for event in events:
            table = Table(title=f"Liste des events")
            table.add_column(
                "Champ", justify="left", style="cyan", no_wrap=True
            )
            table.add_column(
                "Valeur", justify="left", style="cyan", no_wrap=True
            )
            table.add_row("Event Name ", f"{event.event_name}")
            table.add_row("Customer Name", f"{event.customer_name}")
            table.add_row("Customer Contact", f"{event.customer_contact}")
            table.add_row("Date de début", f"{event.start_date}")
            table.add_row("End Date", f"{event.end_date}")
            table.add_row("Location", f"{event.location}")
            table.add_row("Number of attendees", f"{event.nb_attendees}")
            table.add_row("Notes", f"{event.notes}")
            self.view.display_event(event)

    def sales_manager_events(self, support_user=None, assigned_support=None):
        views.MainView.clear_screen(self)
        self.view.display_support_manage_events()
        self.update_event(
            support_user=None,
            assigned_support=self.user,
        )
