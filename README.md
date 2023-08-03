# Description
Ce programme permet de simuler le coût total d'une période de consommation électrique, selon 3 forfaits EDF :
 - l'abonnement base
 - l'abonnement Heures Creuses / Heures Pleines
 - l'abonnement Tempo

Il nécessite d'entrer un fichier CSV de la consommation, au pas horaire (et même demi-horaire), disponible sur le site d'Enedis (quand il fonctionne -_-)

Il prend en compte les jours bleu/blanc/rouge du tarif TEMPO depuis le 01/09/2014

# Les fichiers utilisés :
AnalyseConso.py : le programme, à exécuter sans paramètres
consoexemple.csv : fichier d'exemple à fournir au programme pour calculer les prix
calBAR.csv : historique des jours et leur couleur associée pour le forfait TEMPO

# Ressources utilisées :
Tarifs EDF, disponibles à l'adresse suivante https://particulier.edf.fr/content/dam/2-Actifs/Documents/Offres/Grille_prix_Tarif_Bleu.pdf
Les tarifs sont en dur dans le fichier Python

Fichier calBAR.csv, généré à partir des données sur les jours Bleu/blanc/rouge mises à disposition à https://www.rte-france.com/eco2mix/telecharger-les-indicateurs

Fichier consoexemple.csv
Un fichier d'1 an de consommation, fourni par @MathieuMf (https://twitter.com/MathieuMf)

# Vous voulez contribuer ?
N'hésitez pas. Un nettoyage du code, une refactorisation, une interface graphique, une intégration web, une extension à d'autres forfaits, ou même une critique constructive, tout sera apprécié :-)

Merci Nicolas Automme / @autommen (https://twitter.com/autommen ) pour l'idée originale
