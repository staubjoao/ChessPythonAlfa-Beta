import chess
import time
import random


from multiprocessing import Manager
from pesto import *


class ChessIA:
    def __init__(self):
        self.movimento_nulo = True
        self.movimento_nulo_reducao = 2
        self.pontuacao_checkmate = 10**8
        self.limite_checkmate = 999*(10**4)
        self.quiesce_profundidade = 3
        self.nodes = 0
        self.tempo = 0

    # função que organiza os movimentos de forma simples
    def organizarMovimento(self, tabuleiro):
        movimentos = []
        movimentos_captura = []

        # para cada movimento presente no tabuleiro
        for movimento in tabuleiro.legal_moves:
            # armazena ele no vetor de capturas, se for um movimento de captura
            if tabuleiro.is_capture(movimento):
                movimentos_captura.append(movimento)
            # caso contrario armazena no vetor de movimentos de não captura
            else:
                movimentos.append(movimento)

        # aleatoriza os dois vetores
        random.shuffle(movimentos_captura)
        random.shuffle(movimentos)
        # retorna com os movimentos de captura vindo primeiro
        return movimentos_captura + movimentos

    # função que ordena os movimentos de captura
    def ordenarMovimentoQuiescence(self, tabuleiro):
        estagio = verificaEstagio(tabuleiro)
        # filtra por movimentos importantes para a busca quiescence
        movimentos_captura = filter(lambda movimento: tabuleiro.is_zeroing(
            movimento) or tabuleiro.gives_check(movimento), tabuleiro.legal_moves)
        # ordena os movimentos baseado na sua importancia
        movimentos = sorted(movimentos_captura, key=lambda movimento: self.avaliarMovimento(
            tabuleiro, movimento, estagio), reverse=(True if tabuleiro.turn == chess.BLACK else False))
        return movimentos

    # função que avalia um movimento com base do estagio atual do jogo
    def avaliarMovimento(self, tabuleiro, move, estagio):
        valor_movimento = 0

        # avalia as posiçẽos do movimento
        movimento_de = avaliarPeca(
            tabuleiro, move.from_square, estagio)
        movimento_para = avaliarPeca(
            tabuleiro, move.to_square, estagio)

        valor_movimento += movimento_para - movimento_de

        # avalia o movimento de captura
        if tabuleiro.is_capture(move):
            valor_movimento += avaliarCaptura(
                tabuleiro, move, estagio)

        # se a vez for das brancas retorna o valor positivo, se for das pretas, retorna negativo
        return -valor_movimento if tabuleiro.turn else valor_movimento

    # função que seleciona o movimento, recebe o tabuleiro, e a profundidade da busca
    def selecionarMovimento(self, profundidade, tabuleiro):
        # inicia a cache, para não calcular o que não precisa
        manager = Manager()
        cache = manager.dict()
        # inicializa o contador de nodes e o tempo
        self.nodes = 0
        t0 = time.time()

        melhor_movimento = self.minimax(
            tabuleiro, profundidade, self.movimento_nulo, cache, float("-inf"), float("inf"))[1]

        # coleta o tempo para estatistica
        self.tempo = time.time() - t0
        # retorna a melhor jogada e as estatiscas, nodes acessados e tempo
        return melhor_movimento, (self.nodes, self.tempo)

    # função para persistir jogadas caso encontre uma jogada de captura
    def quiesce(self, tabuleiro, alpha, beta, profundidade):
        self.nodes += 1

        if tabuleiro.is_stalemate():
            return 0

        if tabuleiro.is_checkmate():
            return -self.pontuacao_checkmate

        stand_pat = avaliacaoTabuleiro(tabuleiro)

        # para não rodar infinitamente
        if profundidade == 0:
            return stand_pat

        # poda beta
        if stand_pat >= beta:
            return beta

        # atualizar alpha
        if stand_pat > alpha:
            alpha = stand_pat

        # para cada movimento atual faz
        movimentos = self.ordenarMovimentoQuiescence(
            tabuleiro)
        for movimento in movimentos:
            # verifica se o movimento é de captura
            if tabuleiro.is_capture(movimento):
                # se sim realiza ele
                tabuleiro.push(movimento)
                # faz a chamada recursiva da função, trocando o beta por alpha e alpha por beta, e negando seus valores
                avalicao = -self.quiesce(tabuleiro, -
                                         beta, -alpha, profundidade-1)
                # remove a jogada
                tabuleiro.pop()
                # avalia, se a avaliação for maior ou igual a beta retorna beta
                if avalicao >= beta:
                    return beta
                # caso a avaliação seja maior doque alpha, alpha passa a valer a avaliação
                if avalicao > alpha:
                    alpha = avalicao
        # retorna alpha no final
        return alpha

    # função chave da ingeligencia, minmax com poda alphabeta
    def minimax(self, tabuleiro, profundidade, movimento_nulo, cache, alpha, beta):
        self.nodes += 1

        # verificação se o tabuleiro já foi avaliado
        if (tabuleiro.fen(), profundidade) in cache:
            # se sim, retorna a avaliação, isso é feito para poupar tempo de processamento
            return cache[(tabuleiro.fen(), profundidade)]

        # se o tabuleiro estiver em checkmate
        if tabuleiro.is_checkmate():
            # armazena o valor de checkmate na cache
            cache[(tabuleiro.fen(), profundidade)
                  ] = (-self.pontuacao_checkmate, None)
            # e retorna a pontuação de checkmate
            return (-self.pontuacao_checkmate, None)

        # verifica o empasse, parecido com o checkmate, porém o rei pode sair vivo
        if tabuleiro.is_stalemate():
            cache[(tabuleiro.fen(), profundidade)] = (0, None)
            return (0, None)

        # caso base da recursividade
        if profundidade <= 0:
            # avaliar tabuleiro atual
            # fazendo a chamada da função quiesce que avalia as jogadas de captura
            pontuacao_tabuleiro = self.quiesce(
                tabuleiro, alpha, beta, self.quiesce_profundidade)
            # armazena o valor na cache
            cache[(tabuleiro.fen(), profundidade)] = (
                pontuacao_tabuleiro, None)
            return pontuacao_tabuleiro, None

        # poda de movimento nulo
        if movimento_nulo and profundidade >= (self.movimento_nulo_reducao+1) and not tabuleiro.is_check():
            # avalia o tabuleiro
            pontuacao_tabuleiro = avaliacaoTabuleiro(tabuleiro)
            # se a pontuação for maior ou igual a beta
            if pontuacao_tabuleiro >= beta:
                # adiciona a jogada nula
                tabuleiro.push(chess.Move.null())
                # faz a chamada da função minmax, passando a profundidade menos 1 menos o movimento_nulo_reducao
                pontuacao_tabuleiro = - \
                    self.minimax(tabuleiro, profundidade - 1 - self.movimento_nulo_reducao,
                                 False, cache, -beta, -beta+1)[0]
                # remove a jogada
                tabuleiro.pop()
                # verifica a pontuação
                if pontuacao_tabuleiro >= beta:
                    # armazena a jogada
                    cache[(tabuleiro.fen(), profundidade)] = (beta, None)
                    # realiza a poda
                    return beta, None

        # inicializando melhor_pontuacao e melhor_movimento, como nulo e -infinito
        melhor_movimento = None
        melhor_pontuacao = float("-inf")
        movimentos = self.organizarMovimento(tabuleiro)

        # para todos os movimentos
        for movimento in movimentos:
            # realiza o movimento
            tabuleiro.push(movimento)
            # armazena a pontuação (chamada recursiva da função)
            pontuacao_tabuleiro = - \
                self.minimax(tabuleiro, profundidade-1, movimento_nulo,
                             cache, -beta, -alpha)[0]
            # se a pontuação for maior que o valor teto de checkmate
            if pontuacao_tabuleiro > self.limite_checkmate:
                # pontuação coletada decrementa um
                pontuacao_tabuleiro -= 1
            # se a pontuação for menor que o valor de teto checkmate negado
            if pontuacao_tabuleiro < -self.limite_checkmate:
                # pontuação coletada incrementa um
                pontuacao_tabuleiro += 1
            # remove a movimentação
            tabuleiro.pop()

            # poda beta
            # caso a pontuação atual seja maior ou igual a beta
            if pontuacao_tabuleiro >= beta:
                # armazena o valor
                cache[(tabuleiro.fen(), profundidade)] = (
                    pontuacao_tabuleiro, movimento)
                # realiza a poda
                return pontuacao_tabuleiro, movimento

            # atualiza melhor movimento
                # caso a pontuação atual seja maior que a melhor pontuação
            if pontuacao_tabuleiro > melhor_pontuacao:
                # atualiza
                melhor_pontuacao = pontuacao_tabuleiro
                melhor_movimento = movimento

            # definindo a variável alfa para fazer a poda
            # recebe o maior valor entre alpha e pontuacao_tabuleiro
            alpha = max(alpha, pontuacao_tabuleiro)

            # poda alfa beta quando já foi encontrada uma solução que é pelo menos tão boa quanto a atual
            # essas ramificações não serão capazes de influenciar a decisão final, então não é preciso perder tempo analisando-as
            if alpha >= beta:
                # realiza poda
                break

        # se não houver melhor movimento, faça um aleatório para não retornar nulo
        if not melhor_movimento:
            melhor_movimento = self.random_move(tabuleiro)

        # salva os resultados antes de retornar
        cache[(tabuleiro.fen(), profundidade)] = (
            melhor_pontuacao, melhor_movimento)
        return melhor_pontuacao, melhor_movimento
