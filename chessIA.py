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

        self.peao_valor = 100
        self.torre_valor = 500
        self.cavalo_valor = 320
        self.bispo_valor = 330
        self.rainha_valor = 900

        self.MATE_SCORE = 1000000000
        self.MATE_THRESHOLD = 999000000

        self.nodes = 0
        self.tempo = 0

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

        if peca.color == chess.WHITE:
            return mapeamento[square]
        else:
            return -mapeamento[square]

    def avalieTabuleiro(self, tabuleiro):
        if tabuleiro.is_checkmate():
            if tabuleiro.turn:
                return float('-inf')
            else:
                return float('inf')
        if tabuleiro.is_insufficient_material() or tabuleiro.is_stalemate():
            return 0
        total = 0
        fim_de_jogo = self.verificarFimdeJogo(tabuleiro)

        qtd_peao_branco = len(tabuleiro.pieces(chess.PAWN, chess.WHITE))
        qtd_cavalo_branco = len(tabuleiro.pieces(chess.KNIGHT, chess.WHITE))
        qtd_bispo_branco = len(tabuleiro.pieces(chess.BISHOP, chess.WHITE))
        qtd_torre_branco = len(tabuleiro.pieces(chess.ROOK, chess.WHITE))
        qtd_rainha_branco = len(tabuleiro.pieces(chess.QUEEN, chess.WHITE))
        qtd_peao_preto = len(tabuleiro.pieces(chess.PAWN, chess.BLACK))
        qtd_cavalo_preto = len(tabuleiro.pieces(chess.KNIGHT, chess.BLACK))
        qtd_bispo_preto = len(tabuleiro.pieces(chess.BISHOP, chess.BLACK))
        qtd_torre_preto = len(tabuleiro.pieces(chess.ROOK, chess.BLACK))
        qtd_rainha_preto = len(tabuleiro.pieces(chess.QUEEN, chess.BLACK))

        material = (
            self.peao_valor * (qtd_peao_branco - qtd_peao_preto)
            + self.cavalo_valor * (qtd_cavalo_branco - qtd_cavalo_preto)
            + self.bispo_valor * (qtd_bispo_branco - qtd_bispo_preto)
            + self.torre_valor * (qtd_torre_branco - qtd_torre_preto)
            + self.rainha_valor * (qtd_rainha_branco - qtd_rainha_preto)
        )

        peaosq = 0
        cavalosq = 0
        bisposq = 0
        torresq = 0
        rainhasq = 0
        reisq = 0

        for square in chess.SQUARES:
            peca = tabuleiro.piece_at(square)
            if not peca:
                continue

            valor = self.avaliePeca(peca, square, fim_de_jogo)
            if peca.piece_type == chess.PAWN:
                peaosq += valor
            if peca.piece_type == chess.KNIGHT:
                cavalosq += valor
            if peca.piece_type == chess.BISHOP:
                bisposq += valor
            if peca.piece_type == chess.ROOK:
                torresq += valor
            if peca.piece_type == chess.QUEEN:
                rainhasq += valor
            if peca.piece_type == chess.KING:
                reisq += valor

        eval = material + peaosq + cavalosq + bisposq + torresq + rainhasq + reisq

        if tabuleiro.turn:
            return eval
        else:
            return -eval

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

    def selecionarMovimento(self, profundidade, tabuleiro, debug):
        self.nodes = 0
        t0 = time.time()

        movimento = self.minimaxRoot(profundidade, tabuleiro)

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

    def minimaxRoot(self, profundidade, tabuleiro):
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
            return melhor_movimento_encontrado

    def quiesce(self, tabuleiro, alpha, beta):
        self.nodes += 1
        aux = self.avalieTabuleiro(tabuleiro)
        if aux >= beta:
            return beta
        if aux > alpha:
            alpha = aux

        movimentos = self.ordenarMovimentos(tabuleiro)
        for movimento in movimentos:
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
        self.nodes += 1
        if profundidade == 0:
            return self.quiesce(tabuleiro, alpha, beta)

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
