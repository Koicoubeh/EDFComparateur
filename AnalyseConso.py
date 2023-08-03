#################################################################################################
#
# Ce programme sert à analyser la consommation d'électricité d'un abonnement EDF, il permet de
# de comparer les différents forfaits EDF sur cette consommation passée, et de déterminer lequel
# est le plus avantageux.
# Il tient compte des jours Tempo (bleu, blanc, rouge) et des heures creuses.
#
# Auteur : Koicoubeh
# Contributeur du fichier CSV d'exemple et aide au débug : @MathieuMf (Twitter)
#
#################################################################################################

import csv
from datetime import datetime, timedelta


#################################################################################################
#
# Variables amenées à être modifiées par les utilisateurs
#
#################################################################################################

# Tableaux contenant les heures creuses. Si c'est pas creux... c'est plein !
# exemple : 0,1,2,3,4,5,22,23 : HC de 0h à 6h et de 22h à 24h
HC = [0,1,2,3,4,5,22,23]

# Abonnement en kVA : 6, 9 ou 12
abonnement = 9

# Chemin vers le fichier CSV. Ce fichier est à récupérer sur le site d'Enedis, en ayant activé 
# l'option "Historique de consommation" avec le pas demi-horaire dans l'espace client.
# Il faut que le fichier soit sur 1 an (pas de contrôle sur ce point, mais le résultat ne serait pas significatif)
chemin_csv = "consoexemple.csv"

#################################################################################################
#
# Variables peu susceptibles d'être modifiées par les utilisateurs
#
#################################################################################################

# Prix des différents W.h. Faire un XML/YAML/Json ?
# Attention, les données d'origine sont pour des kW.h mais les données du CSV son des W.h
# Données d'origine  https://particulier.edf.fr/content/dam/2-Actifs/Documents/Offres/Grille_prix_Tarif_Bleu.pdf
# Tarifs au 01/08/2023

TempoBleuHC = 0.1056
TempoBleuHP = 0.1369
TempoBlancHC = 0.1246
TempoBlancHP = 0.1654
TempoRougeHC = 0.1328
TempoRougeHP = 0.7324
AboTempo6kva = 12.8
AboTempo9kva = 16.0
AboTempo12kva = 19.29

BleuBase = 0.2276
AboBleu3kva = 9.47
AboBleu6kva = 12.44
AboBleu9kva = 15.63
AboBleu12kva = 18.89

BleuHC = 0.1828
BleuHP = 0.246
AboHC6kva = 12.85
AboHP9kva = 16.55
AboHP12kva = 19.97

# Dictionnaire des jours bleu blanc rouge. Chaque élément est un tuple (date, couleur)
CalBar = {}

# Tableau des données de consommation. Chaque élément est un tuple (date_heure, consommation HC, consommation HP)
CalConso = []

# Nombre de mois dans le fichier CSV de consommation de l'utilisateur. Par défaut 12
nbMois = 12
PremierMois = 0
DernierMois = 0

# Initialisation des sommes pour chacun des forfaits testés
simulTempo, simulBase, simulHCHP = 0.0, 0.0, 0.0

# Consommation en HP et HC
ConsoHP, ConsoHC = 0.0, 0.0

# Importe un fichier avec les dates des jours bleu blanc rouge, et les stocke dans une liste
# Fichier CSV avec 2 colonnes : date et couleur
# Généré à la main depuis les fichiers "Calendrier TEMPO" dispos sur le site de RTE :
# https://www.rte-france.com/eco2mix/telecharger-les-indicateurs
# Ouvrir le fichier CSV en mode lecture
with open("calBAR.csv", newline='') as csvfile:
    # Créer un objet lecteur CSV
    lecteur_csv = csv.reader(csvfile, delimiter=';')
    
    # Parcourir chaque ligne du CSV
    for ligne in lecteur_csv:
        # Convertir la date au format "01/09/2019" en objet datetime
        date_str = ligne[0]
        date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
        
        # Utiliser la date au format "YYYY-MM-DD" comme clé dans le dictionnaire
        # et la couleur comme valeur associée
        CalBar[date_obj.strftime("%Y-%m-%d")] = ligne[1]



# Ouvrir le fichier CSV de consommation en mode lecture
with open(chemin_csv, newline='', encoding='utf-8-sig') as csvfile:
    lecteur = csv.reader(csvfile, delimiter=';')
    i = 0
    for ligne in lecteur:      
        # Gestion simpliste de l'entête du CSV : si le 5e caractère de la ligne n'est pas un tiret (donc une date), ignorer la ligne
        if ligne[0][4] == "-":
            i += 1
            date_heure = ligne[0]
            consommation = int(ligne[1]) if ligne[1].strip() else 0        
            consommation = consommation / 2000  # Convertir les W sur 30 minutes en kW.h

            date_heure = date_heure[:-6]  # Enlever le décalage horaire (ex: +01:00)            

            # Récupération du 1er mois, pour compter le nombre de mois que recouvre le CSV
            if i == 1:
                PremiereDate = datetime.fromisoformat(date_heure.replace("Z", "+00:00"))

            # Extraire la date (ex: "2023-01-05")
            jour = date_heure[:10]
            # Extraire l'heure (ex: "23:59")
            heure = date_heure[11:]

            # Voir si le jour est bleu, blanc ou rouge
            if jour in CalBar:
                couleur = CalBar[jour]
                # print(f"{jour} {heure} {consommation} {couleur}")

                # tester en fonction de l'heure (un jour commence à 6h, pas à minuit).
                # Si l'heure est inférieure à 6h, on considère que c'est la veille
                if heure < "06:00":
                    jour = (datetime.strptime(jour,"%Y-%m-%d").date() - timedelta(days=1)).strftime("%Y-%m-%d")
                    # jour = temp.strftime("%Y-%m-%d")
                    # print(f" nouveau jour : {jour}")

                # On applique les tarifs en fonction de la couleur du jour et de l'HP/HC
                if couleur == "BLEU":
                    if int(heure[:2]) in HC:
                        ConsoHC += consommation
                        simulTempo += consommation * TempoBleuHC
                        simulBase += consommation * BleuBase
                        simulHCHP += consommation * BleuHC
                    else:
                        ConsoHP += consommation
                        simulTempo += consommation * TempoBleuHP
                        simulBase += consommation * BleuBase
                        simulHCHP += consommation * BleuHP
                elif couleur == "BLANC":
                    if int(heure[:2]) in HC:
                        ConsoHC += consommation
                        simulTempo += consommation * TempoBlancHC
                        simulBase += consommation * BleuBase
                        simulHCHP += consommation * BleuHC
                    else:
                        ConsoHP += consommation
                        simulTempo += consommation * TempoBlancHP
                        simulBase += consommation * BleuBase
                        simulHCHP += consommation * BleuHP
                elif couleur == "ROUGE":
                    if int(heure[:2]) in HC:
                        ConsoHC += consommation
                        simulTempo += consommation * TempoRougeHC
                        simulBase += consommation * BleuBase
                        simulHCHP += consommation * BleuHC
                    else:
                        ConsoHP += consommation
                        simulTempo += consommation * TempoRougeHP
                        simulBase += consommation * BleuBase
                        simulHCHP += consommation * BleuHP
            else:
                print(f"Valeur hors calendrier TEMPO supporté pour la ligne {i} : {jour}")

    # Calcul du nombre de mois que recouvre le fichier CSV
    DerniereDate = datetime.fromisoformat(date_heure.replace("Z", "+00:00"))

    # Durée en mois couverte par le CSV 
    nbMois = int((DerniereDate - PremiereDate).days / 30)
    DernierMois = int(date_heure[5:7])
    print(f"Nombre de lignes traitées : {i}")
    # nbMois = DernierMois - PremierMois + 1
    print(f"Nombre de mois dans le CSV : {nbMois}")

# Ajout du coût annuel de l'abonnement
if abonnement == 6:
    simulTempo += AboTempo6kva*nbMois
    simulBase += AboBleu6kva*nbMois
    simulHCHP += AboHC6kva*nbMois
elif abonnement == 9:
    simulTempo += AboTempo9kva*nbMois
    simulBase += AboBleu9kva*nbMois
    simulHCHP += AboHP9kva*nbMois
elif abonnement == 12:
    simulTempo += AboTempo12kva*nbMois
    simulBase += AboBleu12kva*nbMois
    simulHCHP += AboHP12kva*nbMois

#Arrondir à 2 décimales
simulTempo = round(simulTempo, 2)
simulBase = round(simulBase, 2)
simulHCHP = round(simulHCHP, 2)
ConsoHC = round(ConsoHC, 2)
ConsoHP = round(ConsoHP, 2)

print()
print(f"Consommation HP : {ConsoHP} kW.h")
print(f"Consommation HC : {ConsoHC} kW.h")
print(f"Consommation totale : {round(ConsoHP + ConsoHC, 2)} kW.h")
print()
print(f"Simulation des coûts sur {nbMois} mois, selon les 3 forfaits :")
print(f"  Tempo = {simulTempo} €")
print(f"  Base = {simulBase} €")
print(f"  HCHP = {simulHCHP} €")
print()
