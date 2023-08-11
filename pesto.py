import chess


class Pesto:
    def __init__(self):
        # vetores que representam valores para cada peça no tabuleiro
        self.tabuleiro_peao = [
            0,   0,   0,   0,   0,   0,  0,   0,
            98, 134,  61,  95,  68, 126, 34, -11,
            -6,   7,  26,  31,  65,  56, 25, -20,
            -14,  13,   6,  21,  23,  12, 17, -23,
            -27,  -2,  -5,  12,  17,   6, 10, -25,
            -26,  -4,  -4, -10,   3,   3, 33, -12,
            -35,  -1, -20, -23, -15,  24, 38, -22,
            0,   0,   0,   0,   0,   0,  0,   0]

        self.tabuleiro_peao_final = [
            0,   0,   0,   0,   0,   0,   0,   0,
            178, 173, 158, 134, 147, 132, 165, 187,
            94, 100,  85,  67,  56,  53,  82,  84,
            32,  24,  13,   5,  -2,   4,  17,  17,
            13,   9,  -3,  -7,  -7,  -8,   3,  -1,
            4,   7,  -6,   1,   0,  -5,  -1,  -8,
            13,   8,   8,  10,  13,   0,   2,  -7,
            0,   0,   0,   0,   0,   0,   0,   0]

        self.tabuleiro_cavalo = [
            -167, -89, -34, -49,  61, -97, -15, -107,
            -73, -41,  72,  36,  23,  62,   7,  -17,
            -47,  60,  37,  65,  84, 129,  73,   44,
            -9,  17,  19,  53,  37,  69,  18,   22,
            -13,   4,  16,  13,  28,  19,  21,   -8,
            -23,  -9,  12,  10,  19,  17,  25,  -16,
            -29, -53, -12,  -3,  -1,  18, -14,  -19,
            -105, -21, -58, -33, -17, -28, -19,  -23]

        self.tabuleiro_cavalo_final = [
            -58, -38, -13, -28, -31, -27, -63, -99,
            -25,  -8, -25,  -2,  -9, -25, -24, -52,
            -24, -20,  10,   9,  -1,  -9, -19, -41,
            -17,   3,  22,  22,  22,  11,   8, -18,
            -18,  -6,  16,  25,  16,  17,   4, -18,
            -23,  -3,  -1,  15,  10,  -3, -20, -22,
            -42, -20, -10,  -5,  -2, -20, -23, -44,
            -29, -51, -23, -15, -22, -18, -50, -64]

        self.tabuleiro_bispo = [
            -29,   4, -82, -37, -25, -42,   7,  -8,
            -26,  16, -18, -13,  30,  59,  18, -47,
            -16,  37,  43,  40,  35,  50,  37,  -2,
            -4,   5,  19,  50,  37,  37,   7,  -2,
            -6,  13,  13,  26,  34,  12,  10,   4,
            0,  15,  15,  15,  14,  27,  18,  10,
            4,  15,  16,   0,   7,  21,  33,   1,
            -33,  -3, -14, -21, -13, -12, -39, -21]

        self.tabuleiro_bispo_final = [
            -14, -21, -11,  -8, -7,  -9, -17, -24,
            -8,  -4,   7, -12, -3, -13,  -4, -14,
            2,  -8,   0,  -1, -2,   6,   0,   4,
            -3,   9,  12,   9, 14,  10,   3,   2,
            -6,   3,  13,  19,  7,  10,  -3,  -9,
            -12,  -3,   8,  10, 13,   3,  -7, -15,
            -14, -18,  -7,  -1,  4,  -9, -15, -27,
            -23,  -9, -23,  -5, -9, -16,  -5, -17]

        self.tabuleiro_torre = [
            32,  42,  32,  51, 63,  9,  31,  43,
            27,  32,  58,  62, 80, 67,  26,  44,
            -5,  19,  26,  36, 17, 45,  61,  16,
            -24, -11,   7,  26, 24, 35,  -8, -20,
            -36, -26, -12,  -1,  9, -7,   6, -23,
            -45, -25, -16, -17,  3,  0,  -5, -33,
            -44, -16, -20,  -9, -1, 11,  -6, -71,
            -19, -13,   1,  17, 16,  7, -37, -26]

        self.tabuleiro_torre_final = [
            13, 10, 18, 15, 12,  12,   8,   5,
            11, 13, 13, 11, -3,   3,   8,   3,
            7,  7,  7,  5,  4,  -3,  -5,  -3,
            4,  3, 13,  1,  2,   1,  -1,   2,
            3,  5,  8,  4, -5,  -6,  -8, -11,
            -4,  0, -5, -1, -7, -12,  -8, -16,
            -6, -6,  0,  2, -9,  -9, -11,  -3,
            -9,  2,  3, -1, -5, -13,   4, -20]

        self.tabuleiro_rainha = [
            -28,   0,  29,  12,  59,  44,  43,  45,
            -24, -39,  -5,   1, -16,  57,  28,  54,
            -13, -17,   7,   8,  29,  56,  47,  57,
            -27, -27, -16, -16,  -1,  17,  -2,   1,
            -9, -26,  -9, -10,  -2,  -4,   3,  -3,
            -14,   2, -11,  -2,  -5,   2,  14,   5,
            -35,  -8,  11,   2,   8,  15,  -3,   1,
            -1, -18,  -9,  10, -15, -25, -31, -50]

        self.tabuleiro_rainha_final = [
            -9,  22,  22,  27,  27,  19,  10,  20,
            -17,  20,  32,  41,  58,  25,  30,   0,
            -20,   6,   9,  49,  47,  35,  19,   9,
            3,  22,  24,  45,  57,  40,  57,  36,
            -18,  28,  19,  47,  31,  34,  39,  23,
            -16, -27,  15,   6,   9,  17,  10,   5,
            -22, -23, -30, -16, -16, -23, -36, -32,
            -33, -28, -22, -43,  -5, -32, -20, -41]

        self.tabuleiro_rei = [
            -65,  23,  16, -15, -56, -34,   2,  13,
            29,  -1, -20,  -7,  -8,  -4, -38, -29,
            -9,  24,   2, -16, -20,   6,  22, -22,
            -17, -20, -12, -27, -30, -25, -14, -36,
            -49,  -1, -27, -39, -46, -44, -33, -51,
            -14, -14, -22, -46, -44, -30, -15, -27,
            1,   7,  -8, -64, -43, -16,   9,   8,
            -15,  36,  12, -54,   8, -28,  24,  14]

        self.tabuleiro_rei_final = [
            -74, -35, -18, -18, -11,  15,   4, -17,
            -12,  17,  14,  17,  17,  38,  23,  11,
            10,  17,  23,  15,  20,  45,  44,  13,
            -8,  22,  24,  27,  26,  33,  26,   3,
            -18,  -4,  21,  24,  27,  23,   9, -11,
            -19,  -3,  11,  21,  23,  16,   7,  -9,
            -27, -11,   4,  13,  14,   4,  -5, -17,
            -53, -34, -21, -11, -28, -14, -24, -43]

        self.valor_pecas = {
            chess.PAWN: 82,
            chess.KNIGHT: 337,
            chess.BISHOP: 365,
            chess.ROOK: 477,
            chess.QUEEN: 1025,
            chess.KING: 24000
        }

        self.valor_pecas_final = {
            chess.PAWN: 94,
            chess.KNIGHT: 281,
            chess.BISHOP: 297,
            chess.ROOK: 512,
            chess.QUEEN: 936,
            chess.KING: 24000
        }

        self.pesto_valores = {
            chess.PAWN: self.tabuleiro_peao,
            chess.KNIGHT: self.tabuleiro_cavalo,
            chess.BISHOP: self.tabuleiro_bispo,
            chess.ROOK: self.tabuleiro_torre,
            chess.QUEEN: self.tabuleiro_rainha,
            chess.KING: self.tabuleiro_rei}

        self.pesto_valores_final = {
            chess.PAWN: self.tabuleiro_peao_final,
            chess.KNIGHT: self.tabuleiro_cavalo_final,
            chess.BISHOP: self.tabuleiro_bispo_final,
            chess.ROOK: self.tabuleiro_torre_final,
            chess.QUEEN: self.tabuleiro_rainha_final,
            chess.KING: self.tabuleiro_rei_final}

        self.peao_estagio = 0
        self.cavalo_estagio = 1
        self.bispo_estagio = 1
        self.torre_estagio = 2
        self.rainha_estagio = 4
        self.total_estagio = self.peao_estagio*16 + self.cavalo_estagio*4 + \
            self.bispo_estagio*4 + self.torre_estagio*4 + self.rainha_estagio*2

    def count_pieces(self, tabuleiro):
        """
        Counts the number of each piece on the board.

        :param 
            board: The board to count the pieces on.
        :return: 
            A list of tuples containing the number of pieces of that type
            and their phase value.
        """

        wp = len(tabuleiro.pieces(chess.PAWN, chess.WHITE))
        wn = len(tabuleiro.pieces(chess.KNIGHT, chess.WHITE))
        wb = len(tabuleiro.pieces(chess.BISHOP, chess.WHITE))
        wr = len(tabuleiro.pieces(chess.ROOK, chess.WHITE))
        wq = len(tabuleiro.pieces(chess.QUEEN, chess.WHITE))
        bp = len(tabuleiro.pieces(chess.PAWN, chess.BLACK))
        bn = len(tabuleiro.pieces(chess.KNIGHT, chess.BLACK))
        bb = len(tabuleiro.pieces(chess.BISHOP, chess.BLACK))
        br = len(tabuleiro.pieces(chess.ROOK, chess.BLACK))
        bq = len(tabuleiro.pieces(chess.QUEEN, chess.BLACK))

        return [
            (wp, self.peao_estagio),
            (bp, self.peao_estagio),
            (wn, self.cavalo_estagio),
            (bn, self.cavalo_estagio),
            (wb, self.bispo_estagio),
            (bb, self.bispo_estagio),
            (wr, self.torre_estagio),
            (br, self.torre_estagio),
            (wq, self.rainha_estagio),
            (bq, self.rainha_estagio)]

    def get_phase(self, tabuleiro):
        """
        Calculates the phase of the game based on the number of pieces on the board.

        :param
            pieces: A list of tuples containing the number of pieces of that type
            and their phase value.
        :return:
            The phase of the game.
        """
        pieces = self.count_pieces(tabuleiro)
        phase = self.total_estagio

        for piece_count, piece_phase in pieces:
            phase -= piece_count * piece_phase

        phase = (phase * 256 + (self.total_estagio / 2)) / self.total_estagio
        return phase

    def board_evaluation(self, tabuleiro):
        """
        This functions receives a board and assigns a value to it, it acts as
        an evaluation function of the current state for this game. It returns


        Arguments:
            - board: current board state.

        Returns:
            - total_value(int): integer representing
            current value for this board.
        """
        phase = self.get_phase(tabuleiro)

        mg = {
            chess.WHITE: 0,
            chess.BLACK: 0,
        }
        eg = {
            chess.WHITE: 0,
            chess.BLACK: 0,
        }

        # loop through all squares and sum their piece values for both sides
        for quadrado in range(64):
            piece = tabuleiro.piece_at(quadrado)
            if piece is not None:
                if piece.color == chess.WHITE:
                    mg[piece.color] += self.pesto_valores[piece.piece_type][63 -
                                                                            quadrado] + self.valor_pecas[piece.piece_type]
                    eg[piece.color] += self.pesto_valores_final[piece.piece_type][63 -
                                                                                  quadrado] + self.valor_pecas_final[piece.piece_type]
                else:
                    mg[piece.color] += self.pesto_valores[piece.piece_type][quadrado] + \
                        self.valor_pecas[piece.piece_type]
                    eg[piece.color] += self.pesto_valores_final[piece.piece_type][quadrado] + \
                        self.valor_pecas_final[piece.piece_type]

        # calculate board score based on phase
        mg_score = mg[tabuleiro.turn] - mg[not tabuleiro.turn]
        eg_score = eg[tabuleiro.turn] - eg[not tabuleiro.turn]
        eval = ((mg_score * (256 - phase)) + (eg_score * phase)) / 256

        return eval

    def evaluate_piece(self, tabuleiro, quadrado, fase):
        """
        Evaluates a piece on a given quadrado.

        Arguments:
            - board: current board state.
            - quadrado: quadrado to evaluate.
            - phase: current phase of the game.

        Returns:
            - value(float): float representing
            current value for this piece on this quadrado.
        """
        mg_score = 0
        eg_score = 0

        # get mid and end game score for single piece
        piece = tabuleiro.piece_at(quadrado)
        if piece is not None:
            if piece.color == chess.WHITE:
                mg_score += self.pesto_valores[piece.piece_type][63 -
                                                                 quadrado] + self.valor_pecas[piece.piece_type]
                eg_score += self.pesto_valores_final[piece.piece_type][63 -
                                                                       quadrado] + self.valor_pecas_final[piece.piece_type]
            else:
                mg_score += self.pesto_valores[piece.piece_type][quadrado] + \
                    self.valor_pecas[piece.piece_type]
                eg_score += self.pesto_valores_final[piece.piece_type][quadrado] + \
                    self.valor_pecas_final[piece.piece_type]

        # evaluate piece value based on phase
        eval = ((mg_score * (256 - fase)) + (eg_score * fase)) / 256
        return eval

    def evaluate_capture(self, tabuleiro, movimento, phase):
        """
        Evaluates a capture move based phase of the game.

        Arguments:
            - board: current board state.
            - move: move to evaluate.
            - phase: current phase of the game.

        Returns:
            - value(float): float representing
            value for this capture.
        """
        mg_score = 0
        eg_score = 0

        # en passant score
        if tabuleiro.is_en_passant(movimento):
            return 0

        capturing_piece = tabuleiro.piece_at(movimento.from_square).piece_type
        captured_piece = tabuleiro.piece_at(movimento.to_square).piece_type

        # get mid and end game difference of scores between captured
        # and capturing piece
        if capturing_piece is not None and captured_piece is not None:
            mg_score += self.valor_pecas[captured_piece] - \
                self.valor_pecas[capturing_piece]
            eg_score += self.valor_pecas_final[captured_piece] - \
                self.valor_pecas_final[capturing_piece]

        # evaluate capture based on game's phase
        eval = ((mg_score * (256 - phase)) + (eg_score * phase)) / 256
        return eval
