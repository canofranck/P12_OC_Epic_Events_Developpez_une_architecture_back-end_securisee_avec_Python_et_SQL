@echo off
rem Exécuter les tests avec collecte de la couverture en utilisant le fichier de configuration
coverage run -m unittest discover -s tests

rem Générer un rapport HTML
coverage html

rem Ouvrir le rapport HTML dans le navigateur par défaut
start htmlcov\index.html
