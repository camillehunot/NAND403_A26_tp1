import sys
import json
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
)
from PySide6.QtCore import Qt #permet de configurer le comportement de facon précise des widgets pyside6
#ex : necessaire pour trier les colonnes.


json_path = input("Donner le path du fichier Json") #mettre le lienpath



#>>>>>>>> permet d'ouvrir et de load le .json en toute sécurité
try: 
    file = open(json_path, encoding="utf-8") #ouvre le fichier 
# encoding="utf-8" sert à régler le problème des accents

    data = json.load(file) #met le fichier dans une variable

except:
    print(f"Could not")

#print(data) #vérifier si le fichier est bien load dans la console



# >>>>>>>>> ici on va mettre en forme les bases du tableau, nbr de colonne et de ligne etc <<<<<<<
app = QApplication([]) #ici cela doit venir avant les widgets


headers = list(data[0].keys()) #permet de récupérer les headers en ce basant sur la première liste(position 0), leur quantité et leur nom
#attention si data[1] ne possède pas le même nombre de key il faudrait trouver une facon de combinner les informations. 


tableau = QTableWidget() #définition de notre tableau
tableau.setRowCount(len(data)) #len data nous permet de vérifier combien de ligne en se basant sur la taille de data. Définit le nombre de ligne
tableau.setColumnCount(len(headers))#pour le moment fonctionne mais seulement si toute les ligne ont le meme nombre de key. Définit le nombre de colonne
tableau.setHorizontalHeaderLabels(headers) #définit le titre des columns
tableau.setSortingEnabled(True)#autorise a trier le tableau en fonction des colonnes
tableau.sortByColumn(0, Qt.SortOrder.AscendingOrder) #trier en ordre croissant la première ligne de facon automatique



#>>>>>>>>>> Mettre les values dans nos cases <<<<<<
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


       # valuesTexte = (str(values)) #permet d'inscrire les chiffres en string
        #attention nous allons devoir quand même faire une manipulation plus tard si l'on souhaite
        #trié en ordre de chiffre

        tableau.setItem(row, column, QTableWidgetItem(values))
      #  tableau.setItem(row, len(headers), QTableWidgetItem(values))
        

#>>>>> initialisation et fermeture de l'interface <<<<<<
window = QMainWindow();
window.setCentralWidget(tableau) #on ne voit pas le tableau sans cette ligne
window.show()
sys.exit(app.exec()) #important sinon la fenetre ne va jamais se fermer