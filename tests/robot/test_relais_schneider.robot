*** Settings ***
Library    ../src/SchneiderRelayLibrary.py    use_mock=True

Suite Setup    Connecter au relais
Suite Teardown    Déconnecter du relais

*** Variables ***
${TENSION_MIN}    207.0
${TENSION_MAX}    253.0

*** Test Cases ***
TC01 - Disjoncteur fermé au démarrage
    [Documentation]    Vérifie que le relais est fermé au démarrage
    [Tags]    smoke
    Vérifier disjoncteur fermé

TC02 - Tensions triphasées dans la plage nominale
    [Documentation]    Vérifie que les tensions mesurées sont dans la plage nominale
    [Tags]    mesures
    Lire et stocker mesures du relais
    Vérifier tension dans plage   L1   ${TENSION_MIN}   ${TENSION_MAX}
    Vérifier tension dans plage   L2   ${TENSION_MIN}   ${TENSION_MAX}
    Vérifier tension dans plage   L3   ${TENSION_MIN}   ${TENSION_MAX}

TC03 - Lecture complète des mesures
    [Documentation]    Vérifie que toutes les mesures sont lues et stockées correctement
    [Tags]    mesures
    ${mesures}=    Lire et stocker mesures du relais
    Log    Fréquence réseau : ${mesures.frequence_hz} Hz
    Log    Etat du disjoncteur : ${mesures.etat_disjoncteur}