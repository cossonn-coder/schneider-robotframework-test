from robot.api.deco import keyword, library
from electrical_utils import (
    calculer_puissance_active,
    est_en_surcharge,
    calculer_taux_desequilibre,
)

@library(scope="SUITE")
class ElectricalLibrary:

    @keyword("Vérifier abscence de surcharge")
    def vérifier_abscence_surcharge(self, courant_mesure, courant_nominal, seuil_pourcent=110):
        if est_en_surcharge(float(courant_mesure), float(courant_nominal), float(seuil_pourcent)):
            raise AssertionError(
                f"SURCHARGE : {courant_mesure} A mesuré > à {110} * {courant_nominal} A."
                )

    @keyword("Vérifier équilibre réseau")
    def verifier_equilibre_reseau(self, u1,u2,u3, seuil= 2.0):
        tensions = [float(u1),float(u2),float(u3)]
        taux = calculer_taux_desequilibre(tensions)
        if taux > float(seuil):
            raise AssertionError(
                f"DESEQUILIBRE : {taux:.2f}% > {seuil}%."
                )
        return taux