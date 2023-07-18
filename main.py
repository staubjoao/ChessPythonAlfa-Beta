import pygame
import chess


LIGHT_COLOR = (107, 142, 35)
DARK_COLOR = (85, 107, 47)
SELECTED_COLOR = (0, 255, 0)
VALID_MOVE_COLOR = (100, 100, 100)


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
        self.movimentos_validos = []
        self.screen = pygame.display.set_mode((largura, altura))
        self.imagens_pecas = {}
        self.setPecas()
        pygame.init()

    def setPecas(self):
        pecas = ["wp", "wr", "wn", "wb", "wq",
                        "wk", "bp", "br", "bn", "bb", "bq", "bk"]
        for p in pecas:
            self.imagens_pecas[p] = pygame.image.load(f"images/{p}.png")

    def getMovimentosValidos(self, square):
        self.movimentos_validos = []
        for movimento in self.tabuleiro.legal_moves:
            if movimento.from_square == square:
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
        peca_selecionada = input("Digite a peça que deseja selecionar (q, r, n ou b): ")
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
                            self.getMovimentosValidos(self.quadrado_selecionado)
                    else:
                        if square in self.movimentos_validos:
                            move = chess.Move(self.quadrado_selecionado, square)

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
