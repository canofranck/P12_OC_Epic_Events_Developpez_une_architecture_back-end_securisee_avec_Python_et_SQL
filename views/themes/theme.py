from rich.console import Console
from rich.theme import Theme


def theme_console():
    """
    Creates a custom theme for the console.

    This function creates a custom theme for the console with specific colors for error messages, success messages,
    menu choices, menu text, and panels.

    Returns:
        console: A Console object with the custom theme.
    """
    custom_theme = Theme(
        {
            "error": "red",
            "success": "bold green",
            "menu_choice": "bright_cyan bold",
            "menu_text": "light_green",
            "panel": "white bold",
            "input": "bright_magenta bold",
        }
    )
    return Console(theme=custom_theme)
