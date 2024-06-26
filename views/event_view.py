import constantes
import models
import views
from rich.panel import Panel


class EventView(views.BaseView):

    def display_event(self, event: models.Event):
        self.console.print(
            f"[menu_text]Event Name       :[/] {event.event_name} \n"
            f"[menu_text]Customer Name    :[/] {event.customer_name} \n"
            f"[menu_text]Customer Contact :[/] {event.customer_contact} \n"
            f"[menu_text]Start Date       :[/] {event.start_date} \n"
            f"[menu_text]End Date         :[/] {event.end_date} \n"
            f"[menu_text]Location         :[/] {event.location} \n"
            f"[menu_text]Number attendees :[/] {event.nb_attendees} \n"
            f"[menu_text]Notes            :[/] {event.notes} \n"
        )
        if event.user is not None:
            self.console.print(f"[menu_text]Support :[/] {event.user.email}")

        if event.customer_name is not None:
            self.console.print(
                f"[menu_text]Customer :[/] {event.customer_name} \n"
            )

    def display_new_event_panel(self):
        self.console.print(
            Panel("---   New Event management   ---", expand=True),
            style="menu_text",
        )

    def input_event_start_date(self):
        self.console.print("Event start date: (DD-MM-YY)", style="input")
        return input()

    def input_event_end_date(self):
        self.console.print("Event end date: (DD-MM-YY)", style="input")

        return input()

    def input_event_name(self):
        self.console.print("Event name : ", style="input")

        return input()

    def input_event_location(self):
        self.console.print("Event location : ", style="input")

        return input()

    def input_event_nb_attendees(self):
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
        self.console.print("Add a note (max 200 characters) : ", style="input")
        return input()

    def input_new_event(self):
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
        self.console.print(
            Panel(" -- List Events Filters --", expand=True), style="menu_text"
        )
        self.console.print(
            "[menu_choice]" + constantes.LIST_EVENTS + " - No filters [/]"
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
                if list_event_filter < 0 or list_event_filter > 2:
                    list_event_filter = ""
                    self.console.print("[error]bad input[/]")
                    continue
                continue
            except ValueError:
                self.console.print("[error]ENTER AN ENTIRE VALUE[/]")
                continue
        return list_event_filter

    def display_new_event_validation(self):
        self.console.print("[success]New event created[/]")
        self.wait_for_key_press()

    def display_update_event_validation(self):
        self.console.print("[success]Event correctly updated[/]")
        self.wait_for_key_press()

    def input_list_events_filters(self):
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
        self.console.print(
            "[error]The contract hasn't been signed, so it's impossible to create an event.[/]"
        )
        self.wait_for_key_press()
