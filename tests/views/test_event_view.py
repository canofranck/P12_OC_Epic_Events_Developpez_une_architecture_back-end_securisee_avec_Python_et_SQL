import unittest
from unittest.mock import patch, MagicMock
import models
import constantes
from views import EventView
from rich.panel import Panel


class TestEventView(unittest.TestCase):

    def setUp(self):
        self.console = MagicMock()

        self.view = EventView(self.console)

    @patch("builtins.input", side_effect=["test de notes"])
    def test_input_event_notes(self, mock_input):
        result = self.view.input_event_notes()
        self.assertEqual(result, "test de notes")
        self.console.print("Event notes : ", style="input")

    @patch("builtins.input", side_effect=["10-05-25"])
    def test_input_event_start_date(self, mock_input):
        result = self.view.input_event_start_date()
        self.assertEqual(result, "10-05-25")
        self.console.print("Event start date: (DD-MM-YY)", style="input")

    @patch("builtins.input", side_effect=["test event name"])
    def test_input_event_name(self, mock_input):
        result = self.view.input_event_name()
        self.assertEqual(result, "test event name")
        self.console.print("Event name : ", style="input")

    @patch("builtins.input", side_effect=["test location"])
    def test_input_event_location(self, mock_input):
        result = self.view.input_event_location()
        self.assertEqual(result, "test location")
        self.console.print("Event location : ", style="input")

    @patch("builtins.input", side_effect=["12"])
    def test_input_event_nb_attendees(self, mock_input):
        result = self.view.input_event_nb_attendees()
        self.assertEqual(result, 12)
        self.console.print("Event attendees : ", style="input")

    @patch("builtins.input", side_effect=["event notes"])
    def test_input_event_notes(self, mock_input):
        result = self.view.input_event_notes()
        self.assertEqual(result, "event notes")
        self.console.print("Add a note (max 200 characters) : ", style="input")

    def test_display_new_event_validation(self):
        with patch("views.CustomerView.wait_for_key_press"):
            self.view.display_new_event_validation()
            self.console.print.assert_called_with(
                "[success]New event created[/]"
            )

    def test_display_update_event_validation(self):
        with patch("views.CustomerView.wait_for_key_press"):
            self.view.display_update_event_validation()
            self.console.print.assert_called_with(
                "[success]Event correctly updated[/]"
            )

    def test_input_list_events_filters_no_filter(self):
        with patch("builtins.input", side_effect=["1"]):
            result = self.view.input_list_events_filters()
            self.assertEqual(result, 1)

    def test_input_list_events_filters_you_manage(self):
        with patch("builtins.input", side_effect=["2"]):
            result = self.view.input_list_events_filters()
            self.assertEqual(result, 2)

    def test_input_list_events_filters_no_support(self):
        with patch("builtins.input", side_effect=["3"]):
            result = self.view.input_list_events_filters()
            self.assertEqual(result, 3)

    def test_display_contract_not_signed(self):
        with patch("views.CustomerView.wait_for_key_press"):
            self.view.display_contract_not_signed()
            self.console.print(
                "[error]The contract hasn't been signed, so it's impossible to create an event.[/]"
            )

    def test_display_no_events_found(self):
        with patch("views.CustomerView.wait_for_key_press"):
            self.view.display_no_events_found()
            self.console.print("[error]No events found.[/]")

    def test_display_error(self):
        message = "Custom error message"
        self.view.display_error(message)
        self.console.print.assert_called_with(f"[error] {message} [/]")
