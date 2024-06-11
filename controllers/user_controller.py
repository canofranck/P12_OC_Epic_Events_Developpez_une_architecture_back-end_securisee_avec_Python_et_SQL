import models
import bcrypt
from views import main_view, user_view
from models.user import User


class UserController:
    """Contrôleur pour la gestion des joueurs."""


pass
# def __init__(self):
#     """Initialise le contrôleur des joueurs."""
#     self.users = []
#     self.user_view = user_view()
#     self.main_view = main_view()

# def run_player_menu(self):
#     """Exécute le menu des joueurs.
#     Cette méthode permet de gérer les actions du menu des joueurs,
#     notamment l'ajout de nouveaux joueurs, l'affichage de la liste des
#     joueurs et la sortie du menu.
#     Args:
#         main_view (obj): La vue principale de l'application.
#     Returns:
#         Aucune valeur de retour.
#     Raises:
#         Aucune exception n'est levée.
#     """
# self.main_view.clear_screen()
# while True:
#     choice = self.player_view.display_player_menu()

#     if choice == constantes.PLAYER_MENU_NOUVEAU:
#         self.add_player()
#     elif choice == constantes.PLAYER_MENU_AFFICHER:
#         self.display_players()
#     elif choice == constantes.PLAYER_MENU_QUIT:
#         break
#     else:
#         self.player_view.display_invalid_option_message()

# def add_player(self):
#     """Ajoute un nouveau joueur.
#     Cette méthode permet d'ajouter un nouveau joueur à la liste des
#     joueurs. Elle vérifie également l'existence du joueur avant l'ajout.
#     Args:
#         Aucun argument requis.
#     Returns:
#         Aucune valeur de retour.
#     Raises:
#         Aucune exception n'est levée.
#     """
#     self.main_view.clear_screen()
#     print("Ajout d'un nouveau joueur...")
#     player_data = self.player_view.get_player_data()
#     last_name = player_data["last_name"]
#     first_name = player_data["first_name"]
#     birth_date = player_data["birth_date"]
#     player_id = player_data["player_id"]
#     player_id_national = player_data["player_id_national"]
#     score_tournament = player_data["score_tournament"]
#     player = Player(
#         last_name,
#         first_name,
#         birth_date,
#         player_id,
#         player_id_national,
#         score_tournament,
#     )
#     # Vérifiez s'il y a des doublons en fonction de l'identifiant du joueur

#     if Player.is_player_id_taken(player_id_national):
#         print(
#             "Le joueur existe déjà dans la base de données.Veuillez entrez un nouveau joueur"
#         )
#     else:
#         player.save()
#         print("Joueur ajouté avec succès dans la sauvegarde!")

# def display_players(self):
#     """Affiche la liste des joueurs.
#     Cette méthode affiche la liste de tous les joueurs par ordre
#     alphabétique en fonction de leur nom de famille et de leur prénom.
#     Args:
#         Aucun argument requis.
#     Returns:
#         output_string (str): Une chaîne de caractères contenant la liste
#                              de tous les joueurs.
#     Raises:
#         Aucune exception n'est levée.
#     """
#     self.main_view.clear_screen()
#     players = Player.load_players()
#     self.player_view.afficher_list(players)
