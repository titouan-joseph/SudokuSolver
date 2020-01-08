#!/usr/bin/env python3
from grid import SudokuGrid
import sys


def main():

    if( len(sys.argv) == 1):
        sudoku_line = input("(pas d'args) \n Saisir manuellement la grille (81 caratere de 0 a 9) : \n")
        sudoku = SudokuGrid(sudoku_line)
    elif ( len(sys.argv) == 3):
            if ( sys.argv[1].endswith('.txt') and sys.argv[2].isdigit()):
                sudoku = SudokuGrid.from_file(sys.argv[1], int(sys.argv[2]))
            else:
                sudoku_line = input("(pas bon args) \n Saisir manuellement la grille (81 caratere de 0 a 9) : \n")
                sudoku = SudokuGrid(sudoku_line)
    else:
        raise NameError("2 args excepted but {} were given".format(len(sys.argv)-1))
    return sudoku


if __name__ == "__main__":
    sudoku = main()
    while True:
        print(sudoku)
        i = int(input ("Numero de la ligne \n"))
        j = int(input ("Numero de la colonne \n"))
        v = int(input ("Valeur a inscrire  \n"))
        if(v in range(9)):
            sudoku.write(i,j,v)
        else:
            v = int(input("Valeur interdite, veuillez saisir un chiffre entre 0 et 9 \n"))


