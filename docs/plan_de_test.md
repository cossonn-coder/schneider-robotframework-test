# Plan de Test — Relais Schneider

## Objectif
Valider la logique de calcul électrique et la communication Modbus TCP 
du driver SchneiderRelayDriver, sans dépendance au matériel physique.

## Périmètre
| Inclus | Exclu |
|--------|-------|
| Calculs électriques (puissance, surcharge, déséquilibre) | Interface HMI |
| Driver Modbus + mock | IEC 61850 (prévu v2) |
| Tests d'acceptance RF | Tests de charge |

## Stratégie
- Tests unitaires pytest sur les fonctions pures (electrical_utils.py)
- Tests d'intégration mock sur le driver (schneider_relay.py)
- Tests d'acceptance Robot Framework sur les scénarios métier complets

## Critères de succès
- 0 test en échec
- Couverture de tous les cas limites (valeurs invalides, surcharge, déséquilibre)
- Rapport HTML généré automatiquement

## Cas de test unitaires (pytest)

### electrical_utils.py — 9 tests

| ID | Nom du test | Scénario | Critère de succès |
|----|-------------|----------|-------------------|
| UT01 | test_cas_nominal | Appel avec tension=230, courant=10, cos_phi=0.9 | Retourne 2070.0 |
| UT02 | test_cos_phi_invalide | cos_phi=1.5 (hors plage) | Lève ValueError |
| UT03 | test_tension_negative | tension=-10 | Lève ValueError |
| UT04 | test_courant_negatif | courant=-5 | Lève ValueError |
| UT05 | test_surcharge | courant_mesure=120A, nominal=100A, seuil=110% | Retourne True |
| UT06 | test_courant_nominal_invalide | courant_nominal=0 | Lève ValueError |
| UT07 | test_calculer_taux_desequilibre | tensions=[230, 220, 240] | Retourne ~4.3478260869565215% |
| UT08 | test_calculer_taux_desequilibre_tensions_incorrectes | liste de 2 tensions | Lève ValueError |
| UT09 | test_calculer_taux_desequilibre_moyenne_zero | tensions=[0, 0, 0] | Lève ValueError |

### schneider_relay.py — 4 tests

| ID | Nom du test | Scénario | Critère de succès |
|----|-------------|----------|-------------------|
| UT10 | test_lecture_reseau_normal | Mock réseau normal, lecture mesures | tension_l1=230V, etat=FERME |
| UT11 | test_simuler_ouverture_disjoncteur | Mock ouverture, lecture mesures | etat=OUVERT, courants=0A |
| UT12 | test_lecture_sans_connexion | Appel lire_mesures() sans connecter() | Lève RuntimeError |
| UT13 | test_surcharge | Mock injection 150A sur L1 | est_en_surcharge() retourne True |


## Cas de test d'acceptance (Robot Framework)

| ID | Fichier | Nom du test | Tag | Scénario | Critère de succès |
|----|---------|-------------|-----|----------|-------------------|
| AT01 | test_calcul.robot | Vérifier équilibre réseau | mesures | Mock réseau normal, appel keyword équilibre | Taux déséquilibre < 2%, pas d'exception |
| AT02 | test_calcul.robot | Vérifier abscence de surcharge | protection | Mock 10A sur nominal 100A | est_en_surcharge() retourne False |
| AT03 | test_relais_schneider.robot | TC01 - Disjoncteur fermé au démarrage | smoke | Connexion mock, lecture état | etat_disjoncteur = FERME |
| AT04 | test_relais_schneider.robot | TC02 - Tensions triphasées dans la plage nominale | mesures | Lecture L1/L2/L3, vérif plage EN 50160 | Toutes tensions ∈ [207V, 253V] |
| AT05 | test_relais_schneider.robot | TC03 - Lecture complète des mesures | mesures | Lecture toutes grandeurs, log fréquence et état | Pas d'exception, fréquence et état loggés |