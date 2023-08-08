import sys
from chessGame import ChessGame


def main():
    if len(sys.argv) == 2 and str(sys.argv[1]) == "-sf":
        niveis = [250, 500, 1000, 1500]
        profundidades = [3, 4, 5]
        for profundidade in profundidades:
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
                    chessGame.loopGameStockFish(profundidade)
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
        chessGame.loopGameStockFish()
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
