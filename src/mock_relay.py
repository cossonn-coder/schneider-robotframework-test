import time
from src.schneider_relay import RelaisMesures

class MockSchneiderRelay:
    def __init__(self):
        self._tensions = [230.0, 220.0, 240.0]
        self._courants = [10.0, 10.0, 9.0]
        self._frequence_hz = 50.0
        self._etat = "FERME"
        self._seuils={}
    

    def simuler_reseau_normal(self):
        self._tensions = [230.0, 220.0, 240.0]
        self._courants = [10.0, 10.0, 9.0]
        self._etat = "FERME"

    def simuler_surcharge(self, courant_l1_a):
        self._courants[0] = courant_l1_a
    
    def simuler_desequilibre(self, tensions):
        self._tensions = tensions
    
    def simuler_ouverture_disjoncteur(self):
        self._etat = "OUVERT"
        self._courants = [0.0, 0.0, 0.0]
    
    def get_mesures(self)->RelaisMesures:
        return RelaisMesures(
            tension_l1_v = self._tensions[0],
            tension_l2_v = self._tensions[1],
            tension_l3_v = self._tensions[2],
            courant_l1_a = self._courants[0],
            courant_l2_a = self._courants[1],
            courant_l3_a = self._courants[2],
            frequence_hz = self._frequence_hz,
            horodatage = time.time(),
            etat_disjoncteur = self._etat
        )
    
    def set_seuil(self, nom_seuil, valeur):
        self._seuils[nom_seuil] = valeur
    
    def get_seuil(self, nom_seuil):
        return self._seuils.get(nom_seuil)

