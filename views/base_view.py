import os
import sys
import views

if os.name == "nt":
    import msvcrt
else:
    import termios
    import tty


class BaseView:
    """
    The BaseView class serves as the base class for all views in the application.

    Attributes:
        console: The console object used for displaying output.

    Methods:
        __init__(self, console):
            Initializes the BaseView with the given console object.

        wait_for_key_press(self):
            Waits for the user to press a key before continuing.
    """

    def __init__(self, console):
        """
        Initializes the BaseView with the given console object.

        Args:
            console: The console object used for displaying output.
        """
        self.console = console

    def wait_for_key_press(self):
        """
        Waits for the user to press a key before continuing.
        """
        print("Press a key ton continue ...")
        if os.name == "nt":
            msvcrt.getch()
            views.MainView.clear_screen(self)
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
