# -*-coding: utf8-*-

class SudokuGrid:
    """Cette classe représente une grille de Sudoku.
    Toutes ces méthodes sont à compléter en vous basant sur la documentation fournie en docstring.
    """

    @classmethod
    def from_file(cls, filename, line):
        """À COMPLÉTER!
        Cette méthode de classe crée une nouvelle instance de grille
        à partir d'une ligne contenue dans un fichier.
        Pour retourner une nouvelle instance de la classe, utilisez le premier argument ``cls`` ainsi::
            return cls(arguments du constructeur)

        :param filename: Chemin d'accès vers le fichier à lire
        :param line: Numéro de la ligne à lire
        :type filename: str
        :type line: int
        :return: La grille de Sudoku correspondant à la ligne donnée dans le fichier donné
        :rtype: SudokuGrid
        """
        file = open(str(filename), "r")                 #ouverture du fichier + cast du parametre filename en str pour eviter les erreurs
        file_lines = file.readlines()                   #Lecture du fichier
        str_gameset = file_lines[line-1].strip("\n")    #Recuperer la ligne voulu
        file.close()                                    #Fermeture du fichier
        return SudokuGrid(str_gameset)                  #Contruction et retour de la grille correspondante

    @classmethod
    def from_stdin(cls):
        """À COMPLÉTER!
        Cette méthode de classe crée une nouvelle instance de grille
        à partir d'une ligne lu depuis l'entrée standard (saisi utilisateur).
        *Variante avancée: Permettez aussi de «piper» une ligne décrivant un Sudoku.*
        :return: La grille de Sudoku correspondant à la ligne donnée par l'utilisateur
        :rtype: SudokuGrid
        """
        chaine = str(input())           #Recuperer la saisie de l'utilisateur
        return cls(chaine)              #Retour de la chiane de l'utilisateur

    def __init__(self, initial_values_str):
        """À COMPLÉTER!
        Ce constructeur initialise une nouvelle instance de la classe SudokuGrid.
        Il doit effectuer la conversation de chaque caractère de la chaîne en nombre entier,
        et lever une exception si elle ne peut pas être interprétée comme une grille de Sudoku.
        :param initial_values_str: Une chaîne de caractères contenant **exactement 81 chiffres allant de 0 à 9**,
            où ``0`` indique une case vide
        :type initial_values_str: str
        """

        if len(initial_values_str) == 81:                                                                               #Verification que la chaine fait bien 81 caractere
            try:                                                                                                        #Essaie de la creation du dictionnaire contenant les valeurs de la grille et les coordonnees
                self.sudoku_dict = {(i, j): int(initial_values_str[i + 9 * j]) for i in range(9) for j in range(9)}
            except ValueError:                                                                                          #On jete l'exception ValueError si les 81 caractere ne sont pas des chiffres
                print("Not all characters are number")
        else:
            raise ValueError("String of 81 characters expected but {} was given".format(len(initial_values_str)))        #On jete l'exception ValueError si la chaine ne fait pas 81 caracteres


    def __str__(self):
        """À COMPLÉTER!
        Cette méthode convertit une grille de Sudoku vers un format texte pour être affichée.
        :return: Une chaîne de caractère (sur plusieurs lignes...) représentant la grille
        :rtype: str
        """
        grid = ""                                                                           #Definition de la chaine de carractere pour la grille en ASCII
        spacer = "++---+---+---++---+---+---++---+---+---++\n"                              #Definition du separateur en ligne (\n permet de retourner a la ligne)
        grid += spacer.replace('-', '=')                                                    #Ajout de la permiere ligne dans la chaine (et remplacement du caratere '-' par '=' pour la 1er ligne
        row = []                                                                            #Definition de la list que l'on va utiliser pour creer les ligne
        for i in range(9):                                                                  #Boucle pour parcourrir les 9 ligne de la grille
            row = self.get_row(i)                                                           #On recupere les valeurs de la ligne n
            grid += "|| {} | {} | {} || {} | {} | {} || {} | {} | {} ||\n".format(          #On ajoute la ligne dans la chaine
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])     #pemret de prendre en compte les valeurs differents par ligne de la grille
            if (i + 1) % 3 == 0:                                                            #Tous les 3 ligne on ajoute un ligne de separation plus epaise pour avoir une delimitation visuel
                grid += spacer.replace('-', '=')
            else:                                                                           #Sinon on ajoute notre separateur
                grid += spacer

        return str(grid)                                                                    #Retour de la chaine compossant la grille en ascii

    def get_row(self, i):
        """À COMPLÉTER!
        Cette méthode extrait une ligne donnée de la grille de Sudoku.
        *Variante avancée: Renvoyez un générateur sur les valeurs au lieu d'une liste*
        :param i: Numéro de la ligne à extraire, entre 0 et 8
        :type i: int
        :return: La liste des valeurs présentes à la ligne donnée
        rtype: list of int
        """
        if i in range(9):                                                        #On verifier que la valeur saisie est bien entre 0 et 8 sinon on jete une exception
            return [self.sudoku_dict[(i, ind)] for ind in range(9)]              #On cherche toutes les valeur de la ligne, pour cela on chercher les coordonnees (i,0-9) donc on creer un liste en meme temps que l'on parcour le dictionnaire
        else:
            raise ValueError("Indice 0-9 attempt but {} was given".format(i))    #On jete l'exception de ValueError

    def get_col(self, j):
        """À COMPLÉTER!
        Cette méthode extrait une colonne donnée de la grille de Sudoku.
        *Variante avancée: Renvoyez un générateur sur les valeurs au lieu d'une liste*
        :param j: Numéro de la colonne à extraire, entre 0 et 8
        :type j: int
        :return: La liste des valeurs présentes à la colonne donnée
        :rtype: list of int
        """
        if j in range(9):
            return [self.sudoku_dict[(ind, j)] for ind in range(9)]         #On fait la meme chose ici, sauf on cherche (0-9,j)
        else:
            raise ValueError("Indice 0-9 attempt but {} was given".format(j))

    def get_region(self, reg_row, reg_col):
        """À COMPLÉTER!
        Cette méthode extrait les valeurs présentes dans une région donnée de la grille de Sudoku.
        *Variante avancée: Renvoyez un générateur sur les valeurs au lieu d'une liste*
        :param reg_row: Position verticale de la région à extraire, **entre 0 et 2**
        :param reg_col: Position horizontale de la région à extraire, **entre 0 et 2**
        :type reg_row: int
        :type reg_col: int
        :return: La liste des valeurs présentes à la colonne donnée
        :rtype: list of int
        """

        if reg_row in range(3) and reg_col in range(3):                                                                 #On verifie que l'indice donne est bien entre 0 et 2 sinon on jete un exception
            return [self.sudoku_dict[(i + reg_row * 3, j + reg_col * 3)] for i in range(3) for j in range(3)]           #Pour recuperer les coordonnees de la region, on multipli la valeur de l'indice de la colone par 3 pour obtenir les coordonnes de la case en haut a gauche de la region puis on ajoute 1 puis 2 pour obtenir les 8 autres case dans une double boucle
        else:
            raise ValueError("Indice 0-2 attempt but {} was given".format(j))


    def get_empty_pos(self):
        """À COMPLÉTER!
        Cette méthode renvoit la position des cases vides dans la grille de Sudoku,
        sous la forme de tuples ``(i,j)`` où ``i`` est le numéro de ligne et ``j`` le numéro de colonne.
        *Variante avancée: Renvoyez un générateur sur les tuples de positions ``(i,j)`` au lieu d'une liste*
        :return: La liste des valeurs présentes à la colonne donnée
        :rtype: list of tuple of int
        """
        return [(i, j) for i in range(9) for j in range(9) if self.sudoku_dict[(i, j)] == 0]        #On parcour tout le dictionaire a l'aide d'une double boucle et on chercher les valeurs 0 pour les inscrire dans une liste

    def write(self, i, j, v):
        """À COMPLÉTER!
        Cette méthode écrit la valeur ``v`` dans la case ``(i,j)`` de la grille de Sudoku.
        *Variante avancée: Levez une exception si ``i``, ``j`` ou ``v``
        ne sont pas dans les bonnes plages de valeurs*
        *Variante avancée: Ajoutez un argument booléen optionnel ``force``
        qui empêche d'écrire sur une case non vide*
        :param i: Numéro de ligne de la case à mettre à jour, entre 0 et 8
        :param j: Numéro de colonne de la case à mettre à jour, entre 0 et 8
        :param v: Valeur à écrire dans la case ``(i,j)``, entre 1 et 9
        """
        if i in range(9) and j in range(9) and v in range(1, 10) and self.sudoku_dict[(i, j)] == 0:     #On verifie que i et j sont entre 0 et 8 et que v est bien etre 1 et 10 sinon on jete l'exception correspondante
            self.sudoku_dict[(i, j)] = v                                                                #Si la valeur est a 0 on peut ecrire la valeur dans le dictionnaire
        elif i not in range(9):
            raise ValueError("Indice 0-9 attempt but {} was given".format(i))
        elif j not in range(9):
            raise ValueError("Indice 0-9 attempt but {} was given".format(j))
        elif v not in range(1, 10):
            raise ValueError("Value 1-10 attempt but {} was given".format(j))

    def copy(self):
        """À COMPLÉTER!
        Cette méthode renvoie une nouvelle instance de la classe SudokuGrid,
        copie **indépendante** de la grille de Sudoku.
        Vous pouvez utiliser ``self.__class__(argument du constructeur)``.
        *Variante avancée: vous pouvez aussi utiliser ``self.__new__(self.__class__)``
        et manuellement initialiser les attributs de la copie.*
        """

        old_grid = self.sudoku_dict                             #On copie le dictionnaire
        new_grid = self.__new__(self.__class__)                 #On cree une nouvelle grille
        new_grid.sudoku_dict = old_grid                         #On defini le dictionnaire de la copie
        return new_grid                                         #Retour de la grille