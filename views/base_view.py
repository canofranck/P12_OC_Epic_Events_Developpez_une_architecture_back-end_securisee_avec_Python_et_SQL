import os
import sys
from views.main_view import MainView

if os.name == "nt":
    import msvcrt
else:
    import termios
    import tty


class BaseView:
    def wait_for_key_press(self):
        print("Appuyez sur une touche pour continuer...")
        if os.name == "nt":
            msvcrt.getch()
            MainView.clear_screen(self)
        else:
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
