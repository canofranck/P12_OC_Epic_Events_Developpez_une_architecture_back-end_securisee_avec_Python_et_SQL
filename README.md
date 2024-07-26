

# Projet 12 Epic Events

## Installation & lancement

Commencez tout d'abord par installer Python 

Lancez ensuite la console, placez vous dans le dossier de votre choix puis clonez ce repository:
```
git clone https://github.com/canofranck/P12_OC_Epic_Events_Developpez_une_architecture_back-end_securisee_avec_Python_et_SQL
```
Placez vous dans le dossier P12_OC_Epic_Events_Developpez_une_architecture_back-end_securisee_avec_Python_et_SQL, puis créez un nouvel environnement virtuel:
```
pip install pipenv
pipenv install
```
Ensuite, activez-le.
```
env\Scripts\activate.bat
```

Installez ensuite les packages requis:
```
pipenv install -r requirements.txt

```

## Configuration de la database

Pour ce projet il faut utiliser une Base de donées MySQL.
L application est configuré en local donc veuillez installer MySQL sur votre ordinateur et configuré le : [ download MySQL](https://dev.mysql.com/downloads/installer/)

ensuite utilisé le fichier .env_template pour créer le fichier .env 
Veuillez remplir le fichier avec les informations de votre database MySQL et les info souhaité pour l application 

ATTENTION : tous les champs du ficher a creer .env ne doivent pas avoir de guillemet
```
username= username de la base 
password= password de la base
host= nom du host de la base
database_name= nom souhaité pour la base de l application
salt= clef de salage
secret_key= clef secrete
sentry_url= adresse de votre sentry 
ADMIN_FIRST_NAME= prenom de l admin 
ADMIN_LAST_NAME= nom de l admin 
ADMIN_EMAIL= email de l admin
ADMIN_PHONE= telephone ( +33xxxxxxxxx)
ADMIN_PASSWORD= mot de pass de l admin 

exemple : 
username=root
password=password
host=localhost
database_name=p12_prod
salt=$2b$12$aaaaaaaaaaaaaaaaaaa
secret_key=#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
sentry_url=https://aaaaaaaaaaaaaaaaa@aaaaaaaingest.de.sentry.io/4507526680150096
ADMIN_FIRST_NAME=admin
ADMIN_LAST_NAME=admin user
ADMIN_EMAIL=admin@admin@fr
ADMIN_PHONE=+33110203040
ADMIN_PASSWORD=adminpassword
```

## Lancement du projet 

Pour lancer le projet , dans le terminal à la racine du projet une fois la configuration au dessus éffectué , activer l environnement virtuel et lancer l application :

```
python main.py 
```

Connectez vous à l application avec le login et mot de passe choisi dans le fichier .env

suivez les menus , et crées vos utilisateur commercial et support


## Tests

### Unit tests
 unittest est utilisé pour gérer les tests unitaires, tous ces tests sont stockés dans le repertoire tests/ à la racine du projet.

Pour avoir les test unitaire tapez :
 ```
 pytest -v tests/
 ```

### Coverage

Pour avoir la couverture du code tapez :
```
    pytest --cov=.
```
