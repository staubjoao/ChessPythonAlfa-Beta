import sys
from chessGame import ChessGame


def main():
    if len(sys.argv) == 2 and str(sys.argv[1]) == "-sf":
        print("sf")
    else:
        nomeJogador = input("Digite o nome do jogador: ")
        corSelecionada = int(
            input("Digite a cor que deseja jogar (1 para branco e 0 para preto): "))
        vsStockfish = int(input("Ativar Stockfish? (1 para sim e 0 para não): "))
        if corSelecionada == 1:
            chessGame = ChessGame(700, 750, 8, 8, True, nomeJogador, vsStockfish)
        elif corSelecionada == 0:
            chessGame = ChessGame(700, 750, 8, 8, False, nomeJogador, vsStockfish)
        chessGame.desenharTabuleiro()
        chessGame.loopGame()
        chessGame.finalizar()


if __name__ == '__main__':
    main()
