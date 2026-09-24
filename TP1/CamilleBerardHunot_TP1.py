import sys
import json
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QLabel,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)
from PySide6.QtCore import Qt #permet de configurer le comportement de facon précise des widgets pyside6, necessaire pour trier les colonnes.

from pathlib import Path #permet de récupérer le nom du fichier en se basant sur le path et autres (tailles etc)


app = QApplication([]) #ici cela doit venir avant les widgets

json_path = input("Donner le path du fichier Json") #mettre le lienpath 

def open_json():

    #>>>>>>>> permet d'ouvrir et de load le .json en toute sécurité
    try: 
        file = open(json_path, encoding="utf-8") #ouvre le fichier 
    # encoding="utf-8" sert à régler le problème des accents

        data_load = json.load(file) #met le fichier dans une variable

    except:
        print(f"Could not")

    #print(data) #vérifier si le fichier est bien load dans la console

    return data_load
def info_json(json_path,data):
    # récupérer le nom du fichier
    path_fichier = Path(json_path)
    nom_fichier = Path(path_fichier).name

    #récupérer la taille du fichier
    size_octets = path_fichier.stat().st_size # permet de stocker la taille du fichier en octe dans une variable
    size_ko = round(size_octets / 1024, 2)
    #round permet d'arrondir la valeur, on divise par 1024 car il y a cette quantité d'octet dans un ko, le ,2 sert a indiquer le nombre après la virgule

    #nombre d'élément en try pour éviter les crashs
    try:
        element_number = len(data)

    except:  

        element_number = "error in element_number"  

    return (nom_fichier, size_ko, element_number)

data = open_json() #mise en variable du load  json

name, size, element = info_json(json_path,data) #initialise des variable en groupe car elles résultent d'un return de la même fonction
print(name)
print(size)
print(element)

tableau = QTableWidget() #définition de notre tableau
headers = list(data[0].keys()) #permet de récupérer les headers en ce basant sur la première liste(position 0), leur quantité et leur nom
#attention si data[1] ne possède pas le même nombre de key il faudrait trouver une facon de combinner les informations. 

tableau.setRowCount(len(data)) #len data nous permet de vérifier combien de ligne en se basant sur la taille de data. Définit le nombre de ligne
tableau.setColumnCount(len(headers))#pour le moment fonctionne mais seulement si toute les ligne ont le meme nombre de key. Définit le nombre de colonne
tableau.setHorizontalHeaderLabels(headers) #définit le titre des columns
tableau.setSortingEnabled(True)#autorise a trier le tableau en fonction des colonnes
tableau.sortByColumn(0, Qt.SortOrder.AscendingOrder) #trier en ordre croissant la première ligne de facon automatique



#>>>>>>>>> mise en forme

main_window = QWidget() #fenetre principale
main_window.setWindowTitle("TP1 Camille B Hunot")
main_window.resize(800, 500) # déterminer la taille de la fenetre principale

#main box
main_box = QVBoxLayout()
main_window.setLayout(main_box)#mettre le main box dans notre main window

#titre-name
titre = QLabel(f"Visualisation de : {name}") #affiche le nom du fichier visualisé en en-tete
titre.setStyleSheet("font-size : 16px; font-weight: bold;")
main_box.addWidget(titre)#place le titre dans la main box


#>>>>>>>>>>>>>>>>>>>>>>>>>>>> recherche <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

recherche_box = QHBoxLayout()
recherche_ligne = QLineEdit()
recherche_ligne.setPlaceholderText("Rechercher")
recherche_box.addWidget(recherche_ligne) #ajouter la prise de texte dans notre boite de recherche
main_box.addLayout(recherche_box) #ajouter notre boite de recherche dans notre main box

def recherche(texte_cherche):
    print("help")
    texte_recherche = texte_cherche.lower() #permet d'ignorer les majuscules

    for row in range(tableau.rowCount()):
        texte_true = False #on commence par dire que la ligne ne correspond pas

        for column in range(tableau.columnCount()):

            # on sort la valeur pour la comparer, on doit refaire directement ici sinon on aura des problème avec la fonction text.changed
            row_value = data[row]
            key_variable = headers[column]
            values = row_value.get(key_variable)


            if values and texte_recherche in str(values).lower():
                texte_true = True
                break #si c'est vrai on sort de la boucle car on a une correspondance
            else:
                texte_true = False


        if texte_true:
            tableau.setRowHidden(row, False) #si c'est vrai on cache pas la ligne
        else:
            tableau.setRowHidden(row, True)   #si le texte ne correspond pas on cache la ligne      

recherche_ligne.textChanged.connect(recherche) #permet de chercher a chaque changement de texte


#>>>>>>>>>>>>>>>>>>>>>>> ajouter le tableau dans la main box <<<<<<<<<<<<<<<<<<<<<<

main_box.addWidget(tableau)

#>>>>>>>>>>>>>>>>>>>>>>> ajouter autres infos <<<<<<<<<<<<<<<<<<<<<<

texte_info = QLabel(f"Nom du fichier : {name}\ntaille : {size} ko \nQuantité : {element}")
main_box.addWidget(texte_info)

#>>>>>>>>>>>>>>>>>>>>>>> Mettre les values dans nos cases de <<<<<<<<<<<<<<<<<<<<<<

for row in range(len(data)):
    for column in range(len(headers)):

        row_value = data[row]
        key_variable = headers[column]

        cell_values = row_value.get(key_variable) #obtenir la valeur d'une cellule en se basant sur la row et la column

        values = QTableWidgetItem() #création d'un objet vide

#ici on regarde si la value est un int/float ou un string, et défini en conséquence la variable values
#Permet de considérer les nombres de la bonne facon pour le tri alphabétique
        if isinstance(cell_values, (int,float)): #isinstance retourne vrai si un objet est du type entré dans le paramètre
            values.setData(Qt.ItemDataRole.DisplayRole, cell_values)
        else:
            values = cell_values

        tableau.setItem(row, column, QTableWidgetItem(values)) #permet de placé la value dans le tableau
        
#>>>>> voir + fermeture de l'interface <<<<<<
main_window.show()
sys.exit(app.exec()) #important sinon la fenetre ne va jamais se fermer