# Framework de Test Automatisé — Relais de Protection Schneider

## Contexte
Un relais de protection industriel surveille en continu les paramètres électriques (courant, tension) 
pour ordonner le déclenchement d'un disjoncteur en cas d'anomalie, 
protégeant ainsi le matériel et le personnel. 
Le test automatique est indispensable 
pour garantir une précision rigoureuse des seuils de déclenchement, 
assurer la répétabilité des mesures
et valider rapidement les multiples fonctions complexes des relais numériques modernes.

## Stack technique
- Python 3.14 / pytest — tests unitaires
- Robot Framework 7 — tests d'acceptance
- pymodbus — communication Modbus TCP
- Mock interne — simulation sans matériel physique

## Structure du projet
```
schneider_robotframework/
├── src/
│   ├── __init__.py
│   ├── electrical_utils.py        ✅ fait — 3 fonctions de calcul
│   ├── schneider_relay.py         ✅ fait — driver Modbus + dataclass
│   ├── mock_relay.py              ✅ fait — simulateur relais
│   ├── ElectricalLibrary.py       ✅ fait — librairie RF calculs
│   └── SchneiderRelayLibrary.py   ✅ fait — librairie RF relais
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_electrical_utils.py   ✅ 9 tests PASSED
│   │   └── test_schneider_relay.py    ✅ 4 tests PASSED
│   └── robot/
│       ├── test_calcul.robot          ✅ 2 tests PASSED
│       └── test_relais_schneider.robot ✅ 3 tests PASSED
├── requirements.txt
└── .venv/
```

## Lancer les tests
```powershell
# Installer les dépendances
pip install -r requirements.txt

# Tests unitaires
pytest tests/unit/ -v

# Tests d'acceptance
robot --pythonpath . --pythonpath src --outputdir logs tests/robot/
```

## Résultats
- 13 tests unitaires PASSED
- 5 tests d'acceptance PASSED (mode mock)
- Rapport HTML disponible dans logs/

## Normes appliquées
- EN 50160 — qualité de tension réseau
- IEC 60947 — seuil de surcharge 110% In
- IEC 61000-2-2 — taux de déséquilibre < 2%