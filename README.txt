!!! Ce programme est fait pour fonctionner avec Python 2.7 !!!

Il sert à retrouver la clé principale de l'AES 128 si assez de couples chiffrés normaux / chiffrés fautés lui sont passés en entrée (8 couples minimum sont nécessaires)
ou seulement un sous-ensemble de la clé du dernier tour s'il n'a pas assez de données en entrée
Il prend en paramètre un fichier (voir le fichier "input_example" dans ce même dossier) dont les chiffrés normaux / fautés sont représentés par des listes Python
et qui doivent être organisées ainsi :

Chiffré normal 1
Chiffré fauté 1 correspondant
Chiffré normal 2
Chiffré fauté 2 correspondant
...
Chiffré normal n
Chiffré fauté n correspondant

Voir le fichier test, fonction : "test_input_in_file" ; il suffit d'aller chercher le bon fichier d'input dans la fonction "get_input_from_file", car il va actuellement chercher le fichier d'exemple ("input_example")
Il faut donc soit modifier le chemin, soit modifier le fichier d'exemple.
Il reste ensuite à appeler la fonction "test_input_in_file" dans le "main". C'est actuellement ce qu'il fait par défaut ; "get_input_from_file" est appelée dans une fonction qui la prend en paramètre pour la chronométrer.
Si on a retrouvé la clé du dernier tour en entier, on appelle ensuite la fonction qui remonte à la clé principale de l'AES.
Le fichier "input_example2" ne contient que 6 couples à partir desquels il est possible de retrouver 12 octets de la dernière clé de tour.
Le fichier "input_example3" contient un nombre illégal de listes (non multiple de 4) et génère donc une erreur.
