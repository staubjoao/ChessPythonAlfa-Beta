import chess
import numpy as np
import time


class ChessIA:
    def __init__(self):
        self.tabela_transposicao = {}

        self.peaoTabuleiro = [
            0, 0, 0, 0, 0, 0, 0, 0,
            5, 10, 10, -20, -20, 10, 10, 5,
            5, -5, -10, 0, 0, -10, -5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, 5, 10, 25, 25, 10, 5, 5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0, 0, 0, 0, 0, 0, 0, 0]

        self.cavaloTabuleiro = [
            -40, -10, - 5, - 5, - 5, - 5, -10, -40,
            - 5, 5, 5, 5, 5, 5, 5, - 5,
            - 5, 5, 10, 15, 15, 10, 5, - 5,
            - 5, 5, 10, 15, 15, 10, 5, - 5,
            - 5, 5, 10, 15, 15, 10, 5, - 5,
            - 5, 5, 8, 8, 8, 8, 5, - 5,
            - 5, 0, 5, 5, 5, 5, 0, - 5,
            -50, -20, -10, -10, -10, -10, -20, -50]

        self.bispoTabuleiro = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10, 0, 10, 10, 10, 10, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20]

        self.torreTabuleiro = [
            0, 0, 0, 5, 5, 0, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0]

        self.rainhaTabuleiro = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 5, 5, 5, 5, 5, 0, -10,
            0, 0, 5, 5, 5, 5, 0, -5,
            -5, 0, 5, 5, 5, 5, 0, -5,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20]

        self.reiTabuleiro = [
            20, 30, 10, 0, 0, 10, 30, 20,
            20, 20, 0, 0, 0, 0, 20, 20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30]

    def getMovimentos(self, tabuleiro):
        return tabuleiro.legal_moves

    def avaliarTabuleiro(self, tabuleiro):
        if tabuleiro.is_checkmate():
            if tabuleiro.turn:
                return float('-inf')
            else:
                return float('inf')
        if tabuleiro.is_insufficient_material() or tabuleiro.is_stalemate():
            return 0

        wp = len(tabuleiro.pieces(chess.PAWN, chess.WHITE))
        bp = len(tabuleiro.pieces(chess.PAWN, chess.BLACK))
        wn = len(tabuleiro.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(tabuleiro.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(tabuleiro.pieces(chess.BISHOP, chess.WHITE))
        bb = len(tabuleiro.pieces(chess.BISHOP, chess.BLACK))
        wr = len(tabuleiro.pieces(chess.ROOK, chess.WHITE))
        br = len(tabuleiro.pieces(chess.ROOK, chess.BLACK))
        wq = len(tabuleiro.pieces(chess.QUEEN, chess.WHITE))
        bq = len(tabuleiro.pieces(chess.QUEEN, chess.BLACK))

        material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * \
            (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)

        peaosq = sum([self.peaoTabuleiro[i]
                     for i in tabuleiro.pieces(chess.PAWN, chess.WHITE)])
        peaosq = peaosq + sum([-self.peaoTabuleiro[chess.square_mirror(i)]
                              for i in tabuleiro.pieces(chess.PAWN, chess.BLACK)])
        cavalosq = sum([self.cavaloTabuleiro[i]
                       for i in tabuleiro.pieces(chess.KNIGHT, chess.WHITE)])
        cavalosq = cavalosq + sum([-self.cavaloTabuleiro[chess.square_mirror(i)]
                                  for i in tabuleiro.pieces(chess.KNIGHT, chess.BLACK)])
        bisposq = sum([self.bispoTabuleiro[i]
                       for i in tabuleiro.pieces(chess.BISHOP, chess.WHITE)])
        bisposq = bisposq + sum([-self.bispoTabuleiro[chess.square_mirror(i)]
                                 for i in tabuleiro.pieces(chess.BISHOP, chess.BLACK)])
        torresq = sum([self.torreTabuleiro[i]
                       for i in tabuleiro.pieces(chess.ROOK, chess.WHITE)])
        torresq = torresq + sum([-self.torreTabuleiro[chess.square_mirror(i)]
                                 for i in tabuleiro.pieces(chess.ROOK, chess.BLACK)])
        rainhasq = sum([self.rainhaTabuleiro[i]
                        for i in tabuleiro.pieces(chess.QUEEN, chess.WHITE)])
        rainhasq = rainhasq + sum([-self.rainhaTabuleiro[chess.square_mirror(i)]
                                   for i in tabuleiro.pieces(chess.QUEEN, chess.BLACK)])
        reisq = sum([self.reiTabuleiro[i]
                     for i in tabuleiro.pieces(chess.KING, chess.WHITE)])
        reisq = reisq + sum([-self.reiTabuleiro[chess.square_mirror(i)]
                             for i in tabuleiro.pieces(chess.KING, chess.BLACK)])

        eval = material + peaosq + cavalosq + bisposq + torresq + rainhasq + reisq
        if tabuleiro.turn:
            return eval
        else:
            return -eval

    def getMovimentoTabuleiro(self, tabuleiro):
        return str(tabuleiro.fen())

    def quiesce(self, alpha, beta, tabuleiro):
        aux = self.avaliarTabuleiro(tabuleiro)
        if (aux >= beta):
            return beta
        if (aux > alpha):
            alpha = aux

        chave_posicao = self.getMovimentoTabuleiro(tabuleiro)
        if chave_posicao in self.tabela_transposicao:
            return self.tabela_transposicao[chave_posicao]
        for movimento in self.getMovimentos(tabuleiro):
            if tabuleiro.is_capture(movimento):
                tabuleiro.push(movimento)
                avalicao = -self.quiesce(-beta, -alpha, tabuleiro)
                tabuleiro.pop()
                if (avalicao >= beta):
                    return beta
                alpha = max(avalicao, alpha)
        self.tabela_transposicao[chave_posicao] = alpha
        return alpha

    def alphabeta(self, alpha, beta, profundidade, tabuleiro):
        if profundidade == 0:
            return self.quiesce(alpha, beta, tabuleiro)

        melhor_avaliacao = float('-inf')
        for movimento in self.getMovimentos(tabuleiro):
            tabuleiro.push(movimento)
            avalicao = -self.alphabeta(-beta, -alpha,
                                       profundidade - 1, tabuleiro)
            tabuleiro.pop()
            if (avalicao >= beta):
                return avalicao
            if (avalicao > alpha):
                alpha = avalicao
            alpha = max(avalicao, alpha)
        return melhor_avaliacao

    def escolherMelhorMovimento(self, profundidade, tabuleiro):
        melhorAvaliacao = float('-inf')
        melhorMovimento = None
        alpha = float('-inf')
        beta = float('inf')

        for movimento in self.getMovimentos(tabuleiro):
            tabuleiro.push(movimento)
            avaliacao = -self.alphabeta(-beta, -
                                        alpha, profundidade-1, tabuleiro)

            if avaliacao > melhorAvaliacao:
                melhorAvaliacao = avaliacao
                melhorMovimento = movimento

            if melhorAvaliacao > alpha:
                alpha = melhorAvaliacao
            tabuleiro.pop()

        return melhorMovimento

    def fazerMovimento(self, profundidade, tabuleiro):
        return self.escolherMelhorMovimento(profundidade, tabuleiro)
