import chess
import time

from avaliacao2 import Avaliacao2
from pesto import Pesto


class ChessIA3:
    def __init__(self):
        self.avaliacao_tabuleiro = Avaliacao2()
        self.pesto_funcs = Pesto()

        self.nodes = 0
        self.tempo = 0

    # função que seleciona o movimento, recebe o tabuleiro, e a profundidade da busca
    def selecionarMovimento(self, profundidade, tabuleiro):
        # inicial o node e o tempo
        self.nodes = 0
        t0 = time.time()

        # verifica se começa maximando ou minimizando o tabuleiro
        maximizando = tabuleiro.turn == chess.WHITE
        # inicial o melhor movimento com -infinito
        melhor_avaliacao = -float("inf")
        # se for minimizar declara como infinito
        if not maximizando:
            melhor_avaliacao = float("inf")
        # armazena os movimentos ordenados
        movimentos = self.avaliacao_tabuleiro.organize_moves(tabuleiro)
        # inicializa o melhor movimento encontrado como o primeiro elemento da lista
        melhor_movimento_encontrado = movimentos[0]

        # para todos os movimentos possiveis realiza a poda
        for movimento in movimentos:
            # adiciona o movimento no tabuleiro
            tabuleiro.push(movimento)
            # verifica o possivel empate
            if tabuleiro.can_claim_draw():
                avaliacao = 0.0
            # se não pode empatar avalia a jogada
            else:
                # faz a chamada da função minmax
                avaliacao = - \
                    self.minimax(profundidade-1, tabuleiro, -
                                 float("inf"), float("inf"), not maximizando)
            # retira o movimento do tabuleiro
            tabuleiro.pop()
            # avalia a jogada, se for melhor do que a jogada atual atualiza
            if maximizando and avaliacao >= melhor_avaliacao:
                melhor_avaliacao = avaliacao
                melhor_movimento_encontrado = movimento
            elif not maximizando and avaliacao <= melhor_avaliacao:
                melhor_avaliacao = avaliacao
                melhor_movimento_encontrado = movimento

        # coleta o tempo para estatistica
        self.tempo = time.time() - t0
        # retorna a melhor jogada e as estatiscas, nodes acessados e tempo
        return melhor_movimento_encontrado, (self.nodes, self.tempo)

    # função para persistir jogadas caso encontre uma jogada de captura
    def quiesce(self, tabuleiro, alpha, beta, profundidade):
        self.nodes += 1
        if tabuleiro.is_stalemate():
            return 0

        if tabuleiro.is_checkmate():
            return -float("inf")

        stand_pat = self.pesto_funcs.board_evaluation(tabuleiro)
        # para não rodar infinitamente
        if profundidade == 0:
            return stand_pat

        # beta-cutoff
        if stand_pat >= beta:
            return beta

        # alpha update
        if stand_pat > alpha:
            alpha = stand_pat

        # para cada movimento atual faz
        movimentos = self.avaliacao_tabuleiro.organize_moves_quiescence(
            tabuleiro)
        for movimento in movimentos:
            # verifica se o movimento é de captura
            if tabuleiro.is_capture(movimento):
                # se sim realiza ele
                tabuleiro.push(movimento)
                # faz a chamada recursiva da função, trocando o beta por alpha e alpha por beta, e negando seus valores
                avalicao = -self.quiesce(tabuleiro, -
                                         beta, -alpha, profundidade-1)
                # remove a jogada
                tabuleiro.pop()
                # avalia, se a avaliação for maior ou igual a beta retorna beta
                if avalicao >= beta:
                    return beta
                # caso a avaliação seja maior doque alpha, alpha passa a valer a avaliação
                if avalicao > alpha:
                    alpha = avalicao
        # retorna alpha no final
        return alpha

    # função chave da ingeligencia, minmax com poda alphabeta
    def minimax(self, profundidade, tabuleiro, alpha, beta, maximizando):
        self.nodes += 1

        # verifica se o tabuleiro está em checkmate, se estiver retorna infinto ou -infinito, depende se estiver maximizando ou minimizando
        if tabuleiro.is_checkmate():
            if maximizando:
                return -float("inf")
            else:
                return float("inf")

        if tabuleiro.is_stalemate():
            return 0

        # chegou em um nó folha faz a chamada da função quiesce para verificar as jogadas de captura
        if profundidade == 0:
            return self.quiesce(tabuleiro, alpha, beta, 3)
            # return self.avaliacao_tabuleiro.avalieTabuleiro(tabuleiro)

        # se estiver maximizando
        if maximizando:
            # declada o melhor movimento como -infinito
            melhor_movimento = -float("inf")
            movimentos = self.avaliacao_tabuleiro.organize_moves(tabuleiro)
            # para cada movimento
            for movimento in movimentos:
                # realiza o movimento
                tabuleiro.push(movimento)
                # melhor movimento recebe o maior valor entre o melhor_movimento e a chamada recursiva da função
                melhor_movimento = \
                    max(
                        melhor_movimento,
                        self.minimax(profundidade - 1, tabuleiro,
                                     alpha, beta, not maximizando)
                    )
                # retira o movimento
                tabuleiro.pop()

                # alpha recebe o maior valor entre alpha e melhor_movimento
                alpha = max(alpha, melhor_movimento)

                # se beta é menor ou igual a alpha realiza a poda
                if beta <= alpha:
                    return melhor_movimento
            # retorna o melhor movimento no final
            return melhor_movimento
        # se estiver minimizando
        else:
            # declada o melhor movimento como infinito
            melhor_movimento = float("inf")
            movimentos = self.avaliacao_tabuleiro.organize_moves(tabuleiro)
            # para cada movimento
            for movimento in movimentos:
                # realiza o movimento
                tabuleiro.push(movimento)
                # melhor movimento recebe o menor valor entre o melhor_movimento e a chamada recursiva da função
                melhor_movimento = \
                    min(
                        melhor_movimento,
                        self.minimax(profundidade - 1, tabuleiro,
                                     alpha, beta, not maximizando)
                    )
                # retira o movimento
                tabuleiro.pop()

                # beta recebe o menor valor entre beta e melhor_movimento
                beta = min(beta, melhor_movimento)

                # se beta é menor ou igual a alpha realiza a poda
                if beta <= alpha:
                    return melhor_movimento
            # retorna o melhor movimento no final
            return melhor_movimento
