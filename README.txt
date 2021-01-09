!!! Ce programme est fait pour fonctionner avec Python 2.7 !!!

Il sert � retrouver la cl� principale de l'AES 128 si assez de couples chiffr�s normaux / chiffr�s faut�s lui sont pass�s en entr�e (8 couples minimum sont n�cessaires)
ou seulement un sous-ensemble de la cl� du dernier tour s'il n'a pas assez de donn�es en entr�e
Il prend en param�tre un fichier (voir le fichier "input_example" dans ce m�me dossier) dont les chiffr�s normaux / faut�s sont repr�sent�s par des listes Python
et qui doivent �tre organis�es ainsi :

Chiffr� normal 1
Chiffr� faut� 1 correspondant
Chiffr� normal 2
Chiffr� faut� 2 correspondant
...
Chiffr� normal n
Chiffr� faut� n correspondant

Voir le fichier test, fonction : "test_input_in_file" ; il suffit d'aller chercher le bon fichier d'input dans la fonction "get_input_from_file", car il va actuellement chercher le fichier d'exemple ("input_example")
Il faut donc soit modifier le chemin, soit modifier le fichier d'exemple.
Il reste ensuite � appeler la fonction "test_input_in_file" dans le "main". C'est actuellement ce qu'il fait par d�faut ; "get_input_from_file" est appel�e dans une fonction qui la prend en param�tre pour la chronom�trer.
Si on a retrouv� la cl� du dernier tour en entier, on appelle ensuite la fonction qui remonte � la cl� principale de l'AES.
Le fichier "input_example2" ne contient que 6 couples � partir desquels il est possible de retrouver 12 octets de la derni�re cl� de tour.
Le fichier "input_example3" contient un nombre ill�gal de listes (non multiple de 4) et g�n�re donc une erreur.
