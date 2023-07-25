import pygame
import chess
from chessIA import ChessIA

LIGHT_COLOR = (107, 142, 35)
DARK_COLOR = (85, 107, 47)
SELECTED_COLOR = (0, 255, 0)
VALID_MOVE_COLOR = (100, 100, 100)


class ChessGame:
    def __init__(self, largura, altura, linhas, colunas, cor_jogador, nome_jogador):
        self.largura = largura
        self.altura = altura
        self.linhas = linhas
        self.colunas = colunas
        self.tamanho_quadrado = largura // colunas
        self.cor_jogador = cor_jogador
        self.cor_inteligencia = not self.cor_jogador
        self.nome_jogador = nome_jogador
        self.rodando = True
        self.tabuleiro = chess.Board()
        self.jogador_atual = chess.WHITE
        self.desistencia = False
        self.quadrado_selecionado = None
        self.screen = pygame.display.set_mode((largura, altura))
        self.movimentos_validos = []
        self.imagens_pecas = {}
        self.numero_jogadas_pretas = 0
        self.numero_jogadas_brancas = 0
        self.pecas_capturadas_brancas = []
        self.pecas_capturadas_pretas = []
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

    def desistir(self):
        self.surrendered = True
        if self.jogador_atual == chess.WHITE:
            print("Jogador Preto venceu por desistência.")
        else:
            print("Jogador Branco venceu por desistência.")

    def checarEstadoJogo(self):
        if self.tabuleiro.is_checkmate():
            print("Xeque-mate!")
            if self.jogador_atual:
                self.ganhador = 1
            else:
                self.ganhador = 0
            return True
        elif self.tabuleiro.is_insufficient_material() or self.tabuleiro.is_stalemate():
            print("Empate!")
            self.ganhador = 2
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

    def desenharBotaoDesistir(self):
        font = pygame.font.Font(None, 36)
        button_text = font.render("Desistir", True, (255, 255, 255))
        button_rect = button_text.get_rect(
            center=(self.largura // 2, self.altura - 30))
        pygame.draw.rect(self.screen, (255, 0, 0), button_rect)
        self.screen.blit(button_text, button_rect)

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
        self.desenharBotaoDesistir()

    def getJogadaHumano(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.rodando = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Obtendo a posição do clique do mouse
                pos = pygame.mouse.get_pos()
                col = pos[0] // self.tamanho_quadrado
                row = pos[1] // self.tamanho_quadrado
                square = chess.square(col, self.linhas - 1 - row)

                if self.largura // 2 - 50 <= pos[0] <= self.largura // 2 + 50 and self.altura - 75 <= pos[1] <= self.altura - 25:
                    self.button_clicked = True
                    self.ganhador = 0 if self.cor_jogador else 1
                    self.rodando = False
                else:
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
                                if self.cor_jogador:
                                    self.numero_jogadas_brancas += 1
                                else:
                                    self.numero_jogadas_pretas += 1
                        else:
                            self.quadrado_selecionado = None
                            self.movimentos_validos = []

    def salvarArquivoLog(self):
        try:
            with open(self.nome_jogador+'.txt', 'w') as file:
                cor_ganhador = "brancas" if self.ganhador == 1 else "pretas" if self.ganhador == 0 else "empate"
                file.write(f"O ganhador foram as peças {cor_ganhador} ")
                if self.cor_inteligencia:
                    if cor_ganhador == "brancas":
                        file.write("a inteligencia desenvolvida ganhou!")
                    
                file.write(
                    f"O número de jogadas das peças pretas foi de {self.numero_jogadas_pretas}\n")
                file.write(
                    f"O número de jogadas das peças brancas foi de {self.numero_jogadas_brancas}\n")
                file.write("Peças brancas capturadas: ")
                for i, j in enumerate(self.pecas_capturadas_brancas):
                    if j == len(self.pecas_capturadas_brancas) - 1:
                        file.write(f"{i}\n")
                    else:
                        file.write(f"{i}, ")
                file.write("Peças pretas capturadas: ")
                for i, j in enumerate(self.pecas_capturadas_pretas):
                    if j == len(self.pecas_capturadas_pretas) - 1:
                        file.write(f"{i}\n")
                    else:
                        file.write(f"{i}, ")
        except Exception as e:
            print(f"Erro ao abrir o arquivo: {e}")

    def loopGame(self):
        ia = ChessIA()
        while self.rodando:
            if self.cor_jogador == self.jogador_atual:
                self.getJogadaHumano()
            else:
                best_move = ia.fazerMovimento(3, self.tabuleiro)
                self.tabuleiro.push(best_move)
                self.quadrado_selecionado = None
                self.movimentos_validos = []
                self.jogador_atual = not self.jogador_atual
                if self.cor_jogador:
                    self.numero_jogadas_pretas += 1
                else:
                    self.numero_jogadas_brancas += 1
                if self.checarEstadoJogo():
                    self.rodando = False
            # Desenhar o tabuleiro
            self.desenharTabuleiro()

            pygame.display.flip()
        self.salvarArquivoLog()
        self.finalizar()

    def finalizar(self):
        # Finalizando o pygame
        pygame.quit()
