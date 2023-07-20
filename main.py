
import numpy as np
import time

from chessGame import ChessGame


def main():
    chessGame = ChessGame(700, 700, 8, 8)
    chessGame.desenharTabuleiro()
    chessGame.loopGame()
    chessGame.finalizar()


main()
