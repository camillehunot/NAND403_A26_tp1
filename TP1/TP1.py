import sys
import json
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
)


json_path = input("Donner le path du fichier Json") #mettre le lienpath

try: 
    file = open(json_path, encoding="utf-8") #ouvre le fichier 
# encoding="utf-8" sert à régler le problème des accents

    data = json.load(file) #met le fichier dans une variable

except:
    print(f"Could not")

#print(data) #vérifier si le fichier est bien load dans la console

app = QApplication([]) #ici cela doit venir avant les widgets

# >>>>>>>>> ici on va mettre en forme les bases du tableau, nbr de colonne et de ligne etc <<<<<<<


headers = list(data[0].keys()) #permet de récupérer les headers en ce basant sur la première liste(position 0), leur quantité et leur nom
#attention si data[1] ne possède pas le même nombre de key il faudrait trouver une facon de combinner les informations. 

tableau = QTableWidget() #définition de notre tableau
tableau.setRowCount(len(data)) #len data nous permet de vérifier combien de ligne en se basant sur la taille de data. Définit le nombre de ligne
tableau.setColumnCount(len(headers))#pour le moment fonctionne mais seulement si toute les ligne ont le meme nombre de key. Définit le nombre de colonne
tableau.setHorizontalHeaderLabels(headers) #définit le titre des columns



for row in range(len(data)):
    for column in range(len(headers)):
        values = data[row][headers[column]] #récupère la values présente a cette ligne et colonne
        valuesTexte = (str(values)) #permet d'inscrire les chiffres en string
        #attention nous allons devoir quand même faire une manipulation plus tard si l'on souhaite
        #trié en ordre de chiffre

        tableau.setItem(row, column, QTableWidgetItem(valuesTexte))
      #  tableau.setItem(row, len(headers), QTableWidgetItem(values))
        

    




window = QMainWindow();
window.setCentralWidget(tableau) #on ne voit pas le tableau sans cette ligne
window.show()
sys.exit(app.exec()) #important sinon la fenetre ne va jamais se fermer