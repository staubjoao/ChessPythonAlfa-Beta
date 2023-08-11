import sys
from chessGame import ChessGame

from chessIA2 import ChessIA2
from chessIA3 import ChessIA3


def main():
    if len(sys.argv) == 2 and str(sys.argv[1]) == "-sf":
        niveis = [250, 500, 1000]
        for j in range(10):
            for nivel in niveis:
                for i in range(2):
                    corSelecionada = i
                    nomeJogador = 'stockfish_' + \
                        str(nivel) + \
                        ['_B' if corSelecionada == 1 else '_P'][0]
                    print(nomeJogador)
                    if corSelecionada == 1:
                        chessGame = ChessGame(
                            700, 750, 8, 8, True, nomeJogador, 1, nivel)
                    elif corSelecionada == 0:
                        chessGame = ChessGame(
                            700, 750, 8, 8, False, nomeJogador, 1, nivel)
                    chessGame.loopGameStockFish(5, j+1)
    elif len(sys.argv) == 3 and str(sys.argv[1]) == "-sf":
        nivel = int(sys.argv[2])
        corSelecionada = int(
            input("Digite a cor que deseja jogar (1 para branco e 0 para preto): "))
        nomeJogador = 'stockfish_' + \
            str(nivel) + \
            ['_B' if corSelecionada == 1 else '_P'][0]
        print(nomeJogador)
        if corSelecionada == 1:
            chessGame = ChessGame(700, 750, 8, 8, True, nomeJogador, 1, nivel)
        elif corSelecionada == 0:
            chessGame = ChessGame(700, 750, 8, 8, False, nomeJogador, 1, nivel)
        chessGame.loopGameStockFish(5, 1)
    elif len(sys.argv) == 2 and str(sys.argv[1]) == "-ia":
        for i in range(1):
            # IA V2 jogando com as pretas
            ia = ChessIA2()
            ia2 = ChessIA3()
            chessGame = ChessGame(700, 750, 8, 8, False,
                                  f"ia_v1_B_vs_ia_v2_P", 0, 0)
            chessGame.loopGameIaxIA(4, ia, ia2)

            ia = ChessIA3()
            ia2 = ChessIA2()
            chessGame = ChessGame(700, 750, 8, 8, False,
                                  f"ia_v2_B_vs_ia_v1_P", 0, 0)
            chessGame.loopGameIaxIA(3, ia, ia2)

    else:
        corSelecionada = int(
            input("Digite a cor que deseja jogar (1 para branco e 0 para preto): "))

        nomeJogador = input("Digite o nome do jogador: ")

        if corSelecionada == 1:
            chessGame = ChessGame(700, 750, 8, 8, True,
                                  nomeJogador, 0, 0)
        elif corSelecionada == 0:
            chessGame = ChessGame(700, 750, 8, 8, False,
                                  nomeJogador, 0, 0)

        chessGame.abrirTela()
        chessGame.desenharTabuleiro()
        chessGame.loopGame()
        chessGame.finalizar()


if __name__ == '__main__':
    main()
