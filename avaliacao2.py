import random
import chess

from pesto import Pesto


class Avaliacao2:
    def __init__(self):
        self.funcs_pesto = Pesto()

    def organize_moves(self, tabuleiro):
        non_captures = []
        captures = []

        for move in tabuleiro.legal_moves:
            if tabuleiro.is_capture(move):
                captures.append(move)
            else:
                non_captures.append(move)

        random.shuffle(captures)
        random.shuffle(non_captures)
        return captures + non_captures

    def organize_moves_quiescence(self, tabuleiro):
        phase = self.funcs_pesto.get_phase(tabuleiro)
        # filter only important moves for quiescence search
        captures = filter(lambda move: tabuleiro.is_zeroing(
            move) or tabuleiro.gives_check(move), tabuleiro.legal_moves)
        # sort moves by importance
        moves = sorted(captures, key=lambda move: self.mvv_lva(
            tabuleiro, move, phase), reverse=(True if tabuleiro.turn == chess.BLACK else False))
        return moves

    def mvv_lva(self, tabuleiro, move, phase):
        move_value = 0

        # evaluating position
        from_value = self.funcs_pesto.evaluate_piece(
            tabuleiro, move.from_square, phase)
        to_value = self.funcs_pesto.evaluate_piece(
            tabuleiro, move.to_square, phase)

        move_value += to_value - from_value

        # evaluating capture
        if tabuleiro.is_capture(move):
            move_value += self.funcs_pesto.evaluate_capture(
                tabuleiro, move, phase)

        return -move_value if tabuleiro.turn else move_value
