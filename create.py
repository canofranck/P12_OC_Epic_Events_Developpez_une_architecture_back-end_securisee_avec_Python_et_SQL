from models.user import User, UserRole
from database import init_db


def main():
    # Initialisez la session SQLAlchemy
    session = init_db()

    # Créez un nouvel utilisateur
    nouvel_utilisateur = User(
        username="nouvel_utilisateur",
        password="mot_de_passe",
        full_name="Nom Complet",
        email="nouvel_utilisateur@example.com",
        phone_number="1234567890",
        role=UserRole.MANAGER,  # Choisissez le rôle approprié
    )

    # Ajoutez l'utilisateur à la session et enregistrez-le dans la base de données
    session.add(nouvel_utilisateur)
    session.commit()
    print("Utilisateur créé avec succès.")


if __name__ == "__main__":
    main()
