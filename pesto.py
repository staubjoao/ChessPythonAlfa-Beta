# comentado!
import chess

# vetores que representam valores para cada peça no tabuleiro
# estão dividiso em vetoroes para o começo e meio do jogo, e para o fim
tabuleiro_peao = [
    0,   0,   0,   0,   0,   0,  0,   0,
    98, 134,  61,  95,  68, 126, 34, -11,
    -6,   7,  26,  31,  65,  56, 25, -20,
    -14,  13,   6,  21,  23,  12, 17, -23,
    -27,  -2,  -5,  12,  17,   6, 10, -25,
    -26,  -4,  -4, -10,   3,   3, 33, -12,
    -35,  -1, -20, -23, -15,  24, 38, -22,
    0,   0,   0,   0,   0,   0,  0,   0]

tabuleiro_peao_final = [
    0,   0,   0,   0,   0,   0,   0,   0,
    178, 173, 158, 134, 147, 132, 165, 187,
    94, 100,  85,  67,  56,  53,  82,  84,
    32,  24,  13,   5,  -2,   4,  17,  17,
    13,   9,  -3,  -7,  -7,  -8,   3,  -1,
    4,   7,  -6,   1,   0,  -5,  -1,  -8,
    13,   8,   8,  10,  13,   0,   2,  -7,
    0,   0,   0,   0,   0,   0,   0,   0]

tabuleiro_cavalo = [
    -167, -89, -34, -49,  61, -97, -15, -107,
    -73, -41,  72,  36,  23,  62,   7,  -17,
    -47,  60,  37,  65,  84, 129,  73,   44,
    -9,  17,  19,  53,  37,  69,  18,   22,
    -13,   4,  16,  13,  28,  19,  21,   -8,
    -23,  -9,  12,  10,  19,  17,  25,  -16,
    -29, -53, -12,  -3,  -1,  18, -14,  -19,
    -105, -21, -58, -33, -17, -28, -19,  -23]

tabuleiro_cavalo_final = [
    -58, -38, -13, -28, -31, -27, -63, -99,
    -25,  -8, -25,  -2,  -9, -25, -24, -52,
    -24, -20,  10,   9,  -1,  -9, -19, -41,
    -17,   3,  22,  22,  22,  11,   8, -18,
    -18,  -6,  16,  25,  16,  17,   4, -18,
    -23,  -3,  -1,  15,  10,  -3, -20, -22,
    -42, -20, -10,  -5,  -2, -20, -23, -44,
    -29, -51, -23, -15, -22, -18, -50, -64]

tabuleiro_bispo = [
    -29,   4, -82, -37, -25, -42,   7,  -8,
    -26,  16, -18, -13,  30,  59,  18, -47,
    -16,  37,  43,  40,  35,  50,  37,  -2,
    -4,   5,  19,  50,  37,  37,   7,  -2,
    -6,  13,  13,  26,  34,  12,  10,   4,
    0,  15,  15,  15,  14,  27,  18,  10,
    4,  15,  16,   0,   7,  21,  33,   1,
    -33,  -3, -14, -21, -13, -12, -39, -21]

tabuleiro_bispo_final = [
    -14, -21, -11,  -8, -7,  -9, -17, -24,
    -8,  -4,   7, -12, -3, -13,  -4, -14,
    2,  -8,   0,  -1, -2,   6,   0,   4,
    -3,   9,  12,   9, 14,  10,   3,   2,
    -6,   3,  13,  19,  7,  10,  -3,  -9,
    -12,  -3,   8,  10, 13,   3,  -7, -15,
    -14, -18,  -7,  -1,  4,  -9, -15, -27,
    -23,  -9, -23,  -5, -9, -16,  -5, -17]

tabuleiro_torre = [
    32,  42,  32,  51, 63,  9,  31,  43,
    27,  32,  58,  62, 80, 67,  26,  44,
    -5,  19,  26,  36, 17, 45,  61,  16,
    -24, -11,   7,  26, 24, 35,  -8, -20,
    -36, -26, -12,  -1,  9, -7,   6, -23,
    -45, -25, -16, -17,  3,  0,  -5, -33,
    -44, -16, -20,  -9, -1, 11,  -6, -71,
    -19, -13,   1,  17, 16,  7, -37, -26]

tabuleiro_torre_final = [
    13, 10, 18, 15, 12,  12,   8,   5,
    11, 13, 13, 11, -3,   3,   8,   3,
    7,  7,  7,  5,  4,  -3,  -5,  -3,
    4,  3, 13,  1,  2,   1,  -1,   2,
    3,  5,  8,  4, -5,  -6,  -8, -11,
    -4,  0, -5, -1, -7, -12,  -8, -16,
    -6, -6,  0,  2, -9,  -9, -11,  -3,
    -9,  2,  3, -1, -5, -13,   4, -20]

tabuleiro_rainha = [
    -28,   0,  29,  12,  59,  44,  43,  45,
    -24, -39,  -5,   1, -16,  57,  28,  54,
    -13, -17,   7,   8,  29,  56,  47,  57,
    -27, -27, -16, -16,  -1,  17,  -2,   1,
    -9, -26,  -9, -10,  -2,  -4,   3,  -3,
    -14,   2, -11,  -2,  -5,   2,  14,   5,
    -35,  -8,  11,   2,   8,  15,  -3,   1,
    -1, -18,  -9,  10, -15, -25, -31, -50]

tabuleiro_rainha_final = [
    -9,  22,  22,  27,  27,  19,  10,  20,
    -17,  20,  32,  41,  58,  25,  30,   0,
    -20,   6,   9,  49,  47,  35,  19,   9,
    3,  22,  24,  45,  57,  40,  57,  36,
    -18,  28,  19,  47,  31,  34,  39,  23,
    -16, -27,  15,   6,   9,  17,  10,   5,
    -22, -23, -30, -16, -16, -23, -36, -32,
    -33, -28, -22, -43,  -5, -32, -20, -41]

tabuleiro_rei = [
    -65,  23,  16, -15, -56, -34,   2,  13,
    29,  -1, -20,  -7,  -8,  -4, -38, -29,
    -9,  24,   2, -16, -20,   6,  22, -22,
    -17, -20, -12, -27, -30, -25, -14, -36,
    -49,  -1, -27, -39, -46, -44, -33, -51,
    -14, -14, -22, -46, -44, -30, -15, -27,
    1,   7,  -8, -64, -43, -16,   9,   8,
    -15,  36,  12, -54,   8, -28,  24,  14]

tabuleiro_rei_final = [
    -74, -35, -18, -18, -11,  15,   4, -17,
    -12,  17,  14,  17,  17,  38,  23,  11,
    10,  17,  23,  15,  20,  45,  44,  13,
    -8,  22,  24,  27,  26,  33,  26,   3,
    -18,  -4,  21,  24,  27,  23,   9, -11,
    -19,  -3,  11,  21,  23,  16,   7,  -9,
    -27, -11,   4,  13,  14,   4,  -5, -17,
    -53, -34, -21, -11, -28, -14, -24, -43]

# valores para cada peça
valor_pecas_teste = [
    82,  # peao
    337,  # cavalo
    365,  # bispo
    477,  # torre
    1025,  # rainha
    24000  # rei
]

valor_pecas_final_teste = [
    94,  # peao
    281,  # cavalo
    297,  # bispo
    512,  # torre
    936,  # rainha
    24000  # rei
]

# explicação dessa conta disponivel aqui: https://www.chessprogramming.org/Tapered_Eval
peao_estagio = 0
cavalo_estagio = 1
bispo_estagio = 1
torre_estagio = 2
rainha_estagio = 4
total_estagio = peao_estagio*16 + cavalo_estagio*4 + \
    bispo_estagio*4 + torre_estagio*4 + rainha_estagio*2


# retorna o valor da peça
def valorPeca(peca):
    peca_comeco_meio = 0
    peca_fim = 0
    if peca == chess.PAWN:
        peca_comeco_meio = valor_pecas_teste[0]
        peca_fim = valor_pecas_final_teste[0]
    elif peca == chess.KNIGHT:
        peca_comeco_meio = valor_pecas_teste[1]
        peca_fim = valor_pecas_final_teste[1]
    elif peca == chess.BISHOP:
        peca_comeco_meio = valor_pecas_teste[2]
        peca_fim = valor_pecas_final_teste[2]
    elif peca == chess.ROOK:
        peca_comeco_meio = valor_pecas_teste[3]
        peca_fim = valor_pecas_final_teste[3]
    elif peca == chess.QUEEN:
        peca_comeco_meio = valor_pecas_teste[4]
        peca_fim = valor_pecas_final_teste[4]
    elif peca == chess.KING:
        peca_comeco_meio = valor_pecas_teste[5]
        peca_fim = valor_pecas_final_teste[5]
    return peca_comeco_meio, peca_fim


# retorna o valor da peça em determinado quadrado, a partir da tabela
def valorPesto(peca, quadrado):
    pesto_comeco_meio = 0
    pesto_fim = 0

    mapeamento = []
    mapeamento_final = []

    if peca.piece_type == chess.PAWN:
        mapeamento = tabuleiro_peao
        mapeamento_final = tabuleiro_peao_final
    elif peca.piece_type == chess.KNIGHT:
        mapeamento = tabuleiro_cavalo
        mapeamento_final = tabuleiro_cavalo_final
    elif peca.piece_type == chess.BISHOP:
        mapeamento = tabuleiro_bispo
        mapeamento_final = tabuleiro_bispo_final
    elif peca.piece_type == chess.ROOK:
        mapeamento = tabuleiro_torre
        mapeamento_final = tabuleiro_torre_final
    elif peca.piece_type == chess.QUEEN:
        mapeamento = tabuleiro_rainha
        mapeamento_final = tabuleiro_rainha_final
    elif peca.piece_type == chess.KING:
        mapeamento = tabuleiro_rei
        mapeamento_final = tabuleiro_rei_final

    if peca.color == chess.WHITE:
        pesto_comeco_meio = mapeamento[63-quadrado]
        pesto_fim = mapeamento_final[63-quadrado]
    else:
        pesto_comeco_meio = mapeamento[quadrado]
        pesto_fim = mapeamento_final[quadrado]

    return pesto_comeco_meio, pesto_fim


# calcula estagio atual do jogo a partir do número de peças
def verificaEstagio(tabuleiro):
    # realiza a contagem das peças
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

    # cria um vetor de tuplas, contendo a contagem e o valor de estagio da peça
    pecas = [
        (wp, peao_estagio),
        (bp, peao_estagio),
        (wn, cavalo_estagio),
        (bn, cavalo_estagio),
        (wb, bispo_estagio),
        (bb, bispo_estagio),
        (wr, torre_estagio),
        (br, torre_estagio),
        (wq, rainha_estagio),
        (bq, rainha_estagio)]

    # variavel estagio é inicializada com o valor calculado anteriormente, fora da função
    estagio = total_estagio

    # para cada tupla presente no retorno da função contarPecas
    for qtdpeca, pecaestagio in pecas:
        # decrementa o valor atual do estagio pela contagem
        estagio -= qtdpeca * pecaestagio

    # calculo do estagio
    estagio = (estagio * 256 + (total_estagio / 2)) / total_estagio
    return estagio


# função que realiza avaliação do tabuleiro
def avaliacaoTabuleiro(tabuleiro):
    # verifica o estagio atual
    estagio = verificaEstagio(tabuleiro)

    aval_meio_b = 0
    aval_meio_p = 0

    aval_fim_b = 0
    aval_fim_p = 0

    # percorrer todos os quadrados e somar os valores das peças para ambos os lados
    # função retirada daqui: https://www.chessprogramming.org/PeSTO%27s_Evaluation_Function
    for quadrado in range(64):
        peca = tabuleiro.piece_at(quadrado)
        if peca is not None:
            val_peca, val_peca_final = valorPeca(peca.piece_type)
            pesto_valor, pesto_valor_final = valorPesto(peca, quadrado)
            if peca.color == chess.WHITE:
                aval_meio_b += pesto_valor + val_peca
                aval_fim_b += pesto_valor_final + val_peca_final
            # se não realiza os calculos no tabuleiro "normal"
            else:
                aval_meio_p += pesto_valor + val_peca
                aval_fim_p += pesto_valor_final + val_peca_final

    # avalia o tabuleiro com base no estagio local
    avaliacao_meio = 0
    avaliacao_fim = 0
    if tabuleiro.turn:
        avaliacao_meio = aval_meio_b - aval_meio_p
        avaliacao_fim = aval_fim_b - aval_meio_p
    else:
        avaliacao_meio = aval_meio_p - aval_meio_b
        avaliacao_fim = aval_fim_p - aval_meio_b

    # calcula a avaliação
    return ((avaliacao_meio * (256 - estagio)) +
            (avaliacao_fim * estagio)) / 256


# função que avaliaca a peça presente em um quadrado do tabuleiro
def avaliarPeca(tabuleiro, quadrado, estagio):
    pontuacao_meio = 0
    pontuacao_fim = 0

    # calcula a pontuacao para o meio e fim d jogo para a peça
    peca = tabuleiro.piece_at(quadrado)
    if peca is not None:
        val_peca, val_peca_final = valorPeca(peca.piece_type)
        pesto_valor, pesto_valor_final = valorPesto(peca, quadrado)

        pontuacao_meio += pesto_valor + val_peca
        pontuacao_fim += pesto_valor_final + val_peca_final

    # calcula a avaliação
    return ((pontuacao_meio * (256 - estagio)) + (pontuacao_fim * estagio)) / 256


# função que avalia a captura, se baseando no estagio do jogo
def avaliarCaptura(tabuleiro, movimento, estagio):
    pontuacao_meio = 0
    pontuacao_fim = 0

    # pontuação do en passant
    if tabuleiro.is_en_passant(movimento):
        return 0

    peca_captura = tabuleiro.piece_at(movimento.from_square).piece_type
    peca_capturada = tabuleiro.piece_at(movimento.to_square).piece_type

    # armazena a diferença entre as duas peças
    if peca_captura is not None and peca_capturada is not None:
        val_capturada, val_capturada_fim = valorPeca(peca_capturada)
        val_captura, val_captura_fim = valorPeca(peca_captura)

        pontuacao_meio += val_capturada - val_captura
        pontuacao_fim += val_capturada_fim - val_captura_fim

    # calcula a avaliação
    return ((pontuacao_meio * (256 - estagio)) + (pontuacao_fim * estagio)) / 256
