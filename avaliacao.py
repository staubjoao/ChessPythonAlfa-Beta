import chess


class Avaliacao:
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
            if fim_de_jogo:
                if peca.color == chess.WHITE:
                    mapeamento = self.tabuleiro_peao
                else:
                    mapeamento = list(reversed(self.tabuleiro_peao))
            else:
                if peca.color == chess.WHITE:
                    mapeamento = self.tabuleiro_peao_final
                else:
                    mapeamento = list(reversed(self.tabuleiro_peao_final))

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
