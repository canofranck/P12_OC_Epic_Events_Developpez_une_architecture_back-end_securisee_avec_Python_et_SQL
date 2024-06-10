# from views.main_view import MainView
# from controllers.player_controller import PlayerController
# from controllers.report_controller import ReportController
# from controllers.tournament_controller import TournamentController
# import constantes


class MainController:
    pass


#     """Contrôleur principal de l'application."""

#     def __init__(self):
#         """Initialise le contrôleur principal."""
#         self.main_view = MainView()
#         self.player_controller = PlayerController()
#         self.tournament_controller = TournamentController()
#         self.report_controller = ReportController(self.player_controller)
#         self.main_view = MainView()

#     def run(self):
#         """Lance l'application principale.
#         Cette méthode démarre l'application et affiche le menu principal.
#         En fonction du choix de l'utilisateur, elle dirige vers d'autres
#         fonctionnalités telles que le menu des joueurs, le menu des tournois,
#         le menu de rapports ou termine l'application.
#         Args:
#             Aucun argument requis.
#         Returns:
#             Aucune valeur de retour.
#         Raises:
#             Aucune exception n'est levée.
#         """

#         while True:
#             self.main_view.clear_screen()
#             choice = self.main_view.display_main_menu()

#             if choice == constantes.MAIN_MENU_JOUEUR:
#                 self.player_controller.run_player_menu()
#             elif choice == constantes.MAIN_MENU_TOUNOI:
#                 self.tournament_controller.run_tournament_menu()
#             elif choice == constantes.MAIN_MENU_REPORTS:
#                 self.report_controller.run_report_menu()
#             elif choice == constantes.MAIN_MENU_QUIT:
#                 print("Au revoir !")
#                 break
#             else:
#                 self.main_view.display_invalid_option_message()
