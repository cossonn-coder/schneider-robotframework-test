from robot.api.deco import keyword, library
from robot.api import logger
from schneider_relay import SchneiderRelayDriver

@library(scope="SUITE")
class SchneiderRelayLibrary:
    #port modbus = 502 par défaut, mais ici 5020 pour tester sans matériel physique et éviter les conflits
    def __init__(self, ip="127.0.0.1", port=5020, use_mock="False", mock_backend=None):
        is_mock_enabled = str(use_mock).lower() == "true"
        
        if is_mock_enabled or mock_backend is not None:
            from mock_relay import MockSchneiderRelay
            backend = mock_backend or MockSchneiderRelay()
        else:
            backend = None
            
        self._driver = SchneiderRelayDriver(ip, port=int(port), mock_backend=backend)
        self._mesures = None
    
    @keyword("Connecter au relais")
    def connecter_au_relais(self):
        succes = self._driver.connecter()
        if not succes:
            raise RuntimeError(
                f"Echec connexion {self._driver.ip}:{self._driver.port}"
                )
        logger.info(
            f"Connecté au relais à {self._driver.ip}:{self._driver.port}"
            )

    @keyword("Déconnecter du relais")
    def deconnecter_du_relais(self):
        self._driver.deconnecter()
        logger.info(
            f"Déconnecté du relais à {self._driver.ip}:{self._driver.port}"
            )
    
    @keyword("Lire et stocker mesures du relais")
    def lire_et_stocker_mesures(self):
        self._mesures = self._driver.lire_mesures()
        logger.info(
            f"UL1={self._mesures.tension_l1_v}V | "
            f"IL1={self._mesures.courant_l1_a}A | "
            f"Etat={self._mesures.etat_disjoncteur}"
            )
        return self._mesures
    
    @keyword("Vérifier tension dans plage")
    def verifier_tension_dans_plage(self, phase, min_v, max_v):
        if self._mesures is None:
            raise RuntimeError(
                "Aucune mesure disponible. Appeler 'Lire et stocker mesures du relais' avant."
                )
        
        tension = {
            "L1": self._mesures.tension_l1_v,
            "L2": self._mesures.tension_l2_v,
            "L3": self._mesures.tension_l3_v,
        }

        if phase not in tension:
            raise ValueError(
                f"Phase invalide : {phase}. Doit être L1, L2 ou L3."
                )
        tension = tension[phase]
        if not (float(min_v) <= tension <= float(max_v)):
            raise AssertionError(
                f"Tension {phase} hors plage : {tension}V pas dans [{min_v}V, {max_v}V]."
                )
    
    @keyword("Vérifier disjoncteur fermé")
    def verifier_disjoncteur_ferme(self):
        mesures=self._driver.lire_mesures()
        if mesures.etat_disjoncteur != "FERME":
            raise AssertionError(
                f"Disjoncteur devrait être fermé : état actuel = {mesures.etat_disjoncteur}"
                )