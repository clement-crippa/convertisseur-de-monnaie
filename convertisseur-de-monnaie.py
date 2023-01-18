import tkinter as tk
from tkinter import *
import requests
from datetime import datetime
import csv


# Fonction permettant de convertir un montant d'une monnaie a une autre
def convertir():
    try:
        montant = float(entree_montant.get())
        monnaie_depart = var_depart.get()
        monnaie_cible = var_cible.get()
        if monnaie_depart in taux and monnaie_cible in taux:
            conversion = montant / taux[monnaie_depart] * taux[monnaie_cible]
            date_heure = datetime.now()
            taux_actuel = montant, monnaie_depart, conversion, monnaie_cible, date_heure
            sauvegarde = open("Historique.csv", "a", newline="")
            ecriture = csv.writer(sauvegarde)
            ecriture.writerow(taux_actuel)
            sauvegarde.close()
            if monnaie_cible == "EUR":
                label_resultat.config(text=f"{conversion} €")
            elif monnaie_cible == "USD" or monnaie_cible == "MXN":
                label_resultat.config(text=f"{conversion} $")
            elif monnaie_cible == "JPY":
                label_resultat.config(text=f"{conversion} ¥")
            elif monnaie_cible == "GBP":
                label_resultat.config(text=f"{conversion} £")
            elif monnaie_cible == "THB":
                label_resultat.config(text=f"{conversion} ฿")
            elif monnaie_cible == "DKK":
                label_resultat.config(text=f"{conversion} Kr")
            elif monnaie_cible == "DZD":
                label_resultat.config(text=f"{conversion} DA")
            elif monnaie_cible == "KRW":
                label_resultat.config(text=f"{conversion} ₩")
            else:
                label_resultat.config(text=f"{conversion} {monnaie_cible}")
        else:
            label_resultat.config(
                text="Conversion impossible, devise introuvable ou manquante. Respectez le format ISO 4217 pour ajouter de nouvelle devise")
    except ValueError:
        label_resultat.config(text="Veuillez entrer un montant valide.")


# Fonction permettant d'afficher le contenue du fichier CSV
def historique_live():
    live = open("Historique.csv", "r")
    live = live.read()
    return live


# Fonction permettant l'affichage de la fenêtre historique
def affichage_live():
    historique = Tk()
    historique.title("Historique")
    contenue_historique = historique_live()
    label_historique = tk.Label(historique, text=contenue_historique)
    label_historique.pack()
    historique.mainloop()


# Fonction permetttant de mettre a jour le taux de change
def mettre_a_jour_taux():
    global taux
    # Demande a l'API les donnée live (Actualisation toutes les heures)
    reponse = requests.get("https://openexchangerates.org/api/latest.json",
                           params={"app_id": "8eb93f55bdd3489189795ec14ff29965"})
    donnees = reponse.json()
    taux = {
        # Monnaie en format ISO 4217
        "EUR": donnees["rates"]["EUR"],
        "USD": donnees["rates"]["USD"],
        "JPY": donnees["rates"]["JPY"],
        "GBP": donnees["rates"]["GBP"],
        "THB": donnees["rates"]["THB"],
        "DKK": donnees["rates"]["DKK"],
        "DZD": donnees["rates"]["DZD"],
        "KRW": donnees["rates"]["KRW"],
        "MXN": donnees["rates"]["MXN"],
        "TND": donnees["rates"]["TND"],
    }


# Fenêtre du programme
fenetre = tk.Tk()
fenetre.title("Convertisseur de monnaies")

# Indication d'entrer un montant
label_montant = tk.Label(fenetre, text="Entrez un montant :")
label_montant.pack()

# Montant
entree_montant = tk.Entry(fenetre)
entree_montant.pack()

# Indication sélectionner une monnaie de départ
label_depart = tk.Label(fenetre, text="Sélectionnez une monnaie de départ :")
label_depart.pack()

# Monnaie de départ sélectionnée par défaut
var_depart = tk.StringVar(value="EUR")

# Menu déroulant pour la sélection de la monnaie de départ
menu_depart = tk.OptionMenu(fenetre, var_depart, "EUR", "USD", "JPY", "GBP", "THB", "DKK", "DZD", "KRW", "MXN", "TND")
menu_depart.pack()

# Indication sélectionner une monnaie cible
label_cible = tk.Label(fenetre, text="Sélectionnez en quoi voulez-vous la convertir :")
label_cible.pack()

# Monnaie cible sélectionnée par défaut
var_cible = tk.StringVar(value="USD")

# Menu déroulant pour la sélection de la monnaie cible
menu_cible = tk.OptionMenu(fenetre, var_cible, "EUR", "USD", "JPY", "GBP", "THB", "DKK", "DZD", "KRW", "MXN", "TND")
menu_cible.pack()

# Bouton pour lancer la conversion
bouton_convertir = tk.Button(fenetre, bg="#4296d7", text="Convertir", command=convertir)
bouton_convertir.pack()

# Bouton pour mettre à jour les taux de change
bouton_maj = tk.Button(fenetre, bg="#4254fc", text="Mettre à jour les taux", command=mettre_a_jour_taux)
bouton_maj.pack()

# Affichage du résultat
label_resultat = tk.Label(fenetre, text="")
label_resultat.pack()

# Mettre à jour les taux de change au lancement de l'applications
mettre_a_jour_taux()
# Bouton Historique
bouton_historique = tk.Button(fenetre, bg="Gray", text="Historique", command=affichage_live)
bouton_historique.pack()

fenetre.mainloop()
