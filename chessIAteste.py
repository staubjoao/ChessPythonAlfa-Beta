from typing import Dict, List, Any
import chess
import numpy as np
import time


class ChessIAteste:
    def __init__(self):
        self.tabuleiro_peao = [
            0, 0, 0, 0, 0, 0, 0, 0,
            20, 26, 26, 28, 28, 26, 26, 20,
            12, 14, 16, 21, 21, 16, 14, 12,
            8, 10, 12, 18, 18, 12, 10, 8,
            4, 6, 8, 16, 16, 8, 6, 4,
            2, 2, 4, 6, 6, 4, 2, 2,
            0, 0, 0, -4, -4, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0]

        self.tabuleiro_cavalo = [
            -40, -10, - 5, - 5, - 5, - 5, -10, -40,
            - 5, 5, 5, 5, 5, 5, 5, - 5,
            - 5, 5, 10, 15, 15, 10, 5, - 5,
            - 5, 5, 10, 15, 15, 10, 5, - 5,
            - 5, 5, 10, 15, 15, 10, 5, - 5,
            - 5, 5, 8, 8, 8, 8, 5, - 5,
            - 5, 0, 5, 5, 5, 5, 0, - 5,
            -50, -20, -10, -10, -10, -10, -20, -50]

        self.tabuleiro_bispo = [
            -40, -20, -15, -15, -15, -15, -20, -40,
            0, 5, 5, 5, 5, 5, 5, 0,
            0, 10, 10, 18, 18, 10, 10, 0,
            0, 10, 10, 18, 18, 10, 10, 0,
            0, 5, 10, 18, 18, 10, 5, 0,
            0, 0, 5, 5, 5, 5, 0, 0,
            0, 5, 0, 0, 0, 0, 5, 0,
            -50, -20, -10, -20, -20, -10, -20, -50]

        self.tabuleiro_torre = [
            10, 10, 10, 10, 10, 10, 10, 10,
            5, 5, 5, 10, 10, 5, 5, 5,
            0, 0, 5, 10, 10, 5, 0, 0,
            0, 0, 5, 10, 10, 5, 0, 0,
            0, 0, 5, 10, 10, 5, 0, 0,
            0, 0, 5, 10, 10, 5, 0, 0,
            0, 0, 5, 10, 10, 5, 0, 0,
            0, 0, 5, 10, 10, 5, 0, 0]

        self.tabuleiro_rainha = [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 10, 10, 10, 10, 0, 0,
            0, 0, 10, 15, 15, 10, 0, 0,
            0, 0, 10, 15, 15, 10, 0, 0,
            0, 0, 10, 10, 10, 10, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0]

        self.tabuleiro_rei = [
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            12, 8, 4, 0, 0, 4, 8, 12,
            16, 12, 8, 4, 4, 8, 12, 16,
            24, 20, 16, 12, 12, 16, 20, 24,
            24, 24, 24, 16, 16, 6, 32, 32]

        self.tabuleiro_rei_final = [
            -30, -5, 0, 0, 0, 0, -5, -30,
            -5, 0, 0, 0, 0, 0, 0, -5,
            0, 0, 0, 0, 0, 0, 0, 0,
            0, 0, 0, 5, 5, 0, 0, 0,
            0, 0, 0, 5, 5, 0, 0, 0,
            0, 0, 0, 0, 0, 0, 0, 0,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -40, -10, -5, -5, -5, -5, -10, -40]

        self.valor_precas = {
            chess.PAWN: 100,
            chess.ROOK: 500,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.QUEEN: 900,
            chess.KING: 20000
        }

        self.peao_valor = 100
        self.torre_valor = 500
        self.cavalo_valor = 320
        self.bispo_valor = 330
        self.rainha_valor = 900

        self.MATE_SCORE = 1000000000
        self.MATE_THRESHOLD = 999000000

        self.debug_info: Dict[str, Any] = {}

    def avaliarCaptura(self, tabuleiro, movimento):
        if tabuleiro.is_en_passant(movimento):
            return self.valor_precas[chess.PAWN]
        movimento_de = tabuleiro.piece_at(movimento.to_square)
        movimento_para = tabuleiro.piece_at(movimento.from_square)
        if movimento_de is None or movimento_para is None:
            raise Exception(
                f"Espava-se uma(s) peça(s): {movimento.to_square} e {movimento.from_square}")
        return self.valor_precas[movimento_de.piece_type] - self.valor_precas[movimento_para.piece_type]

    def avaliePeca(self, peca, square, fim_de_jogo):
        piece_type = peca.piece_type
        mapeamento = []
        if piece_type == chess.PAWN:
            if peca.color == chess.WHITE:
                mapeamento = self.tabuleiro_peao
            else:
                mapeamento = list(reversed(self.tabuleiro_peao))

        if piece_type == chess.KNIGHT:
            mapeamento = self.tabuleiro_cavalo

        if piece_type == chess.BISHOP:
            if peca.color == chess.WHITE:
                mapeamento = self.tabuleiro_bispo
            else:
                mapeamento = list(reversed(self.tabuleiro_bispo))

        if piece_type == chess.ROOK:
            if peca.color == chess.WHITE:
                mapeamento = self.tabuleiro_torre
            else:
                mapeamento = list(reversed(self.tabuleiro_torre))

        if piece_type == chess.QUEEN:
            mapeamento = self.tabuleiro_rainha

        if piece_type == chess.KING:
            if fim_de_jogo:
                if peca.color == chess.WHITE:
                    mapeamento = self.tabuleiro_rei_final
                else:
                    mapeamento = list(reversed(self.tabuleiro_rei_final))
            else:
                if peca.color == chess.WHITE:
                    mapeamento = self.tabuleiro_rei
                else:
                    mapeamento = list(reversed(self.tabuleiro_rei))

        return mapeamento[square]

    def avalieTabuleiro(self, tabuleiro):
        total = 0
        fim_de_jogo = self.verificarFimdeJogo(tabuleiro)

        for square in chess.SQUARES:
            peca = tabuleiro.piece_at(square)
            if not peca:
                continue

            valor = self.valor_precas[peca.piece_type] + \
                self.avaliePeca(peca, square, fim_de_jogo)
            if peca.color == chess.WHITE:
                total += valor
            else:
                total -= valor
        return total

    def verificarFimdeJogo(self, tabuleiro) -> bool:
        rainhas = 0
        menores = 0

        for square in chess.SQUARES:
            pecas = tabuleiro.piece_at(square)
            if pecas and pecas.piece_type == chess.QUEEN:
                rainhas += 1
            if pecas and (
                pecas.piece_type == chess.BISHOP or pecas.piece_type == chess.KNIGHT
            ):
                menores += 1

        if rainhas == 0 or (rainhas == 2 and menores <= 1):
            return True

        return False

    def selecionarMovimento(self, profundidade, tabuleiro, debug):
        self.debug_info.clear()
        self.debug_info["nodes"] = 0
        t0 = time.time()

        movimento = self.minimaxRoot(profundidade, tabuleiro)

        self.debug_info["time"] = time.time() - t0
        # if debug == True:
        #     print(f"info {self.debug_info}")
        return movimento, self.debug_info

    def valorMovimento(self, tabuleiro, movimento, fim_de_jogo):
        if movimento.promotion is not None:
            return -float("inf") if tabuleiro.turn == chess.BLACK else float("inf")

        peca = tabuleiro.piece_at(movimento.from_square)
        if peca:
            valor_de = self.avaliePeca(
                peca, movimento.from_square, fim_de_jogo)
            valor_para = self.avaliePeca(
                peca, movimento.to_square, fim_de_jogo)
            position_change = valor_de - valor_para
        else:
            raise Exception(f"Espava-se uma peça: {movimento.from_square}")

        valor_captura = 0.0
        if tabuleiro.is_capture(movimento):
            valor_captura = self.avaliarCaptura(tabuleiro, movimento)

        valor_movimento_atual = valor_captura + position_change
        if tabuleiro.turn == chess.BLACK:
            valor_movimento_atual = -valor_movimento_atual
        return valor_movimento_atual

    def ordenarMovimentos(self, tabuleiro):
        fim_de_jogo = self.verificarFimdeJogo(tabuleiro)

        def orderer(move):
            return self.valorMovimento(tabuleiro, move, fim_de_jogo)

        movimentos_ordenados = sorted(
            tabuleiro.legal_moves, key=orderer, reverse=(
                tabuleiro.turn == chess.WHITE)
        )
        return list(movimentos_ordenados)

    def minimaxRoot(self, profundidade, tabuleiro):
        maximizar = tabuleiro.turn == chess.WHITE
        melhor_movimento = -float("inf")
        if not maximizar:
            melhor_movimento = float("inf")

        moves = self.ordenarMovimentos(tabuleiro)
        melhor_movimento_found = moves[0]

        for move in moves:
            tabuleiro.push(move)
            if tabuleiro.can_claim_draw():
                value = 0.0
            else:
                value = self.minimax(profundidade - 1, tabuleiro, -float("inf"),
                                     float("inf"), not maximizar)
            tabuleiro.pop()
            if maximizar and value >= melhor_movimento:
                melhor_movimento = value
                melhor_movimento_found = move
            elif not maximizar and value <= melhor_movimento:
                melhor_movimento = value
                melhor_movimento_found = move

        return melhor_movimento_found

    def minimax(self, profundidade, tabuleiro, alpha, beta, maximizando):
        self.debug_info["nodes"] += 1

        if tabuleiro.is_checkmate():
            return -self.MATE_SCORE if maximizando else self.MATE_SCORE
        elif tabuleiro.is_game_over():
            return 0

        if profundidade == 0:
            return self.avalieTabuleiro(tabuleiro)

        if maximizando:
            melhor_movimento = -float("inf")
            movimentos = self.ordenarMovimentos(tabuleiro)
            for movimento in movimentos:
                tabuleiro.push(movimento)
                movimento_atual = self.minimax(profundidade - 1, tabuleiro, alpha,
                                               beta, not maximizando)
                if movimento_atual > self.MATE_THRESHOLD:
                    movimento_atual -= 1
                elif movimento_atual < -self.MATE_THRESHOLD:
                    movimento_atual += 1
                melhor_movimento = max(
                    melhor_movimento,
                    movimento_atual,
                )
                tabuleiro.pop()
                alpha = max(alpha, melhor_movimento)
                if beta <= alpha:
                    return melhor_movimento
            return melhor_movimento
        else:
            melhor_movimento = float("inf")
            moves = self.ordenarMovimentos(tabuleiro)
            for move in moves:
                tabuleiro.push(move)
                movimento_atual = self.minimax(profundidade - 1, tabuleiro, alpha,
                                               beta, not maximizando)
                if movimento_atual > self.MATE_THRESHOLD:
                    movimento_atual -= 1
                elif movimento_atual < -self.MATE_THRESHOLD:
                    movimento_atual += 1
                melhor_movimento = min(
                    melhor_movimento,
                    movimento_atual,
                )
                tabuleiro.pop()
                beta = min(beta, melhor_movimento)
                if beta <= alpha:
                    return melhor_movimento
            return melhor_movimento
