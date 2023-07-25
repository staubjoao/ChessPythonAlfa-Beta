import chess
import numpy as np
import time


class ChessIA:
    def __init__(self):
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
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50]

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

    def getMovimentosCorAtual(self, tabuleiro):
        movimentos_cor = []

        for move in tabuleiro.legal_moves:
            if tabuleiro.piece_at(move.from_square).color == tabuleiro.turn:
                movimentos_cor.append(move)
        return movimentos_cor

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

        pawnsq = sum([self.peaoTabuleiro[i]
                     for i in tabuleiro.pieces(chess.PAWN, chess.WHITE)])
        pawnsq = pawnsq + sum([-self.peaoTabuleiro[chess.square_mirror(i)]
                              for i in tabuleiro.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([self.cavaloTabuleiro[i]
                       for i in tabuleiro.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-self.cavaloTabuleiro[chess.square_mirror(i)]
                                  for i in tabuleiro.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq = sum([self.bispoTabuleiro[i]
                       for i in tabuleiro.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq = bishopsq + sum([-self.bispoTabuleiro[chess.square_mirror(i)]
                                   for i in tabuleiro.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([self.torreTabuleiro[i]
                     for i in tabuleiro.pieces(chess.ROOK, chess.WHITE)])
        rooksq = rooksq + sum([-self.torreTabuleiro[chess.square_mirror(i)]
                               for i in tabuleiro.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([self.rainhaTabuleiro[i]
                      for i in tabuleiro.pieces(chess.QUEEN, chess.WHITE)])
        queensq = queensq + sum([-self.rainhaTabuleiro[chess.square_mirror(i)]
                                 for i in tabuleiro.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([self.reiTabuleiro[i]
                     for i in tabuleiro.pieces(chess.KING, chess.WHITE)])
        kingsq = kingsq + sum([-self.reiTabuleiro[chess.square_mirror(i)]
                               for i in tabuleiro.pieces(chess.KING, chess.BLACK)])

        eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
        if tabuleiro.turn:
            return eval
        else:
            return -eval

    def quiesce(self, alpha, beta, tabuleiro):
        stand_pat = self.avaliarTabuleiro(tabuleiro)
        if (stand_pat >= beta):
            return beta
        if (stand_pat > alpha):
            alpha = stand_pat

        for move in tabuleiro.legal_moves:
            if tabuleiro.is_capture(move):
                tabuleiro.push(move)
                score = -self.quiesce(-beta, -alpha, tabuleiro)
                tabuleiro.pop()
                if (score >= beta):
                    return beta
                if (score > alpha):
                    alpha = score
        return alpha

    def alphabeta(self, alpha, beta, profundidadeleft, tabuleiro):
        bestscore = float('-inf')
        if (profundidadeleft == 0):
            resultado = self.quiesce(alpha, beta, tabuleiro)

            return resultado
        for move in tabuleiro.legal_moves:
            tabuleiro.push(move)
            score = -self.alphabeta(-beta, -alpha,
                                    profundidadeleft - 1, tabuleiro)
            tabuleiro.pop()
            if (score >= beta):
                return score
            if (score > bestscore):
                bestscore = score
            if (score > alpha):
                alpha = score
        return bestscore

    def escolherMelhorMovimento(self, profundidade, tabuleiro):
        melhorAvaliacao = float('-inf')
        melhorMovimento = None
        alpha = float('-inf')
        beta = float('inf')

        for movimento in self.getMovimentosCorAtual(tabuleiro):
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
