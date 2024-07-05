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
            "error": "red",  # Messages d'erreur en rouge
            "success": "bold green",  # Messages de succès en vert gras
            "menu_choice": "bright_cyan bold",  # Sélection du menu en cyan clair et gras
            "menu_text": "light_green",  # Texte du menu en jaune clair
            "panel": "white bold",  # Texte des panneaux en blanc gras
            "input": "bright_magenta bold",  # Entrées utilisateur en magenta clair et gras
        }
    )
    return Console(theme=custom_theme)
