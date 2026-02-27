*** Settings ***
Library    ../src/ElectricalLibrary.py

*** Test Cases ***
Vérifier équilibre réseau
    Vérifier équilibre réseau  230.0  229.0  231.0

Vérifier abscence de surcharge
    Vérifier abscence de surcharge  15.0  16.0