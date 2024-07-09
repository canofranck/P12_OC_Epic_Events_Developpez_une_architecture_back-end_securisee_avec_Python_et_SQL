import constantes
import models
import views
from rich.panel import Panel
from rich.table import Table


class EventView(views.BaseView):
    """
    The EventView class is responsible for managing the event-related views in the application.

    Methods:
        input_event_notes(self):
            Prompts the user to input notes for the event.

        display_event(self, event: models.Event):
            Displays the details of an event.

        display_new_event_panel(self):
            Displays a panel with the title "New Event management".

        input_event_start_date(self):
            Prompts the user to input the start date of the event.

        input_event_end_date(self):
            Prompts the user to input the end date of the event.

        input_event_name(self):
            Prompts the user to input the name of the event.

        input_event_location(self):
            Prompts the user to input the location of the event.

        input_event_nb_attendees(self):
            Prompts the user to input the number of attendees for the event.

        input_event_notes(self):
            Prompts the user to input notes for the event.

        input_new_event(self):
            Prompts the user to input the details of a new event.

        input_list_events_filters(self):
            Prompts the user to select a filter for the list of events.

        display_new_event_validation(self):
            Displays a success message indicating that a new event has been created.

        display_update_event_validation(self):
            Displays a success message indicating that an event has been updated.

        display_contract_not_signed(self):
            Displays an error message indicating that a contract hasn't been signed, so it's impossible to create an event.

        display_support_manage_events(self):
            Displays a panel with the title "Support Events management".
    """

    def input_event_notes(self):
        """
        Prompts the user to input notes for the event.

        This method displays a message asking the user to input notes for the event. The user's input
        is returned as a string.

        Returns:
            str: The notes for the event.
        """
        self.console.print("Event notes : ", style="input")
        return input()

    def display_event(self, events: models.Event, table):
        """
        Displays the details of an event.

        This method displays a table with the details of the given event, including the event name, event ID,
        contract ID, customer name, sales contact, event start date, event end date, event location, number of attendees,
        event notes, and support contact.

        Args:
            event (models.Event): The event object containing the details to be displayed.
        """

        table.column_widths = "auto"
        self.console.print(table)

    def display_new_event_panel(self):
        """
        Displays a panel with the title "New Event management".
        """
        self.console.print(
            Panel("---   New Event management   ---", expand=True),
            style="menu_text",
        )

    def input_event_start_date(self):
        """
        Prompts the user to input the start date of the event.

        Returns:
            str: The start date of the event in the format "DD-MM-YY".
        """
        self.console.print("Event start date: (DD-MM-YY)", style="input")
        return input()

    def input_event_end_date(self):
        """
        Prompts the user to input the end date of the event.

        Returns:
            str: The end date of the event in the format "DD-MM-YY".
        """
        self.console.print("Event end date: (DD-MM-YY)", style="input")
        return input()

    def input_event_name(self):
        """
        Prompts the user to input the name of the event.

        Returns:
            str: The name of the event.
        """
        self.console.print("Event name : ", style="input")

        return input()

    def input_event_location(self):
        """
        Prompts the user to input the location of the event.

        Returns:
            str: The location of the event.
        """
        self.console.print("Event location : ", style="input")

        return input()

    def input_event_nb_attendees(self):
        """
        Prompts the user to input the number of attendees for the event.

        Returns:
            int: The number of attendees for the event.
        """
        self.console.print("Event attendees : ", style="input")

        nb_attendees = 0
        while nb_attendees == 0:
            try:
                nb_attendees = int(input())
                if nb_attendees < 0:
                    nb_attendees = 0
                    print("ENTER A POSITIVE VALUE")
                    continue
            except ValueError:
                print("ENTER A ENTIRE VALUE")
                continue

        return nb_attendees

    def input_event_notes(self):
        """
        Prompts the user to input notes for the event.

        Returns:
            str: The notes for the event.
        """
        self.console.print("Add a note (max 200 characters) : ", style="input")
        return input()

    def input_new_event(self):
        """
        Prompts the user to input the details of a new event.

        Returns:
            dict: A dictionary containing the details of the new event.
        """
        event_name = self.input_event_name()
        event_location = self.input_event_location()
        event_attendees = self.input_event_nb_attendees()
        event_notes = self.input_event_notes()
        return {
            "name": event_name,
            "location": event_location,
            "attendees": event_attendees,
            "notes": event_notes,
        }

    def input_list_events_filters(self):
        """
        Prompts the user to select a filter for the list of events.

        Returns:
            int: The selected filter option.
        """
        self.console.print(
            Panel(" -- List Events Filters --", expand=True), style="menu_text"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.SALES_LIST_EVENT_NO_FILTER
            + " - No filters [/]"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.SALES_LIST_EVENT_ONLY_YOURS
            + " - Only the events you manage [/]"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.SALES_LIST_EVENT_NO_SUPPORT
            + " - Display events that have no support [/]"
        )

        list_event_filter = ""
        while list_event_filter == "":
            try:
                list_event_filter = int(input())
                if list_event_filter < 0 or list_event_filter > 3:
                    list_event_filter = ""
                    self.console.print("[error]bad input[/]")
                    continue
                continue
            except ValueError:
                self.console.print("[error]ENTER AN ENTIRE VALUE[/]")
                continue
        return list_event_filter

    def display_new_event_validation(self):
        """
        Displays a success message indicating that a new event has been created.
        """
        self.console.print("[success]New event created[/]")
        self.wait_for_key_press()

    def display_update_event_validation(self):
        """
        Displays a success message indicating that an event has been updated.
        """
        self.console.print("[success]Event correctly updated[/]")
        self.wait_for_key_press()

    def input_list_events_filters(self):
        """
        Prompts the user to select a filter for the list of events.

        Returns:
            int: The selected filter option.
        """
        self.console.print(
            Panel("-- List Events Filters --", expand=True), style="menu_text"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.EVENT_FILTER_NO_FILTER
            + " - No filters [/]"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.EVENT_FILTER_ONLY_YOURS
            + " - Only the events you manage [/]"
        )
        self.console.print(
            "[menu_choice]"
            + constantes.EVENT_FILTER_NO_SUPPORT
            + " - Display events that have no support [/]"
        )
        list_event_filter = ""
        while list_event_filter == "":
            try:
                list_event_filter = int(input())
                if list_event_filter < 1 or list_event_filter > 3:
                    list_event_filter = ""
                    self.console.print("[error]error MENU INPUT[/]")
                    continue
                continue
            except ValueError:
                self.console.print("[error]error  ERR NOT DIGIT VALUE[/]")
                continue
        return list_event_filter

    def display_contract_not_signed(self):
        """
        Displays an error message indicating that a contract hasn't been signed, so it's impossible to create an event.
        """
        self.console.print(
            "[error]The contract hasn't been signed, so it's impossible to create an event.[/]"
        )
        self.wait_for_key_press()

    def display_support_manage_events(self):
        """
        Displays a panel with the title "Support Events management".
        """
        self.console.print(
            Panel("---   Support Events management   ---", expand=True),
            style="menu_text",
        )

    def display_no_events_found(self):
        """
        Displays a message indicating that no events were found.
        """
        self.console.print("[error]No events found.[/]")
        self.wait_for_key_press()

    def display_error(self, message):
        """
        Displays an error message.
        """
        self.console.print(f"[error] {message} [/]")
