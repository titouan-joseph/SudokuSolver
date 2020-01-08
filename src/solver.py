# -*-coding: utf8-*-
class SudokuSolver:
    """Cette classe permet d'explorer les solutions d'une grille de Sudoku pour la résoudre.
    Elle fait intervenir des notions de programmation par contraintes
    que vous n'avez pas à maîtriser pour ce projet."""

    def __init__(self, grid):
        """À COMPLÉTER
        Ce constructeur initialise une nouvelle instance de solver à partir d'une grille initiale.
        Il construit les ensembles de valeurs possibles pour chaque case vide de la grille,
        en respectant les contraintes définissant un Sudoku valide.
        :param grid: Une grille de Sudoku
        :type grid: SudokuGrid
        """
        self.grid = grid  # On defini la grille de la class
        self.dict_of_sol = {}  # On definit le dictionnaire pour stocker les solutions possible
        self.reduce_all_domains()  # On appel la fonction pour reduire la listes des valeurs possible

    def is_valid(self):
        """À COMPLÉTER
        Cette méthode vérifie qu'il reste des possibilités pour chaque case vide
        dans la solution partielle actuelle.
        :return: Un booléen indiquant si la solution partielle actuelle peut encore mener à une solution valide
        :rtype: bool
        """
        return (list_of_values != set() for list_of_values in
                self.dict_of_sol.values())  # On parcour le dictionnaire et on regarde qu'il existe des possibilites pour chaque case

    def is_solved(self):
        """À COMPLÉTER
        Cette méthode vérifie si la solution actuelle est complète,
        c'est-à-dire qu'il ne reste plus aucune case vide.
        :return: Un booléen indiquant si la solution actuelle est complète.
        :rtype: bool
        """

        return self.grid.get_empty_pos() == []  # On verifie que la liste des posibilites est vide

    def reduce_all_domains(self):
        """À COMPLÉTER
        Cette méthode devrait être appelée à l'initialisation
        et élimine toutes les valeurs impossibles pour chaque case vide.
        *Indication: Vous pouvez utiliser les fonction ``get_row``, ``get_col`` et ``get_region`` de la grille*
        """

        for coor in self.grid.get_empty_pos():                                                      #On parcour les coordonnees pour lesquels on cherche un valeur
            row = self.grid.get_row(coor[0])                                                        #On defini une variable avec la liste de la ligne correspondantes
            col = self.grid.get_col(coor[1])                                                        #On defini une variable avec la liste de la colone correspondantes
            reg = self.grid.get_region(coor[0] // 3, coor[1] // 3)                                  #On defini une variable avec la liste de la region correspondantes

            list_values = list(sorted(set(range(9)) - (set(row) | set(col) | set(reg))))            #On supprime a une liste qui contient toutes les valeurs possible pour un sudoku les valeurs contenu dans les lignes, colones, regions correspondantes

            self.dict_of_sol[coor] = list_values                                                    #On ajoute a notre dictionnaire la liste des valeurs trouveses

    def reduce_domains(self, last_i, last_j, last_v):
        """À COMPLÉTER
        Cette méthode devrait être appelée à chaque mise à jour de la grille,
        et élimine la dernière valeur affectée à une case
        pour toutes les autres cases concernées par cette mise à jour (même ligne, même colonne ou même région).
        :param last_i: Numéro de ligne de la dernière case modifiée, entre 0 et 8
        :param last_j: Numéro de colonne de la dernière case modifiée, entre 0 et 8
        :param last_v: Valeur affecté à la dernière case modifiée, entre 1 et 9
        :type last_i: int
        :type last_j: int
        :type last_v: int
        """

        for coor, values in self.dict_of_sol.items():                                                                   #On parcour notre dictionnaire
            region_element = (coor[0] // 3, coor[1] // 3)                                                               #On definit les coordonne de notre region
            region_last = (last_i // 3, last_j // 3)                                                                    #On definit les coordonne de la derniere region
            if last_v in values and (coor[0] == last_i or coor[1] == last_j or (region_element == region_last)):      #On verifie que la valeur etait bien dans la liste des posibilites et que les coordonnees coincide bien
                values.remove(last_v)                                                                                   #On supprime la valeur dans la liste

    def commit_one_var(self):
        """À COMPLÉTER
        Cette méthode cherche une case pour laquelle il n'y a plus qu'une seule possibilité.
        Si elle en trouve une, elle écrit cette unique valeur possible dans la grille
        et renvoie la position de la case et la valeur inscrite.
        :return: Le numéro de ligne, de colonne et la valeur inscrite dans la case
        ou ``None`` si aucune case n'a pu être remplie.
        :rtype: tuple of int or None
        """

        for coor, values in self.dict_of_sol.items():               #On parcour notre dictionnaire
            if len(values) == 1:                                    #Si la lsite des valeurs est egale a 1, il y a qu'une valeur possible donc on l'ecrit
                self.grid.write(coor[0], coor[1], values[0])        #Ecriture de la valeur dans la grille
                return coor[0], coor[1], values[0]
        return None

    def solve_step(self):
        """À COMPLÉTER
        Cette méthode alterne entre l'affectation de case pour lesquelles il n'y a plus qu'une possibilité
        et l'élimination des nouvelles valeurs impossibles pour les autres cases concernées.
        Elle répète cette alternance tant qu'il reste des cases à remplir,
        et correspond à la résolution de Sudokus dits «simple».
        *Variante avancée: en plus de vérifier s'il ne reste plus qu'une seule possibilité pour une case,
        il est aussi possible de vérifier s'il ne reste plus qu'une seule position valide pour une certaine valeur
        sur chaque ligne, chaque colonne et dans chaque région*
        """

        while len(self.grid.get_empty_pos()) > 0:       #Tant que la liste des cases vide existe
            res = self.commit_one_var()
            if res is not None:                         #On regarde s'il y a des valeurs possible
                (i, j, v) = res                         #Si oui on reduit le domaine des posibilites de la ligne, colone et region correspondante
                self.reduce_domains(i, j, v)
                del self.dict_of_sol[(i, j)]            #On supprime cette valeur du dictionnaire
            else:
                break

    def branch(self):
        """À COMPLÉTER
        Cette méthode sélectionne une variable libre dans la solution partielle actuelle,
        et crée autant de sous-problèmes que d'affectation possible pour cette variable.
        Ces sous-problèmes seront sous la forme de nouvelles instances de solver
        initialisées avec une grille partiellement remplie.
        *Variante avancée: Renvoyez un générateur au lieu d'une liste.*
        *Variante avancée: Un choix judicieux de variable libre,
        ainsi que l'ordre dans lequel les affectations sont testées
        peut fortement améliorer les performances de votre solver.*
        :return: Une liste de sous-problèmes ayant chacun une valeur différente pour la variable choisie
        :rtype: list of SudokuSolver
        """

        list_sudokusolver = []                                                                  #On defini la liste des SudokuSolever
        self.dict_of_sol = sorted(self.dict_of_sol.items(), key=lambda t: len(t[1]))            #On organise le dictionnaire enn fonction des listes de valeurs les plus petite
        coor_min = next(iter(self.dict_of_sol))[0]                                              #On defini les coordonnee ou il y a le moins de valeurs

        for values in next(iter(self.dict_of_sol))[1]:                                          #On parcour la liste des valeurs possible
            newGrid = self.grid.copy()                                                          #On copie la grille actuelle
            newGrid.write(coor_min[0], coor_min[1], values)                                     #On ecrit dans cette grille la valeur de la possibilité
            sous_probleme = self.__class__(newGrid)                                             #On creer son solver
            list_sudokusolver.append(sous_probleme)                                             #On l'ajoute a la liste

        return list_sudokusolver

    def solve(self):
        """
        Cette méthode implémente la fonction principale de la programmation par contrainte.
        Elle cherche d'abord à affiner au mieux la solution partielle actuelle par un appel à ``solve_step``.
        Si la solution est complète, elle la retourne.
        Si elle est invalide, elle renvoie ``None`` pour indiquer un cul-de-sac dans la recherche de solution
        et déclencher un retour vers la précédente solution valide.
        Sinon, elle crée plusieurs sous-problèmes pour explorer différentes possibilités
        en appelant récursivement ``solve`` sur ces sous-problèmes.
        :return: Une solution pour la grille de Sudoku donnée à l'initialisation du solver
        (ou None si pas de solution)
        :rtype: SudokuGrid or None
        """

        self.solve_step()                       #On commence par regarder s'il est possible de resoudre le sudoku sans creer de sous problemes
        if self.is_solved():
            return self.grid                    #Si c'est possible on le retourne
        elif self.is_valid():                   #Sinon on regarde si on peut toujours resoudre le sudoku
            for element in self.branch():       #On recupere les sous probleme pour essayer des les resoudre
                s = element.solve()
                if s is not None:               #Si le probleme est resolut on le retourne
                    return s
            return None
        else:
            return None