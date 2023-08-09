import chess
import time


class ChessIA:
    def __init__(self):
        self.tabuleiro_peao = [
            0,  0,  0,  0,  0,  0,  0,  0,
            5, 10, 10, -20, -20, 10, 10,  5,
            5, -5, -10,  0,  0, -10, -5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5,  5, 10, 25, 25, 10,  5,  5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0, 0, 0, 0, 0, 0, 0, 0]

        self.tabuleiro_cavalo = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50]

        self.tabuleiro_bispo = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10, 0, 10, 10, 10, 10, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20]

        self.tabuleiro_torre = [
            0, 0, 0, 5, 5, 0, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0]

        self.tabuleiro_rainha = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -5, 0, 5, 5, 5, 5, 0, -5,
            0, 0, 5, 5, 5, 5, 0, -5,
            -10, 5, 5, 5, 5, 5, 0, -10,
            -10, 0, 5, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20]

        self.tabuleiro_rei = [
            20, 30, 10, 0, 0, 10, 30, 20,
            20, 20, 0, 0, 0, 0, 20, 20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30]

        self.tabuleiro_rei_final = [
            50, -30, -30, -30, -30, -30, -30, -50,
            -30, -30,  0,  0,  0,  0, -30, -30,
            -30, -10, 20, 30, 30, 20, -10, -30,
            -30, -10, 30, 40, 40, 30, -10, -30,
            -30, -10, 30, 40, 40, 30, -10, -30,
            -30, -10, 20, 30, 30, 20, -10, -30,
            -30, -20, -10,  0,  0, -10, -20, -30,
            -50, -40, -30, -20, -20, -30, -40, -50]

        self.valor_pecas = {
            chess.PAWN: 100,
            chess.ROOK: 500,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.QUEEN: 900,
            chess.KING: 20000
        }

        self.nodes = 0
        self.tempo = 0

        self.teste1 = 0
        self.teste2 = 0

    def avaliarCaptura(self, tabuleiro, movimento):
        if tabuleiro.is_en_passant(movimento):
            return self.valor_pecas[chess.PAWN]
        movimento_de = tabuleiro.piece_at(movimento.to_square)
        movimento_para = tabuleiro.piece_at(movimento.from_square)
        if movimento_de is None or movimento_para is None:
            raise Exception(
                f"Espava-se uma(s) peça(s): {movimento.to_square} e {movimento.from_square}")
        return self.valor_pecas[movimento_de.piece_type] - self.valor_pecas[movimento_para.piece_type]

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

        for quadrado in chess.SQUARES:
            peca = tabuleiro.piece_at(quadrado)
            if not peca:
                continue

            value = self.valor_pecas[peca.piece_type] + \
                self.avaliePeca(peca, quadrado, fim_de_jogo)
            total += value if peca.color == chess.WHITE else -value

        return total

    def verificarFimdeJogo(self, tabuleiro):
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

    def selecionarMovimento(self, profundidade, tabuleiro):
        self.nodes = 0
        t0 = time.time()

        try:
            movimento = chess.polyglot.MemoryMappedReader(
                "./books/human.bin").weighted_choice(tabuleiro).move()
            return movimento
        except:
            melhor_avaliacao = -float("inf")
            alpha = -float("inf")
            beta = float("inf")
            movimentos = self.ordenarMovimentos(tabuleiro)
            melhor_movimento_encontrado = movimentos[0]

            for movimento in movimentos:
                tabuleiro.push(movimento)
                avaliacao = - \
                    self.minimax(profundidade-1, tabuleiro, -beta, -alpha)
                if avaliacao > melhor_avaliacao:
                    melhor_avaliacao = avaliacao
                    melhor_movimento_encontrado = movimento
                if avaliacao > alpha:
                    alpha = avaliacao
                tabuleiro.pop()
            movimento = melhor_movimento_encontrado

        print("quiesce", self.teste1)
        print("minimax", self.teste2)

        self.tempo = time.time() - t0
        return movimento, (self.nodes, self.tempo)

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

    def quiesce(self, tabuleiro, alpha, beta):
        self.teste1 += 1
        self.nodes += 1
        aux = self.avalieTabuleiro(tabuleiro)
        if aux >= beta:
            return beta
        if alpha < aux:
            alpha = aux

        # movimentos = self.ordenarMovimentos(tabuleiro)
        for movimento in tabuleiro.legal_moves:
            if tabuleiro.is_capture(movimento):
                tabuleiro.push(movimento)
                avalicao = -self.quiesce(tabuleiro, -beta, -alpha)
                tabuleiro.pop()
                if avalicao >= beta:
                    return beta
                if (avalicao > alpha):
                    alpha = avalicao
        return alpha

    def minimax(self, profundidade, tabuleiro, alpha, beta):
        self.teste2 += 1
        if profundidade == 0:
            return self.quiesce(tabuleiro, alpha, beta)
            # return self.avalieTabuleiro(tabuleiro)

        self.nodes += 1
        melhor_movimento = -float("inf")
        movimentos = self.ordenarMovimentos(tabuleiro)
        for movimento in movimentos:
            tabuleiro.push(movimento)
            movimento_atual = self.minimax(
                profundidade - 1, tabuleiro, -beta, -alpha)
            tabuleiro.pop()
            if movimento_atual >= beta:
                return movimento_atual
            if movimento_atual >= melhor_movimento:
                melhor_movimento = movimento_atual
            if movimento_atual > alpha:
                alpha = movimento_atual
        return melhor_movimento
