import pytest
from src.schneider_relay import SchneiderRelayDriver
from src.mock_relay import MockSchneiderRelay

@pytest.fixture
def relais():
    mock = MockSchneiderRelay()
    driver = SchneiderRelayDriver(ip="127.0.0.1", mock_backend=mock)
    driver.connecter()
    return mock, driver

def test_lecture_reseau_normal(relais):
    #ARRANGE
    mock, driver = relais
    #ACT
    mock.simuler_reseau_normal()
    mesures = driver.lire_mesures()
    #ASSERT
    assert mesures.tension_l1_v == 230.0
    assert mesures.tension_l2_v == 220.0
    assert mesures.tension_l3_v == 240.0
    assert mesures.courant_l1_a == 10.0
    assert mesures.courant_l2_a == 10.0
    assert mesures.courant_l3_a == 9.0
    assert mesures.frequence_hz == 50.0
    assert mesures.etat_disjoncteur == "FERME"

def test_simuler_ouverture_disjoncteur(relais):
    #ARRANGE
    mock, driver = relais
    #ACT
    mock.simuler_ouverture_disjoncteur()
    mesures = driver.lire_mesures()
    #ASSERT
    assert mesures.courant_l1_a == 0.0
    assert mesures.courant_l2_a == 0.0
    assert mesures.courant_l3_a == 0.0
    assert mesures.etat_disjoncteur == "OUVERT"

def test_lecture_sans_connexion():
    mock = SchneiderRelayDriver(ip="127.0.0.1", mock_backend=None)
    with pytest.raises(RuntimeError):
        mock.lire_mesures()

def test_surcharge(relais):
    #ARRANGE
    mock, driver = relais
    #ACT
    mock.simuler_surcharge(courant_l1_a=20.0)
    mesures = driver.lire_mesures()
    #ASSERT
    assert mesures.courant_l1_a == 20.0
