import sys
from chessGame import ChessGame


def main():
    if len(sys.argv) == 2 and str(sys.argv[1]) == "-sf":
        print("sf")
    else:
        vsStockfish = int(input("Ativar Stockfish? (1 para sim e 0 para não): "))
        corSelecionada = int(
            input("Digite a cor que deseja jogar (1 para branco e 0 para preto): "))
        
        if vsStockfish == 1:
            nivelStockfish = int(input("Digite o nível de habilidade do Stockfish: "))
            nomeJogador = 'stockfish_' + str(nivelStockfish) + ['_B' if corSelecionada == 1 else '_P'][0]
        else:
            nivelStockfish = 2000
            nomeJogador = input("Digite o nome do jogador: ")

        if corSelecionada == 1:
            chessGame = ChessGame(700, 750, 8, 8, True, nomeJogador, vsStockfish, nivelStockfish)
        elif corSelecionada == 0:
            chessGame = ChessGame(700, 750, 8, 8, False, nomeJogador, vsStockfish, nivelStockfish)

        chessGame.desenharTabuleiro()
        chessGame.loopGame()
        chessGame.finalizar()


if __name__ == '__main__':
    main()
