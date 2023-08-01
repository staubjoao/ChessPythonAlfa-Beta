import chess
import numpy as np
import time


class ChessPieces:
    P = 1
    N = 2
    B = 3
    R = 4
    Q = 5
    K = 6
    p = 7
    n = 8
    b = 9
    r = 10
    q = 11
    k = 12


class ChessIA:
    def __init__(self):
        self.tabela_transposicao = {}

        self.mg_pawn_table = [
            0,   0,   0,   0,   0,   0,  0,   0,
            98, 134,  61,  95,  68, 126, 34, -11,
            -6,   7,  26,  31,  65,  56, 25, -20,
            -14,  13,   6,  21,  23,  12, 17, -23,
            -27,  -2,  -5,  12,  17,   6, 10, -25,
            -26,  -4,  -4, -10,   3,   3, 33, -12,
            -35,  -1, -20, -23, -15,  24, 38, -22,
            0,   0,   0,   0,   0,   0,  0,   0]

        self.eg_pawn_table = [
            0,   0,   0,   0,   0,   0,   0,   0,
            178, 173, 158, 134, 147, 132, 165, 187,
            94, 100,  85,  67,  56,  53,  82,  84,
            32,  24,  13,   5,  -2,   4,  17,  17,
            13,   9,  -3,  -7,  -7,  -8,   3,  -1,
            4,   7,  -6,   1,   0,  -5,  -1,  -8,
            13,   8,   8,  10,  13,   0,   2,  -7,
            0,   0,   0,   0,   0,   0,   0,   0]

        self.mg_knight_table = [
            -167, -89, -34, -49,  61, -97, -15, -107,
            -73, -41,  72,  36,  23,  62,   7,  -17,
            -47,  60,  37,  65,  84, 129,  73,   44,
            -9,  17,  19,  53,  37,  69,  18,   22,
            -13,   4,  16,  13,  28,  19,  21,   -8,
            -23,  -9,  12,  10,  19,  17,  25,  -16,
            -29, -53, -12,  -3,  -1,  18, -14,  -19,
            -105, -21, -58, -33, -17, -28, -19,  -23]

        self.eg_knight_table = [
            -58, -38, -13, -28, -31, -27, -63, -99,
            -25,  -8, -25,  -2,  -9, -25, -24, -52,
            -24, -20,  10,   9,  -1,  -9, -19, -41,
            -17,   3,  22,  22,  22,  11,   8, -18,
            -18,  -6,  16,  25,  16,  17,   4, -18,
            -23,  -3,  -1,  15,  10,  -3, -20, -22,
            -42, -20, -10,  -5,  -2, -20, -23, -44,
            -29, -51, -23, -15, -22, -18, -50, -64]

        self.mg_bishop_table = [
            -29,   4, -82, -37, -25, -42,   7,  -8,
            -26,  16, -18, -13,  30,  59,  18, -47,
            -16,  37,  43,  40,  35,  50,  37,  -2,
            -4,   5,  19,  50,  37,  37,   7,  -2,
            -6,  13,  13,  26,  34,  12,  10,   4,
            0,  15,  15,  15,  14,  27,  18,  10,
            4,  15,  16,   0,   7,  21,  33,   1,
            -33,  -3, -14, -21, -13, -12, -39, -21]

        self.eg_bishop_table = [
            -14, -21, -11,  -8, -7,  -9, -17, -24,
            -8,  -4,   7, -12, -3, -13,  -4, -14,
            2,  -8,   0,  -1, -2,   6,   0,   4,
            -3,   9,  12,   9, 14,  10,   3,   2,
            -6,   3,  13,  19,  7,  10,  -3,  -9,
            -12,  -3,   8,  10, 13,   3,  -7, -15,
            -14, -18,  -7,  -1,  4,  -9, -15, -27,
            -23,  -9, -23,  -5, -9, -16,  -5, -17]

        self.mg_rook_table = [
            32,  42,  32,  51, 63,  9,  31,  43,
            27,  32,  58,  62, 80, 67,  26,  44,
            -5,  19,  26,  36, 17, 45,  61,  16,
            -24, -11,   7,  26, 24, 35,  -8, -20,
            -36, -26, -12,  -1,  9, -7,   6, -23,
            -45, -25, -16, -17,  3,  0,  -5, -33,
            -44, -16, -20,  -9, -1, 11,  -6, -71,
            -19, -13,   1,  17, 16,  7, -37, -26]

        self.eg_rook_table = [
            13, 10, 18, 15, 12,  12,   8,   5,
            11, 13, 13, 11, -3,   3,   8,   3,
            7,  7,  7,  5,  4,  -3,  -5,  -3,
            4,  3, 13,  1,  2,   1,  -1,   2,
            3,  5,  8,  4, -5,  -6,  -8, -11,
            -4,  0, -5, -1, -7, -12,  -8, -16,
            -6, -6,  0,  2, -9,  -9, -11,  -3,
            -9,  2,  3, -1, -5, -13,   4, -20]

        self.mg_queen_table = [
            -28,   0,  29,  12,  59,  44,  43,  45,
            -24, -39,  -5,   1, -16,  57,  28,  54,
            -13, -17,   7,   8,  29,  56,  47,  57,
            -27, -27, -16, -16,  -1,  17,  -2,   1,
            -9, -26,  -9, -10,  -2,  -4,   3,  -3,
            -14,   2, -11,  -2,  -5,   2,  14,   5,
            -35,  -8,  11,   2,   8,  15,  -3,   1,
            -1, -18,  -9,  10, -15, -25, -31, -50]

        self.eg_queen_table = [
            -9,  22,  22,  27,  27,  19,  10,  20,
            -17,  20,  32,  41,  58,  25,  30,   0,
            -20,   6,   9,  49,  47,  35,  19,   9,
            3,  22,  24,  45,  57,  40,  57,  36,
            -18,  28,  19,  47,  31,  34,  39,  23,
            -16, -27,  15,   6,   9,  17,  10,   5,
            -22, -23, -30, -16, -16, -23, -36, -32,
            -33, -28, -22, -43,  -5, -32, -20, -41]

        self.mg_king_table = [
            -65,  23,  16, -15, -56, -34,   2,  13,
            29,  -1, -20,  -7,  -8,  -4, -38, -29,
            -9,  24,   2, -16, -20,   6,  22, -22,
            -17, -20, -12, -27, -30, -25, -14, -36,
            -49,  -1, -27, -39, -46, -44, -33, -51,
            -14, -14, -22, -46, -44, -30, -15, -27,
            1,   7,  -8, -64, -43, -16,   9,   8,
            -15,  36,  12, -54,   8, -28,  24,  14]

        self.eg_king_table = [
            -74, -35, -18, -18, -11,  15,   4, -17,
            -12,  17,  14,  17,  17,  38,  23,  11,
            10,  17,  23,  15,  20,  45,  44,  13,
            -8,  22,  24,  27,  26,  33,  26,   3,
            -18,  -4,  21,  24,  27,  23,   9, -11,
            -19,  -3,  11,  21,  23,  16,   7,  -9,
            -27, -11,   4,  13,  14,   4,  -5, -17,
            -53, -34, -21, -11, -28, -14, -24, -43]

        self.mg_pesto_table = [
            self.mg_pawn_table,
            self.mg_knight_table,
            self.mg_bishop_table,
            self.mg_rook_table,
            self.mg_queen_table,
            self.mg_king_table]

        self.eg_pesto_table = [
            self.eg_pawn_table,
            self.eg_knight_table,
            self.eg_bishop_table,
            self.eg_rook_table,
            self.eg_queen_table,
            self.eg_king_table]

        self.gamephaseInc = [0, 0, 1, 1, 1, 1, 2, 2, 4, 4, 0, 0]
        self.mg_table = [[0 for _ in range(64)] for _ in range(12)]
        self.eg_table = [[0 for _ in range(64)] for _ in range(12)]

        self.mg_value = [82, 337, 365, 477, 1025,  0]
        self.eg_value = [94, 281, 297, 512,  936,  0]

    def flip_square(self, sq):
        return sq ^ 56

    def init_tables(self):
        pc = 0
        for p in range(6):
            for sq in range(64):
                self.mg_table[pc][sq] = self.mg_value[p] + \
                    self.mg_pesto_table[p][sq]
                self.eg_table[pc][sq] = self.eg_value[p] + \
                    self.eg_pesto_table[p][sq]
                self.mg_table[pc + 1][sq] = self.mg_value[p] + \
                    self.mg_pesto_table[p][self.flip_square(sq)]
                self.eg_table[pc + 1][sq] = self.eg_value[p] + \
                    self.eg_pesto_table[p][self.flip_square(sq)]
            pc += 2

    def other_side(self, side):
        return side ^ 1

    def pc_color(self, pc):
        return chess.WHITE if pc.color == chess.WHITE else chess.BLACK

    def evaluate(self, tabuleiro):
        if tabuleiro.is_checkmate():
            if tabuleiro.turn:
                return float('-inf')
            else:
                return float('inf')
        if tabuleiro.is_insufficient_material() or tabuleiro.is_stalemate():
            return 0

        mg = [0, 0]
        eg = [0, 0]
        gamePhase = 0

        mg_table = [
            [0] * 64, [0] * 64, [0] * 64, [0] * 64,
            [0] * 64, [0] * 64, [0] * 64, [0] * 64,
            [0] * 64, [0] * 64, [0] * 64, [0] * 64,
        ]

        eg_table = [
            [0] * 64, [0] * 64, [0] * 64, [0] * 64,
            [0] * 64, [0] * 64, [0] * 64, [0] * 64,
            [0] * 64, [0] * 64, [0] * 64, [0] * 64,
        ]

        for p in range(6):
            for sq in range(64):
                mg_table[p][sq] = self.mg_value[p] + self.mg_pesto_table[p][sq]
                eg_table[p][sq] = self.eg_value[p] + self.eg_pesto_table[p][sq]
                mg_table[p + 1][sq] = self.mg_value[p] + \
                    self.mg_pesto_table[p][self.flip_square(sq)]
                eg_table[p + 1][sq] = self.eg_value[p] + \
                    self.eg_pesto_table[p][self.flip_square(sq)]

        for sq in range(64):
            pc = tabuleiro.piece_at(sq)
            if pc is not None:
                mg[self.pc_color(pc)] += self.mg_table[pc.piece_type][sq]
                eg[self.pc_color(pc)] += self.eg_table[pc.piece_type][sq]
                gamePhase += self.gamephaseInc[pc.piece_type]

        mgScore = mg[tabuleiro.turn] - mg[1 - tabuleiro.turn]
        egScore = eg[tabuleiro.turn] - eg[1 - tabuleiro.turn]
        mgPhase = gamePhase if gamePhase <= 24 else 24
        egPhase = 24 - mgPhase

        return (mgScore * mgPhase + egScore * egPhase) // 24

    def avaliarMovimento(self, tabuleiro, movimento):
        tabuleiro_copia = tabuleiro.copy()
        tabuleiro_copia.push(movimento)

        return self.evaluate(tabuleiro_copia)

    def ordenarMovimentos(self, tabuleiro):
        movimentos = self.getMovimentos(tabuleiro)
        movimentos_ordenados = sorted(
            movimentos, key=lambda move: self.avaliarMovimento(tabuleiro, move), reverse=True)
        return movimentos_ordenados

    def getMovimentos(self, tabuleiro):
        return tabuleiro.legal_moves

    def getMovimentoTabuleiro(self, tabuleiro):
        return str(tabuleiro.fen())

    def quiesce(self, alpha, beta, tabuleiro):
        aux = self.evaluate(tabuleiro)
        if aux >= beta:
            return beta
        if aux > alpha:
            alpha = aux

        chave_posicao = self.getMovimentoTabuleiro(tabuleiro)
        if chave_posicao in self.tabela_transposicao:
            return self.tabela_transposicao[chave_posicao]
        for movimento in self.getMovimentos(tabuleiro):
            if tabuleiro.is_capture(movimento):
                tabuleiro.push(movimento)
                avalicao = -self.quiesce(-beta, -alpha, tabuleiro)
                tabuleiro.pop()
                if avalicao >= beta:
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
            if avalicao >= beta:
                return avalicao
            if avalicao > melhor_avaliacao:
                melhor_avaliacao = avalicao
            if avalicao > alpha:
                alpha = avalicao
            alpha = max(avalicao, alpha)
        return melhor_avaliacao

    def escolherMelhorMovimento(self, profundidade, tabuleiro):
        melhorAvaliacao = float('-inf')
        melhorMovimento = None
        alpha = float('-inf')
        beta = float('inf')

        inicio = time.time()
        movimentos_ordenados = self.ordenarMovimentos(tabuleiro)
        fim = time.time()
        tempo_total = fim - inicio
        print("Tempo total de execução para ordenar os movimentos:",
              tempo_total, "segundos")
        for movimento in movimentos_ordenados:
            tabuleiro.push(movimento)
            inicio = time.time()
            avaliacao = -self.alphabeta(-beta, -
                                        alpha, profundidade-1, tabuleiro)
            fim = time.time()
            tempo_total = fim - inicio
            print("Tempo total de execução para ordenar avaliar o movimento:",
                  tempo_total, "segundos")
            if avaliacao > melhorAvaliacao:
                melhorAvaliacao = avaliacao
                melhorMovimento = movimento

            if melhorAvaliacao > alpha:
                alpha = melhorAvaliacao
            tabuleiro.pop()

        return melhorMovimento

    def fazerMovimento(self, profundidade, tabuleiro):
        self.init_tables()
        print(self.evaluate(tabuleiro))
        return self.escolherMelhorMovimento(profundidade, tabuleiro)
