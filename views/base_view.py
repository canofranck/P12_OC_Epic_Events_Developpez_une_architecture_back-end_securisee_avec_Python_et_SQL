import os
import sys
import views

if os.name == "nt":
    import msvcrt
else:
    import termios
    import tty


class BaseView:
    def __init__(self, console):
        self.console = console

    def wait_for_key_press(self):
        print("Appuyez sur une touche pour continuer...")
        if os.name == "nt":
            msvcrt.getch()
            # views.MainView.clear_screen(self)
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
