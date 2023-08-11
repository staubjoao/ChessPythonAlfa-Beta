# comentado!
import random
import chess

from pesto import verificaEstagio, avaliarPeca, avaliarCaptura


class Avaliacao2:

    # função que organiza os movimentos de forma simples
    def organizarMovimento(self, tabuleiro):
        movimentos = []
        movimentos_captura = []

        # para cada movimento presente no tabuleiro
        for movimento in tabuleiro.legal_moves:
            # armazena ele no vetor de capturas, se for um movimento de captura
            if tabuleiro.is_capture(movimento):
                movimentos_captura.append(movimento)
            # caso contrario armazena no vetor de movimentos de não captura
            else:
                movimentos.append(movimento)

        # aleatoriza os dois vetores
        random.shuffle(movimentos_captura)
        random.shuffle(movimentos)
        # retorna com os movimentos de captura vindo primeiro
        return movimentos_captura + movimentos

    # função que ordena os movimentos de captura
    def ordenarMovimentoQuiescence(self, tabuleiro):
        estagio = verificaEstagio(tabuleiro)
        # filter only important moves for quiescence search
        movimentos_captura = filter(lambda movimento: tabuleiro.is_zeroing(
            movimento) or tabuleiro.gives_check(movimento), tabuleiro.legal_moves)
        # ordena os movimentos baseado na sua importancia, utilizando a
        movimentos = sorted(movimentos_captura, key=lambda movimento: self.avaliarMovimento(
            tabuleiro, movimento, estagio), reverse=(True if tabuleiro.turn == chess.BLACK else False))
        return movimentos

    # função que avalia um movimento com base do estagio atual do jogo
    def avaliarMovimento(self, tabuleiro, move, estagio):
        valor_movimento = 0

        # avalia as posiçẽos do movimento
        movimento_de = avaliarPeca(
            tabuleiro, move.from_square, estagio)
        movimento_para = avaliarPeca(
            tabuleiro, move.to_square, estagio)

        valor_movimento += movimento_para - movimento_de

        # avalia o movimento de captura
        if tabuleiro.is_capture(move):
            valor_movimento += avaliarCaptura(
                tabuleiro, move, estagio)

        # se a vez for das brancas retorna o valor positivo, se for das pretas, retorna negativo
        return -valor_movimento if tabuleiro.turn else valor_movimento
