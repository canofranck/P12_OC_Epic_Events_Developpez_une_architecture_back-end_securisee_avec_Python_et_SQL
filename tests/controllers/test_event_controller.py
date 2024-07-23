import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from sqlalchemy.orm import Session
import models
import views
import constantes
from controllers import EventController


class TestEventController(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.view = MagicMock(spec=views.EventView)
        self.user = MagicMock(spec=models.User)
        self.controller = EventController(self.session, self.view, self.user)

    @patch("models.Contract")
    @patch("models.Customer")
    @patch("models.Event")
    def test_create_event(self, MockEvent, MockCustomer, MockContract):
        customer = MockCustomer()
        contract = MockContract()
        contract.is_signed = True

        self.view.input_event_name.return_value = "Event Test"
        self.view.input_event_location.return_value = "Test Location"
        self.view.input_event_nb_attendees.return_value = 100
        self.view.input_event_notes.return_value = "Test Notes"
        self.controller.set_new_event = MagicMock(
            return_value=(datetime(2023, 7, 22), datetime(2023, 7, 23))
        )

        self.controller.create_event(customer, contract)

        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()
        self.view.display_new_event_validation.assert_called_once()

    @patch("models.Event")
    def test_update_event(self, MockEvent):
        event = MockEvent()
        event.event_name = "Test Event"
        event.id = 1
        event.location = "Initial Location"
        event.nb_attendees = 100
        event.notes = "Initial Notes"
        self.controller.get_event = MagicMock(return_value=event)

        self.controller.set_new_event = MagicMock(
            return_value=(datetime(2023, 7, 22), datetime(2023, 7, 23))
        )
        self.view.input_event_location.return_value = "Updated Location"
        self.view.input_event_nb_attendees.return_value = 200
        self.view.input_event_notes.return_value = "Updated Notes"

        self.controller.update_event()

        self.session.commit.assert_called_once()

        # Assurez-vous que les valeurs de l'événement ont été mises à jour
        self.assertEqual(event.location, "Updated Location")
        self.assertEqual(event.nb_attendees, 200)
        self.assertEqual(event.notes, "Updated Notes")
        self.assertEqual(event.start_date, datetime(2023, 7, 22))
        self.assertEqual(event.end_date, datetime(2023, 7, 23))

    @patch("models.Event")
    def test_get_event(self, MockEvent):
        event_name = "Event Test"
        assigned_support = self.user
        self.view.input_event_name.return_value = event_name
        filters = {"event_name": event_name, "user": assigned_support}

        event = MockEvent()
        self.session.query().filter_by(**filters).first.return_value = event

        result = self.controller.get_event(assigned_support)
        self.assertEqual(result, event)

    def test_set_new_event_date(self):
        date_input = "22-07-23"
        self.view.input_event_start_date.return_value = date_input

        date_result = self.controller.set_new_event_date(is_start_date=True)
        self.assertEqual(
            date_result, datetime.strptime(date_input, "%d-%m-%y")
        )


if __name__ == "__main__":
    unittest.main()
