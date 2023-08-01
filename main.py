import sys
from chessGame import ChessGame


def main():
    if len(sys.argv) == 2 and str(sys.argv[1]) == "-sf":
        print("sf")
    else:
        nomeJogador = input("Digite o nome do jogador: ")
        corSelecionada = int(
            input("Digite a cor que deseja jogar (1 para branco e 0 para preto): "))
        if corSelecionada == 1:
            chessGame = ChessGame(700, 750, 8, 8, True, nomeJogador)
        elif corSelecionada == 0:
            chessGame = ChessGame(700, 750, 8, 8, False, nomeJogador)
        chessGame.desenharTabuleiro()
        chessGame.loopGame()
        chessGame.finalizar()


if __name__ == '__main__':
    main()
