"""
calculer la puissance active
U x I x cos(phi)
"""
def calculer_puissance_active(tension, courant, cos_phi):
    
        if ((cos_phi < 0) or (cos_phi > 1)):
            raise ValueError("cos_phi doit etre en 0 et 1")
        
        if(tension<0):
            raise ValueError("tension doit etre positif")
        if(courant<0):
            raise ValueError("courant doit etre positif")
        puissance_active = tension * courant * cos_phi
        return puissance_active

def est_en_surcharge(courant_mesure, courant_nominal, seuil_pourcent=110):
    
    if (courant_nominal <= 0):
        raise ValueError("courant_nominal doit etre positif")

    seuil_surcharge = courant_nominal * (seuil_pourcent / 100)
    
    reponse = False
    if (courant_mesure > seuil_surcharge):
        reponse = True
        
    return reponse

def calculer_taux_desequilibre(tensions):
    if len(tensions) != 3:
        raise ValueError("Il doit y avoir exactement 3 tensions pour calculer le taux de desequilibre.")

    moyenne = sum(tensions) / len(tensions)
    if moyenne == 0:
        raise ValueError("La moyenne des tensions ne peut pas être zéro.")

    ecart_max = max(abs(tension - moyenne) for tension in tensions)
    taux = (ecart_max / moyenne) * 100

    return taux


if __name__ == "__main__":
    print(calculer_puissance_active(230,0.2,0.7))
    print(est_en_surcharge(12,10))
    print(calculer_taux_desequilibre([230, 220, 240]))
    