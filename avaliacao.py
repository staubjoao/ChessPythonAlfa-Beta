import chess


class Avaliacao:
    def __init__(self):

        # vetores que representam valores para cada peça no tabuleiro
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

        # valor de cada peça
        self.valor_pecas = {
            chess.PAWN: 100,
            chess.ROOK: 500,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.QUEEN: 900,
            chess.KING: 20000
        }

    # função que ordena os movimentos
    def ordenarMovimentos(self, tabuleiro):
        # verifica se está no final do jogo
        fim_de_jogo = self.verificarFimdeJogo(tabuleiro)

        # função para ordenar o movimento a partir do valor
        def orderer(move):
            return self.valorMovimento(tabuleiro, move, fim_de_jogo)

        # função lambda que ordena o movimento
        movimentos_ordenados = sorted(
            tabuleiro.legal_moves, key=orderer, reverse=(
                tabuleiro.turn == chess.WHITE)
        )
        # tranforma os movimentos ordenados em uma lista
        return list(movimentos_ordenados)

    # função que retorna o valor do movimento
    def valorMovimento(self, tabuleiro, movimento, fim_de_jogo):
        # se o movimento é de promoção, retorna infinto, ou seja, melhor movimento possivel a ser feito
        if movimento.promotion is not None:
            return -float("inf") if tabuleiro.turn == chess.BLACK else float("inf")

        # armazena a peça do movimento
        peca = tabuleiro.piece_at(movimento.from_square)
        diferenca = 0
        # caso a peça não seja nula
        if peca:
            # calcula o valor da jogda, faz a difereça do valor atual para o valor final
            valor_de = self.avaliePeca(
                peca, movimento.from_square, fim_de_jogo)
            valor_para = self.avaliePeca(
                peca, movimento.to_square, fim_de_jogo)
            diferenca = valor_para - valor_de
        # caso seja nula dispara uma exceção
        else:
            raise Exception(f"Espava-se uma peça: {movimento.from_square}")

        # variavel para calcular o valor de captura
        valor_captura = 0.0
        # se for um movimento de captura avalia o movimento
        if tabuleiro.is_capture(movimento):
            valor_captura = self.avaliarCaptura(tabuleiro, movimento)

        # valor do movimento
        valor_movimento_atual = valor_captura + diferenca
        # caso o tabuleiro esteja com as pretas nega o valor
        if tabuleiro.turn == chess.BLACK:
            valor_movimento_atual = -valor_movimento_atual
        # retorna o valor do movimento para ser validado
        return valor_movimento_atual

    # função que avalia a captura
    def avaliarCaptura(self, tabuleiro, movimento):
        # verifica se é um caso de en passant, se sim a captura é de um peão
        if tabuleiro.is_en_passant(movimento):
            return self.valor_pecas[chess.PAWN]

        # armazena as peças presentes no movimento
        movimento_de = tabuleiro.piece_at(movimento.to_square)
        movimento_para = tabuleiro.piece_at(movimento.from_square)
        # caso alguma deles seja nula dispara uma exceção
        if movimento_de is None or movimento_para is None:
            raise Exception(
                f"Espava-se uma(s) peça(s): {movimento.to_square} e {movimento.from_square}")
        # se não retorna o valor da captura
        return self.valor_pecas[movimento_de.piece_type] - self.valor_pecas[movimento_para.piece_type]

    # função que avalia uma peça
    def avaliePeca(self, peca, square, fim_de_jogo):
        # armazena o tipo da peça
        tipo_peca = peca.piece_type
        mapeamento = []
        # ao depender da tipo da peça e da cor da mesma, armazena em mapeamento o vetor que equivale ao tipo da peça
        # no caso se for preta armazena a lista invertida
        if tipo_peca == chess.PAWN:
            if peca.color == chess.WHITE:
                mapeamento = self.tabuleiro_peao
            else:
                mapeamento = list(reversed(self.tabuleiro_peao))

        if tipo_peca == chess.KNIGHT:
            mapeamento = self.tabuleiro_cavalo

        if tipo_peca == chess.BISHOP:
            if peca.color == chess.WHITE:
                mapeamento = self.tabuleiro_bispo
            else:
                mapeamento = list(reversed(self.tabuleiro_bispo))

        if tipo_peca == chess.ROOK:
            if peca.color == chess.WHITE:
                mapeamento = self.tabuleiro_torre
            else:
                mapeamento = list(reversed(self.tabuleiro_torre))

        if tipo_peca == chess.QUEEN:
            mapeamento = self.tabuleiro_rainha

        if tipo_peca == chess.KING:
            # no caso do rei, que tem valores diferentes para o fim de jogo armazena vetores diferentes caso estejá no fim
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

        # retorna o valor do mapeamento onde a pela se encontra
        return mapeamento[square]

    # função para avaliação do tabuleiro como um todo
    def avalieTabuleiro(self, tabuleiro):
        # verifica o checkmate, se sim retorna -inf ou inf, depende da cor atual
        if tabuleiro.is_checkmate():
            if tabuleiro.turn:
                return float('-inf')
            else:
                return float('inf')
        # verifica o empate por afogamento, se sim retorna 0
        if tabuleiro.is_insufficient_material() or tabuleiro.is_stalemate():
            return 0

        # armazena se está no fim do jogo
        fim_de_jogo = self.verificarFimdeJogo(tabuleiro)

        # calcula a quantidade de cada peça, brancas e pretas
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

        # a partir da diferença das quantidades calcula o material inicial do tabuleiro
        material = \
            self.valor_pecas[chess.PAWN] * (wp - bp) + \
            self.valor_pecas[chess.KING] * (wn - bn) + \
            self.valor_pecas[chess.BISHOP] * (wb - bb) + \
            self.valor_pecas[chess.ROOK] * (wr - br) + \
            self.valor_pecas[chess.QUEEN] * (wq - bq)

        peaosq = 0
        cavalosq = 0
        bisposq = 0
        torresq = 0
        rainhasq = 0
        reisq = 0

        # para cada quadrado presente no tabuleiro
        for quadrado in chess.SQUARES:
            # armazena a peça naquele quadrado
            peca = tabuleiro.piece_at(quadrado)

            # se não tiver peça pula o passo
            if not peca:
                continue

            # se tiver pega o valor daquela peça naquele quadrado
            valor = self.valor_pecas[peca.piece_type] + \
                self.avaliePeca(peca, quadrado, fim_de_jogo)

            # e para o tipo da peça soma ou subtrai da sua variavel, depende da cor
            tipo_peca = peca.piece_type
            if tipo_peca == chess.PAWN:
                if peca.color == chess.WHITE:
                    peaosq += valor
                else:
                    peaosq -= valor
            if tipo_peca == chess.KNIGHT:
                if peca.color == chess.WHITE:
                    cavalosq += valor
                else:
                    cavalosq -= valor
            if tipo_peca == chess.BISHOP:
                if peca.color == chess.WHITE:
                    bisposq += valor
                else:
                    bisposq -= valor
            if tipo_peca == chess.ROOK:
                if peca.color == chess.WHITE:
                    torresq += valor
                else:
                    torresq -= valor
            if tipo_peca == chess.QUEEN:
                if peca.color == chess.WHITE:
                    rainhasq += valor
                else:
                    rainhasq -= valor
            if tipo_peca == chess.KING:
                if peca.color == chess.WHITE:
                    reisq += valor
                else:
                    reisq -= valor

        # calculo final da função
        eval = material + peaosq + cavalosq + bisposq + torresq + rainhasq + reisq

        # retorna o valor eval ou -eval, depende da cor atual do turno
        if tabuleiro.turn:
            return eval
        else:
            return -eval

    # função que verifica o fim do jogo
    def verificarFimdeJogo(self, tabuleiro):
        # inicia as variaveis para a quantidade de rainhas e peças menores
        rainhas = 0
        menores = 0

        # para cada quadrado do tabuleiro
        for square in chess.SQUARES:
            pecas = tabuleiro.piece_at(square)
            # verifica se a peça presente naquele quadrado é uma rainha
            if pecas and pecas.piece_type == chess.QUEEN:
                rainhas += 1
            # verifica se a peça presente naquele quadrado é peça de valor menor (bispo e cavalo)
            if pecas and (
                pecas.piece_type == chess.BISHOP or pecas.piece_type == chess.KNIGHT
            ):
                menores += 1

        # se encontrar 0 rainhas ou 2 rainhas e 2 ou menos bispo/cavalo, é fim de jogo
        if rainhas == 0 or (rainhas == 2 and menores <= 2):
            return True

        # se não, não é
        return False
