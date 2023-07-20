import pygame
import chess
import numpy as np


LIGHT_COLOR = (107, 142, 35)
DARK_COLOR = (85, 107, 47)
SELECTED_COLOR = (0, 255, 0)
VALID_MOVE_COLOR = (100, 100, 100)


class Inteligencia:
    def __init__(self):
        self.peaoTabuleiro = np.array([
            0, 0, 0, 0, 0, 0, 0, 0,
            5, 10, 10, -20, -20, 10, 10, 5,
            5, -5, -10, 0, 0, -10, -5, 5,
            0, 0, 0, 20, 20, 0, 0, 0,
            5, 5, 10, 25, 25, 10, 5, 5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
            0, 0, 0, 0, 0, 0, 0, 0])

        self.cavaloTabuleiro = [
            -50, -40, -30, -30, -30, -30, -40, -50,
            -40, -20, 0, 5, 5, 0, -20, -40,
            -30, 5, 10, 15, 15, 10, 5, -30,
            -30, 0, 15, 20, 20, 15, 0, -30,
            -30, 5, 15, 20, 20, 15, 5, -30,
            -30, 0, 10, 15, 15, 10, 0, -30,
            -40, -20, 0, 0, 0, 0, -20, -40,
            -50, -40, -30, -30, -30, -30, -40, -50]

        self.bispoTabuleiro = [
            -20, -10, -10, -10, -10, -10, -10, -20,
            -10, 5, 0, 0, 0, 0, 5, -10,
            -10, 10, 10, 10, 10, 10, 10, -10,
            -10, 0, 10, 10, 10, 10, 0, -10,
            -10, 5, 5, 10, 10, 5, 5, -10,
            -10, 0, 5, 10, 10, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -10, -10, -10, -10, -20]

        self.torreTabuleiro = [
            0, 0, 0, 5, 5, 0, 0, 0,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            -5, 0, 0, 0, 0, 0, 0, -5,
            5, 10, 10, 10, 10, 10, 10, 5,
            0, 0, 0, 0, 0, 0, 0, 0]

        self.rainhaTabuleiro = [
            -20, -10, -10, -5, -5, -10, -10, -20,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -10, 5, 5, 5, 5, 5, 0, -10,
            0, 0, 5, 5, 5, 5, 0, -5,
            -5, 0, 5, 5, 5, 5, 0, -5,
            -10, 0, 5, 5, 5, 5, 0, -10,
            -10, 0, 0, 0, 0, 0, 0, -10,
            -20, -10, -10, -5, -5, -10, -10, -20]
            
        self.reiTabuleiro = [
            20, 30, 10, 0, 0, 10, 30, 20,
            20, 20, 0, 0, 0, 0, 20, 20,
            -10, -20, -20, -20, -20, -20, -20, -10,
            -20, -30, -30, -40, -40, -30, -30, -20,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30,
            -30, -40, -40, -50, -50, -40, -40, -30]
        
    def getMovimentosCorAtual(self, tabuleiro):
        movimentos_cor = []

        for move in tabuleiro.legal_moves:
            if tabuleiro.piece_at(move.from_square).color == tabuleiro.turn:
                movimentos_cor.append(move)
        return movimentos_cor
        
    def avaliarTabuleiro(self, tabuleiro):
        if tabuleiro.is_checkmate():
            if tabuleiro.turn:
                return float('-inf')
            else:
                return float('inf')
        if tabuleiro.is_insufficient_material() or tabuleiro.is_stalemate():
            return 0
            
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

        material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)

        pawnsq = sum([self.peaoTabuleiro[i] for i in tabuleiro.pieces(chess.PAWN, chess.WHITE)])
        peoesTabuleiroBranco = tabuleiro.pieces(chess.PAWN, chess.WHITE)
        print(type(peoesTabuleiroBranco))
        teste = np.array(peoesTabuleiroBranco)
        print(teste)
        for i in peoesTabuleiroBranco:
            print(i)
        soma_peoes = np.sum(self.peaoTabuleiro[np.array(tabuleiro.pieces(chess.PAWN, chess.WHITE))])
        print(pawnsq == soma_peoes)
        pawnsq = pawnsq + sum([-self.peaoTabuleiro[chess.square_mirror(i)]
                                    for i in tabuleiro.pieces(chess.PAWN, chess.BLACK)])
        knightsq = sum([self.cavaloTabuleiro[i] for i in tabuleiro.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-self.cavaloTabuleiro[chess.square_mirror(i)]
                                        for i in tabuleiro.pieces(chess.KNIGHT, chess.BLACK)])
        bishopsq = sum([self.bispoTabuleiro[i] for i in tabuleiro.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq = bishopsq + sum([-self.bispoTabuleiro[chess.square_mirror(i)]
                                        for i in tabuleiro.pieces(chess.BISHOP, chess.BLACK)])
        rooksq = sum([self.torreTabuleiro[i] for i in tabuleiro.pieces(chess.ROOK, chess.WHITE)])
        rooksq = rooksq + sum([-self.torreTabuleiro[chess.square_mirror(i)]
                                    for i in tabuleiro.pieces(chess.ROOK, chess.BLACK)])
        queensq = sum([self.rainhaTabuleiro[i] for i in tabuleiro.pieces(chess.QUEEN, chess.WHITE)])
        queensq = queensq + sum([-self.rainhaTabuleiro[chess.square_mirror(i)]
                                    for i in tabuleiro.pieces(chess.QUEEN, chess.BLACK)])
        kingsq = sum([self.reiTabuleiro[i] for i in tabuleiro.pieces(chess.KING, chess.WHITE)])
        kingsq = kingsq + sum([-self.reiTabuleiro[chess.square_mirror(i)]
                                    for i in tabuleiro.pieces(chess.KING, chess.BLACK)])
            
        eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
        if tabuleiro.turn:
            return eval
        else:
            return -eval
            
    def quiesce(self, alpha, beta, tabuleiro):
        stand_pat = self.avaliarTabuleiro(tabuleiro)
        if (stand_pat >= beta):
            return beta
        if (stand_pat > alpha):
            alpha = stand_pat

        for move in tabuleiro.legal_moves:
            if tabuleiro.is_capture(move):
                tabuleiro.push(move)
                score = -self.quiesce(-beta, -alpha, tabuleiro)
                tabuleiro.pop()
                if (score >= beta):
                    return beta
                if (score > alpha):
                    alpha = score
        return alpha
            
    def alphabeta(self, alpha, beta, profundidadeleft, tabuleiro):
        bestscore = float('-inf')
        if (profundidadeleft == 0):
            return self.quiesce(alpha, beta, tabuleiro)
        for move in tabuleiro.legal_moves:
            tabuleiro.push(move)
            score = -self.alphabeta(-beta, -alpha, profundidadeleft - 1, tabuleiro)
            tabuleiro.pop()
            if (score >= beta):
                return score
            if (score > bestscore):
                bestscore = score
            if (score > alpha):
                alpha = score
        return bestscore
            
    def escolherMelhorMovimento(self, profundidade, tabuleiro):
        melhorAvaliacao = float('-inf')
        melhorMovimento = None
        alpha = float('-inf')
        beta = float('inf')

        
        for movimento in self.getMovimentosCorAtual(tabuleiro):
            tabuleiro.push(movimento)
            avaliacao = -self.alphabeta(-beta,-alpha, profundidade-1, tabuleiro)
            
            if avaliacao > melhorAvaliacao:
                melhorAvaliacao = avaliacao
                melhorMovimento = movimento

            if melhorAvaliacao > alpha:
                alpha = melhorAvaliacao
            tabuleiro.pop()

        return melhorMovimento
    
    def fazerMovimento(self, profundidade, tabuleiro):
        return self.escolherMelhorMovimento(profundidade, tabuleiro)


class ChessGame:
    def __init__(self, largura, altura, linhas, colunas):
        self.largura = largura
        self.altura = altura
        self.linhas = linhas
        self.colunas = colunas
        self.tamanho_quadrado = largura // colunas
        self.rodando = True
        self.tabuleiro = chess.Board()
        self.jogador_atual = chess.WHITE
        self.quadrado_selecionado = None
        self.screen = pygame.display.set_mode((largura, altura))
        self.movimentos_validos = []
        self.imagens_pecas = {}
        self.setPecas()
        pygame.init()

    def setPecas(self):
        pecas = ["wp", "wr", "wn", "wb", "wq",
                 "wk", "bp", "br", "bn", "bb", "bq", "bk"]
        for p in pecas:
            self.imagens_pecas[p] = pygame.image.load(f"images/{p}.png")

    def getMovimentosValidos(self):
        self.movimentos_validos = []
        for movimento in self.tabuleiro.legal_moves:
            if movimento.from_square == self.quadrado_selecionado:
                self.movimentos_validos.append(movimento.to_square)

    def checarEstadoJogo(self):
        if self.tabuleiro.is_checkmate():
            print("Xeque-mate!")
            return True
        elif self.tabuleiro.is_insufficient_material() or self.tabuleiro.is_stalemate():
            print("Empate!")
            return True
        else:
            return False

    def movimentoRoque(self, move):
        # Atualizar a posição do rei e da torre no tabuleiro
        self.tabuleiro.push(move)

        # Atualizar a variável de seleção atual e a vez do jogador atual
        self.quadrado_selecionado = None
        self.movimentos_validos = []
        self.jogador_atual = not self.jogador_atual

    def enPassantMovimento(self, move):
        # Atualizar a posição do peão e do peão adversário no tabuleiro
        self.tabuleiro.push(move)

        # Atualizar a variável de seleção atual e a vez do jogador atual
        self.quadrado_selecionado = None
        self.movimentos_validos = []
        self.jogador_atual = not self.jogador_atual

    def promocaoPeao(self, move, promotion_piece):
        # Atualizar a posição do peão e substituí-lo pela nova peça escolhida
        self.tabuleiro.push(move)
        self.tabuleiro.set_piece_at(move.to_square, promotion_piece)

        # Atualizar a variável de seleção atual e a vez do jogador atual
        self.quadrado_selecionado = None
        self.movimentos_validos = []
        self.jogador_atual = not self.jogador_atual

    def getPecaPromocao(self):
        peca_selecionada = input(
            "Digite a peça que deseja selecionar (q, r, n ou b): ")
        if peca_selecionada == "q":
            promotion_piece = chess.Piece(chess.QUEEN, self.jogador_atual)
        elif peca_selecionada == "r":
            promotion_piece = chess.Piece(chess.ROOK, self.jogador_atual)
        elif peca_selecionada == "n":
            promotion_piece = chess.Piece(chess.KNIGHT, self.jogador_atual)
        elif peca_selecionada == "b":
            promotion_piece = chess.Piece(chess.BISHOP, self.jogador_atual)
        else:
            self.promotion_piece()
        return promotion_piece

    def desenharTabuleiro(self):
        for row in range(self.linhas):
            for col in range(self.colunas):
                square_color = LIGHT_COLOR if (
                    row + col) % 2 == 0 else DARK_COLOR
                pygame.draw.rect(self.screen, square_color, (col * self.tamanho_quadrado,
                                                             row * self.tamanho_quadrado, self.tamanho_quadrado, self.tamanho_quadrado))

                # Destacar o quadrado selecionado
                if self.quadrado_selecionado and chess.square(col, self.linhas - 1 - row) == self.quadrado_selecionado:
                    pygame.draw.rect(self.screen, SELECTED_COLOR, (col * self.tamanho_quadrado,
                                                                   row * self.tamanho_quadrado, self.tamanho_quadrado, self.tamanho_quadrado))

                # Destacar as posições válidas para movimento com círculos
                if chess.square(col, self.linhas - 1 - row) in self.movimentos_validos:
                    circle_center = (col * self.tamanho_quadrado + self.tamanho_quadrado //
                                     2, row * self.tamanho_quadrado + self.tamanho_quadrado // 2)
                    pygame.draw.circle(self.screen, VALID_MOVE_COLOR,
                                       circle_center, self.tamanho_quadrado // 4)

                # Desenhar as peças no tabuleiro
                piece = self.tabuleiro.piece_at(
                    chess.square(col, self.linhas - 1 - row))
                if piece is not None:
                    if piece.symbol().islower():
                        piece_image = self.imagens_pecas["b"+piece.symbol()]
                    else:
                        piece_image = self.imagens_pecas["w" +
                                                         piece.symbol().lower()]
                    self.screen.blit(pygame.transform.scale(piece_image, (self.tamanho_quadrado, self.tamanho_quadrado)),
                                     (col * self.tamanho_quadrado, row * self.tamanho_quadrado))

    def loopGame(self):
        while self.rodando:
            if self.jogador_atual:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.rodando = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        # Obtendo a posição do clique do mouse
                        pos = pygame.mouse.get_pos()
                        col = pos[0] // self.tamanho_quadrado
                        row = pos[1] // self.tamanho_quadrado
                        square = chess.square(col, self.linhas - 1 - row)

                        if self.quadrado_selecionado is None:
                            # Se a posição inicial for válida e tiver uma peça do jogador atual
                            piece = self.tabuleiro.piece_at(square)
                            if piece is not None and piece.color == self.jogador_atual:
                                self.quadrado_selecionado = square
                                self.getMovimentosValidos()
                        else:
                            if square in self.movimentos_validos:
                                move = chess.Move(
                                    self.quadrado_selecionado, square)

                                if self.tabuleiro.is_castling(move):
                                    self.movimentoRoque(move)
                                elif self.tabuleiro.is_en_passant(move):
                                    self.enPassantMovimento(move)
                                elif (
                                    self.tabuleiro.piece_type_at(
                                        self.quadrado_selecionado) == chess.PAWN
                                    and chess.square_rank(square) in [0, 7]
                                ):
                                    promotion_piece = self.getPecaPromocao()
                                    print(promotion_piece)
                                    if promotion_piece is not None:
                                        # Executar a promoção do peão
                                        self.promocaoPeao(
                                            move, promotion_piece)
                                        promotion_piece = None
                                        if self.checarEstadoJogo():
                                            self.rodando = False
                                else:
                                    self.tabuleiro.push(move)
                                    self.quadrado_selecionado = None
                                    self.movimentos_validos = []
                                    self.jogador_atual = not self.jogador_atual
                                    if self.checarEstadoJogo():
                                        self.rodando = False
                            else:
                                self.quadrado_selecionado = None
                                self.movimentos_validos = []
            else:
                ia = Inteligencia()
                best_move = ia.fazerMovimento(3, self.tabuleiro)
                self.tabuleiro.push(best_move)
                self.quadrado_selecionado = None
                self.movimentos_validos = []
                self.jogador_atual = not self.jogador_atual
                if self.checarEstadoJogo():
                    self.rodando = False
            # Desenhar o tabuleiro
            self.desenharTabuleiro()

            pygame.display.flip()
        self.finalizar()

    def finalizar(self):
        # Finalizando o pygame
        pygame.quit()


def main():
    chessGame = ChessGame(800, 800, 8, 8)
    chessGame.desenharTabuleiro()
    chessGame.loopGame()
    chessGame.finalizar()


main()
