import constantes
import models
import views


class EventView:

    def display_event(self, event: models.Event):
        print(
            f"Event Name       : {event.name} \n"
            f"Customer Name    : {event.customer_name} \n"
            f"Customer Contact : {event.customer_contact} \n"
            f"Start Date       : {event.start_date} \n"
            f"End Date         : {event.end_date} \n"
            f"Location         : {event.location} \n"
            f"Number attendees : {event.attendees} \n"
            f"Notes            : {event.notes} \n"
        )
        if event.user is not None:
            print(f"Support : {event.user.email}")

        if event.customer_name is not None:
            print(f"Customer : {event.customer_name} \n")
        print("--------------- \n")

    def display_new_event_panel(self):
        return print("--- New Event management ---")

    def input_event_start_date(self):

        return input("Event start date: (DD-MM-YY) ")

    def input_event_end_date(self):

        return input("Event end date: (DD-MM-YY) ")

    def input_event_name(self):

        return input("Event name : ")

    def input_event_location(self):

        return input("Event location : ")

    def input_event_nb_attendees(self):

        attendees = 0
        while attendees == 0:
            try:
                attendees = int(input("Event attendees : "))
                if attendees < 0:
                    attendees = 0
                    print("ENTER A POSITIVE VALUE")
                    continue
            except ValueError:
                print("ENTER A ENTIRE VALUE")
                continue
        return attendees

    def input_event_notes(self):

        return input("Add a note (max 200 characters) : ")

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
        print(" -- List Events Filters --")
        print(constantes.LIST_EVENTS, " - No filters")
        print(
            constantes.SALES_LIST_EVENT_ONLY_YOURS,
            " - Only the events you manage",
        )
        print(
            constantes.SALES_LIST_EVENT_NO_SUPPORT,
            " - Display events that have no support",
        )
        list_event_filter = ""
        while list_event_filter == "":
            try:
                list_event_filter = int(input())
                if list_event_filter < 0 or list_event_filter > 2:
                    list_event_filter = ""
                    print("bad input")
                    continue
                continue
            except ValueError:
                print("ENTER AN ENTIRE VALUE")
                continue
        return list_event_filter

    def display_new_event_validation(self):
        return print("New event created")

    def display_update_event_validation(self):
        return print("Event correctly updated")
