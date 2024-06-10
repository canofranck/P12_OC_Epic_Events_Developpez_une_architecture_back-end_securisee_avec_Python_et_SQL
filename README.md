![chess_club](_img/echec.jpg)

# Projet 4 Tournoi Echecs
***logiciel de gestion de tournoi d'échecs.***

Développé sous Windows 10  et Python version 3.10.11


## Table des matières

1. [Installation du projet](#chapitre1)
    1. [Windows](#chapitre1-1)
    1. [MacOS et Linux](#chapitre1-2)
    3. [Générer un rapport flake8](#chapitre1-3)
2. [menus du programme](#chapitre2)
    1. [Menu principal](#chapitre2-1)
    2. [Menu des Rapports](#chapitre2-2)
3. [Exemple de match et de rapports](#chapitre3)
    1. [Affichage entrée d'un match](#chapitre3-1)
    2. [Exemple de Rapports](#chapitre3-2)


<div id='chapitre1'></div>

## 1. Initialisation du projet

<div id='chapitre1-1'></div>


#### i. Windows :
Dans Windows Powershell, naviguer vers le dossier souhaité.
###### Récupération du projet

     git clone https://github.com/canofranck/projet4_tournoi_d_echecs

###### Activer l'environnement virtuel
    cd Repertoire_du_projet
    python -m venv env 
    env\scripts\activate
    
###### Installer les packages requis
    pip install -r requirements.txt

###### Lancer le programme
    python main.py


<div id='chapitre1-2'></div>

---------

#### ii. MacOS et Linux :
Dans le terminal, naviguer vers le dossier souhaité.
###### Récupération du projet

    $ git clone  https://github.com/canofranck/projet4_tournoi_d_echecs

###### Activer l'environnement virtuel
    $ cd Repertoire_du_projet
    $ python3 -m venv env 
    $ env/bin/activate
    
###### Installer les packages requis
    $ pip install -r requirements.txt

###### Lancer le programme
    $ python3 main.py


<div id='chapitre1-3'></div>

----------

#### iii. Générer un rapport flake8

    $ flake8 --format=html --htmldir=flake8-report --exclude=env .


**Vous trouverez le rapport dans le dossier 'flake8-report'**


![latest_report](_img/flake8.jpg)

<div id='chapitre2'></div>

## 2. menus du programme

<div id='chapitre2-1'></div>

#### i. Menu Principal
![main_menu](_img/menu_main.jpg)

<div id='chapitre2-2'></div>

#### ii. Menu des rapports
![main_menu](_img/menu_reports.jpg)

<div id='chapitre3'></div>

## 3. Exemple de match et de rapports

<div id='chapitre3-1'></div>

#### i. Affichage entrée d'un match :
![round](_img/round.jpg)

<div id='chapitre3-2'></div>

#### ii. Exemple de Rapports :
![report_player](_img/reports_player.jpg)


![report_round](_img/reports_round.jpg)
