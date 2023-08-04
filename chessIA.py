import chess
import numpy as np
import time


class ChessIA:
    def __init__(self):
        self.peaoTabuleiro = [
            0, 0, 0, 0, 0, 0, 0, 0,
            20, 26, 26, 28, 28, 26, 26, 20,
            12, 14, 16, 21, 21, 16, 14, 12,
            8, 10, 12, 18, 18, 12, 10, 8,
            4, 6, 8, 16, 16, 8, 6, 4,
            2, 2, 4, 6, 6, 4, 2, 2,
            0, 0, 0, -4, -4, 0, 0, 0,
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
            -40, -20, -15, -15, -15, -15, -20, -40,
            0, 5, 5, 5, 5, 5, 5, 0,
            0, 10, 10, 18, 18, 10, 10, 0,
            0, 10, 10, 18, 18, 10, 10, 0,
            0, 5, 10, 18, 18, 10, 5, 0,
            0, 0, 5, 5, 5, 5, 0, 0,
            0, 5, 0, 0, 0, 0, 5, 0,
            -50, -20, -10, -20, -20, -10, -20, -50]

        self.torreTabuleiro = [
            10, 10, 10, 10, 10, 10, 10, 10,
            5, 5, 5, 10, 10, 5, 5, 5,
            0, 0, 5, 10, 10, 5, 0, 0,
            0, 0, 5, 10, 10, 5, 0, 0,
            0, 0, 5, 10, 10, 5, 0, 0,
            0, 0, 5, 10, 10, 5, 0, 0,
            0, 0, 5, 10, 10, 5, 0, 0,
            0, 0, 5, 10, 10, 5, 0, 0]

        self.rainhaTabuleiro = [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 10, 10, 10, 10, 0, 0,
            0, 0, 10, 15, 15, 10, 0, 0,
            0, 0, 10, 15, 15, 10, 0, 0,
            0, 0, 10, 10, 10, 10, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0]

        self.reiTabuleiro = [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            12, 8, 4, 0, 0, 4, 8, 12,
            16, 12, 8, 4, 4, 8, 12, 16,
            24, 20, 16, 12, 12, 16, 20, 24,
            24, 24, 24, 16, 16, 6, 32, 32]

        self.peao_valor = 100
        self.cavalo_valor = 320
        self.bispo_valor = 330
        self.torre_valor = 500
        self.rainha_valor = 900

    def avaliarTabuleiro(self):
        if self.tabuleiro.is_checkmate():
            if self.tabuleiro.turn:
                return float('-inf')
            else:
                return float('inf')
        if self.tabuleiro.is_insufficient_material() or self.tabuleiro.is_stalemate():
            return 0

        qtd_peao_branco = len(self.tabuleiro.pieces(chess.PAWN, chess.WHITE))
        qtd_cavalo_branco = len(
            self.tabuleiro.pieces(chess.KNIGHT, chess.WHITE))
        qtd_bispo_branco = len(
            self.tabuleiro.pieces(chess.BISHOP, chess.WHITE))
        qtd_torre_branco = len(self.tabuleiro.pieces(chess.ROOK, chess.WHITE))
        qtd_rainha_branco = len(
            self.tabuleiro.pieces(chess.QUEEN, chess.WHITE))
        qtd_peao_preto = len(self.tabuleiro.pieces(chess.PAWN, chess.BLACK))
        qtd_cavalo_preto = len(
            self.tabuleiro.pieces(chess.KNIGHT, chess.BLACK))
        qtd_bispo_preto = len(self.tabuleiro.pieces(chess.BISHOP, chess.BLACK))
        qtd_torre_preto = len(self.tabuleiro.pieces(chess.ROOK, chess.BLACK))
        qtd_rainha_preto = len(self.tabuleiro.pieces(chess.QUEEN, chess.BLACK))

        material = (
            self.peao_valor * (qtd_peao_branco - qtd_peao_preto)
            + self.cavalo_valor * (qtd_cavalo_branco - qtd_cavalo_preto)
            + self.bispo_valor * (qtd_bispo_branco - qtd_bispo_preto)
            + self.torre_valor * (qtd_torre_branco - qtd_torre_preto)
            + self.rainha_valor * (qtd_rainha_branco - qtd_rainha_preto)
        )

        peaosq = sum([self.peaoTabuleiro[i]
                     for i in self.tabuleiro.pieces(chess.PAWN, chess.WHITE)])
        peaosq = peaosq + sum([-self.peaoTabuleiro[chess.square_mirror(i)]
                              for i in self.tabuleiro.pieces(chess.PAWN, chess.BLACK)])
        cavalosq = sum([self.cavaloTabuleiro[i]
                       for i in self.tabuleiro.pieces(chess.KNIGHT, chess.WHITE)])
        cavalosq = cavalosq + sum([-self.cavaloTabuleiro[chess.square_mirror(i)]
                                  for i in self.tabuleiro.pieces(chess.KNIGHT, chess.BLACK)])
        bisposq = sum([self.bispoTabuleiro[i]
                       for i in self.tabuleiro.pieces(chess.BISHOP, chess.WHITE)])
        bisposq = bisposq + sum([-self.bispoTabuleiro[chess.square_mirror(i)]
                                 for i in self.tabuleiro.pieces(chess.BISHOP, chess.BLACK)])
        torresq = sum([self.torreTabuleiro[i]
                       for i in self.tabuleiro.pieces(chess.ROOK, chess.WHITE)])
        torresq = torresq + sum([-self.torreTabuleiro[chess.square_mirror(i)]
                                 for i in self.tabuleiro.pieces(chess.ROOK, chess.BLACK)])
        rainhasq = sum([self.rainhaTabuleiro[i]
                        for i in self.tabuleiro.pieces(chess.QUEEN, chess.WHITE)])
        rainhasq = rainhasq + sum([-self.rainhaTabuleiro[chess.square_mirror(i)]
                                   for i in self.tabuleiro.pieces(chess.QUEEN, chess.BLACK)])
        reisq = sum([self.reiTabuleiro[i]
                     for i in self.tabuleiro.pieces(chess.KING, chess.WHITE)])
        reisq = reisq + sum([-self.reiTabuleiro[chess.square_mirror(i)]
                             for i in self.tabuleiro.pieces(chess.KING, chess.BLACK)])

        eval = material + peaosq + cavalosq + bisposq + torresq + rainhasq + reisq

        if self.tabuleiro.turn:
            return eval
        else:
            return -eval

    def avaliarMovimento(self, movimento):
        tabuleiro_copia = self.tabuleiro.copy()
        tabuleiro_copia.push(movimento)

        return self.avaliarTabuleiro(tabuleiro_copia)

    def ordenarMovimentos(self):
        movimentos = self.getMovimentos()
        movimentos = sorted(
            movimentos, key=lambda move: self.avaliarMovimento(self.tabuleiro, move), reverse=True)
        return movimentos

    def getMovimentos(self):
        return self.tabuleiro.legal_moves

    def getMovimentoTabuleiro(self):
        return str(self.tabuleiro.fen())

    def quiesce(self, alpha, beta):
        aux = self.avaliarTabuleiro()
        if aux >= beta:
            return beta
        if alpha < aux:
            alpha = aux

        for movimento in self.getMovimentos():
            if self.tabuleiro.is_capture(movimento):
                self.tabuleiro.push(movimento)
                avalicao = -self.quiesce(-beta, -alpha)
                self.tabuleiro.pop()
                if avalicao >= beta:
                    return beta
                if (avalicao > alpha):
                    alpha = avalicao
        return alpha

    def alphabeta(self, alpha, beta, profundidade):
        if profundidade == 0:
            return self.quiesce(alpha, beta)

        melhor_avaliacao = float('-inf')
        for movimento in self.getMovimentos():
            self.tabuleiro.push(movimento)
            avalicao = -self.alphabeta(-beta, -alpha, profundidade - 1)
            self.tabuleiro.pop()
            if avalicao >= beta:
                return avalicao
            if avalicao > melhor_avaliacao:
                melhor_avaliacao = avalicao
            if avalicao > alpha:
                alpha = avalicao
        return melhor_avaliacao

    def escolherMelhorMovimento(self, profundidade, tabuleiro):
        self.tabuleiro = tabuleiro
        melhorMovimento = chess.Move.null()
        melhorAvaliacao = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for movimento in self.getMovimentos():
            self.tabuleiro.push(movimento)
            avaliacao = -self.alphabeta(-beta, -alpha, profundidade-1)
            if avaliacao > melhorAvaliacao:
                melhorAvaliacao = avaliacao
                melhorMovimento = movimento

            if melhorAvaliacao > alpha:
                alpha = melhorAvaliacao
            self.tabuleiro.pop()
        return melhorMovimento
