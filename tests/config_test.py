from unittest.mock import MagicMock
import controllers


def new_mock_main_controller():
    mock_session = MagicMock()
    mock_console = MagicMock()
    mock_user_controller = MagicMock()
    mock_customer_controller = MagicMock()
    mock_contract_controller = MagicMock()
    mock_event_controller = MagicMock()

    mock_main_controller = controllers.MainController(
        session=mock_session, console=mock_console
    )
    mock_main_controller.user_controller = mock_user_controller
    mock_main_controller.customer_controller = mock_customer_controller
    mock_main_controller.contract_controller = mock_contract_controller
    mock_main_controller.event_controller = mock_event_controller

    mock_main_controller.view = MagicMock()
    return mock_main_controller


def new_mock_user_controller(salt, secret_key):
    mock_session = MagicMock()
    mock_view = MagicMock()

    mock_user_controller = controllers.UserController(
        session=mock_session, view=mock_view, salt=salt, secret_key=secret_key
    )
    mock_user_controller.view = MagicMock()
    return mock_user_controller


def new_mock_customer_controller():
    mock_session = MagicMock()
    mock_view = MagicMock()

    mock_customer_controller = controllers.CustomerController(
        session=mock_session, view=mock_view
    )

    return mock_customer_controller


def new_mock_contract_controller():
    mock_session = MagicMock()
    mock_view = MagicMock()

    mock_contract_controller = controllers.ContractController(
        session=mock_session, view=mock_view
    )

    return mock_contract_controller


def new_mock_event_controller():
    mock_session = MagicMock()
    mock_view = MagicMock()

    mock_event_controller = controllers.EventController(
        session=mock_session, view=mock_view
    )
    mock_event_controller.view = MagicMock()
    return mock_event_controller
