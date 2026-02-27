import pytest
from src.electrical_utils import calculer_puissance_active
from src.electrical_utils import est_en_surcharge
from src.electrical_utils import calculer_taux_desequilibre

def test_cas_nominal():
    # ARRANGE
    tension = 230.0
    courant = 10.0
    cos_phi = 1.0
    
    # ACT
    resultat = calculer_puissance_active(tension, courant, cos_phi)
    

    # ASSERT
    assert resultat == pytest.approx(2300.0)

def test_cos_phi_invalide():
    with pytest.raises(ValueError):
        calculer_puissance_active(230.0, 10.0, 1.5)

def test_tension_negative():
    with pytest.raises(ValueError):
        calculer_puissance_active(-230.0, 10.0, 1.0)

def test_courant_negative():
    with pytest.raises(ValueError):
        calculer_puissance_active(230.0, -10.0, 1.0)

def test_surcharge():
    #ARRANGE
    courant_mesure = 9.0
    courant_nominal = 10.0
    courant_surcharge = 12.0
    #ACT 
    resultat_nominal= est_en_surcharge(courant_mesure, courant_nominal)
    resultat_surcharge = est_en_surcharge(courant_surcharge, courant_nominal)

    #ASSERT
    assert resultat_nominal == False
    assert resultat_surcharge == True

def test_courant_nominal_invalide():
    with pytest.raises(ValueError):
        est_en_surcharge(12.0, -10.0)

def test_calculer_taux_desequilibre():
    # ARRANGE
    tensions = [230.0, 220.0, 240.0]
    
    # ACT
    resultat = calculer_taux_desequilibre(tensions)
    
    # ASSERT
    assert resultat == pytest.approx(4.35, abs=0.01)

def test_calculer_taux_desequilibre_tensions_incorrectes():
    with pytest.raises(ValueError):
        calculer_taux_desequilibre([230.0, 220.0])  # Moins de 3 tensions

def test_calculer_taux_desequilibre_moyenne_zero():
    with pytest.raises(ValueError):
        calculer_taux_desequilibre([0.0, 0.0, 0.0])  # Moyenne des tensions est zéro




