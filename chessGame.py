import pygame
import chess
from chessIA import ChessIA
from stockfish import Stockfish
import os

LIGHT_COLOR = (107, 142, 35)
DARK_COLOR = (85, 107, 47)
SELECTED_COLOR = (0, 255, 0)
VALID_MOVE_COLOR = (100, 100, 100)


class ChessGame:
    def __init__(self, largura, altura, linhas, colunas, cor_jogador, nome_jogador, vs_stockfish, nivel_stockfish):
        self.largura = largura
        self.altura = altura
        self.linhas = linhas
        self.colunas = colunas
        self.tamanho_quadrado = largura // colunas
        self.cor_jogador = cor_jogador
        self.nome_jogador = nome_jogador
        self.vs_stockfish = vs_stockfish
        self.nivel_stockfish = nivel_stockfish
        self.button_clicked = False
        self.rodando = True
        self.tabuleiro = chess.Board()
        self.jogador_atual = chess.WHITE
        self.desistencia = False
        self.quadrado_selecionado = None
        self.movimentos_validos = []
        self.imagens_pecas = {}
        self.jogadas_brancas = []
        self.jogadas_pretas = []
        self.scores_brancas = []
        self.scores_pretas = []
        self.debug_info_nodes = []
        self.debug_info_time = []
        self.setPecas()

    def abrirTela(self):
        self.screen = pygame.display.set_mode((self.largura, self.altura))
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

    def getScore(self, cor):
        p = len(self.tabuleiro.pieces(chess.PAWN, cor))
        n = len(self.tabuleiro.pieces(chess.KNIGHT, cor))
        b = len(self.tabuleiro.pieces(chess.BISHOP, cor))
        r = len(self.tabuleiro.pieces(chess.ROOK, cor))
        q = len(self.tabuleiro.pieces(chess.QUEEN, cor))
        k = len(self.tabuleiro.pieces(chess.KING, cor))

        return p + n * 3 + b * 3 + r * 5 + q * 9 + k * 100

    def desistir(self):
        if self.jogador_atual:
            print("Jogador Preto venceu por desistência.")
        else:
            print("Jogador Branco venceu por desistência.")
        for square in chess.SQUARES:
            piece = self.tabuleiro.piece_at(square)
            if piece is not None and piece.piece_type == chess.KING and piece.color == self.jogador_atual:
                self.tabuleiro.remove_piece_at(square)
                break

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

    def enPassantMovimento(self, move):
        # Atualizar a posição do peão e do peão adversário no tabuleiro
        self.tabuleiro.push(move)

        # Atualizar a variável de seleção atual e a vez do jogador atual
        self.quadrado_selecionado = None
        self.movimentos_validos = []

    def promocaoPeao(self, move, promotion_piece):
        # Atualizar a posição do peão e substituí-lo pela nova peça escolhida
        self.tabuleiro.push(move)
        self.tabuleiro.set_piece_at(move.to_square, promotion_piece)

        # Atualizar a variável de seleção atual e a vez do jogador atual
        self.quadrado_selecionado = None
        self.movimentos_validos = []

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

    def setJogada(self, cor, move):
        xeque = 100 if self.tabuleiro.is_checkmate() else 0
        if cor:
            self.jogadas_brancas.append(move)
            self.scores_pretas.append(
                self.getScore(False)-xeque)
        else:
            self.jogadas_pretas.append(move)
            self.scores_brancas.append(
                self.getScore(True)-xeque)

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
                    self.desistir()
                    self.jogador_atual = not self.jogador_atual
                    self.checarEstadoJogo()
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
                                if promotion_piece is not None:
                                    # Executar a promoção do peão
                                    self.promocaoPeao(
                                        move, promotion_piece)
                                    promotion_piece = None
                            else:
                                self.tabuleiro.push(move)
                                self.quadrado_selecionado = None
                                self.movimentos_validos = []
                            self.setJogada(self.cor_jogador, move)
                            if self.checarEstadoJogo():
                                self.rodando = False
                            else:
                                self.jogador_atual = not self.jogador_atual
                        else:
                            self.quadrado_selecionado = None
                            self.movimentos_validos = []

    def salvarArquivoLog(self, ia):
        print(self.nome_jogador)
        try:
            with open(f"testes/{self.nome_jogador}.txt", "w") as file:
                cor_inteligencia = "pretas" if self.cor_jogador else "brancas"
                cor_ganhador = "brancas" if self.ganhador == 1 else "pretas" if self.ganhador == 0 else "empate"
                if self.button_clicked:
                    file.write("O jogador desistiu!\n")
                else:
                    file.write("O jogador jogou até o fim!\n")
                file.write(
                    f"A inteligencia estava jogando com as {cor_inteligencia}\n")
                file.write(f"O ganhador foram as {cor_ganhador}\n")
                file.write("Jogadas brancas:\n")
                for i in range(len(self.jogadas_brancas)):
                    file.write(str(self.jogadas_brancas[i]))
                    file.write(f", {self.scores_pretas[i]}\n")
                file.write("Jogadas pretas:\n")
                for i in range(len(self.jogadas_pretas)):
                    file.write(str(self.jogadas_pretas[i]))
                    file.write(f", {self.scores_brancas[i]}\n")
                if ia:
                    file.write("debug_info_ia_brancos:\n")
                    for i in range(len(self.debug_info_nodes)):
                        file.write(
                            f"nós: {self.debug_info_nodes[i][0]}, tempo: {self.debug_info_time[i][0]}\n")
                    file.write("debug_info_ia_pretos:\n")
                    for i in range(len(self.debug_info_nodes)):
                        file.write(
                            f"nós: {self.debug_info_nodes[i][1]}, tempo: {self.debug_info_time[i][1]}\n")
                else:
                    file.write("debug_info_ia:\n")
                    for i in range(len(self.debug_info_nodes)):
                        file.write(
                            f"nós: {self.debug_info_nodes[i]}, tempo: {self.debug_info_time[i]}\n")
        except Exception as e:
            print(f"Erro ao abrir o arquivo: {e}")

    def imprimirTabuleiro(self):
        tabuleiro_str = list(str(self.tabuleiro))
        unicode_pecas = {
            "R": "♖",
            "N": "♘",
            "B": "♗",
            "Q": "♕",
            "K": "♔",
            "P": "♙",
            "r": "♜",
            "n": "♞",
            "b": "♝",
            "q": "♛",
            "k": "♚",
            "p": "♟",
            ".": "·",
        }
        for i, char in enumerate(tabuleiro_str):
            if char in unicode_pecas:
                tabuleiro_str[i] = unicode_pecas[char]
        for i in tabuleiro_str:
            print(i, end="")

    def loopGame(self):
        ia = ChessIA()

        profundidade = 3
        while self.rodando:
            if self.cor_jogador == self.jogador_atual:
                self.getJogadaHumano()
            else:
                best_move, debug_info = ia.selecionarMovimento(
                    profundidade, self.tabuleiro)
                self.debug_info_nodes.append(debug_info[0])
                self.debug_info_time.append(debug_info[1])
                if best_move != None:
                    self.tabuleiro.push(best_move)
                    self.quadrado_selecionado = None
                    self.movimentos_validos = []
                    self.setJogada(not self.cor_jogador, best_move)
                    if self.checarEstadoJogo():
                        self.rodando = False
                    else:
                        self.jogador_atual = not self.jogador_atual
                else:
                    self.rodando = False

            # Desenhar o tabuleiro
            self.desenharTabuleiro()

            pygame.display.flip()
        self.salvarArquivoLog()
        self.finalizar()

    def loopGameStockFish(self, profundidade):
        ia = ChessIA()
        if os.name == "posix":
            stockfish = Stockfish(path='./stockfish_linux/stockfish-ubuntu-x86-64-avx2', depth=profundidade,
                                  parameters={"Threads": 4, "Minimum Thinking Time": 300, 'Hash': 2048})
        else:
            stockfish = Stockfish(path='stockfish\\stockfish-windows-x86-64-avx2.exe', depth=profundidade,
                                  parameters={"Threads": 4, "Minimum Thinking Time": 300, 'Hash': 2048})
        stockfish.set_elo_rating(self.nivel_stockfish)
        count = 0
        while self.rodando:
            if self.cor_jogador == self.jogador_atual:
                print("Vez do stockfish")
                stockfish.set_fen_position(self.tabuleiro.fen())
                best_move = chess.Move.from_uci(stockfish.get_best_move())

                self.tabuleiro.push(best_move)
                self.setJogada(self.cor_jogador, best_move)
                if self.checarEstadoJogo():
                    self.rodando = False
                else:
                    self.jogador_atual = not self.jogador_atual
            else:
                print("Vez da nossa IA")
                best_move, debug_info = ia.selecionarMovimento(
                    profundidade, self.tabuleiro)

                self.debug_info_nodes.append(debug_info[0])
                self.debug_info_time.append(debug_info[1])
                # passa o tabuleiro para o stockfish
                stockfish.set_fen_position(self.tabuleiro.fen())
                top_moves_sf = stockfish.get_top_moves(3)
                if best_move != None:
                    self.tabuleiro.push(best_move)
                    self.setJogada(not self.cor_jogador, best_move)
                if self.checarEstadoJogo():
                    self.rodando = False
                else:
                    self.jogador_atual = not self.jogador_atual
            if self.tabuleiro.can_claim_fifty_moves() or self.tabuleiro.can_claim_draw():
                self.rodando = False
                self.ganhador = 2

            self.imprimirTabuleiro()
            print()
            count += 1

        self.salvarArquivoLog()

    def loopGameIaxIA(self, profundidade):
        ia = ChessIA()
        count = 0
        while self.rodando:
            tempo = []
            nodes = []
            if self.jogador_atual:
                print("Vez das brancas")
                best_move, debug_info = ia.selecionarMovimento(
                    profundidade, self.tabuleiro)

                nodes.append(debug_info[0])
                tempo.append(debug_info[1])

                if best_move != None:
                    self.tabuleiro.push(best_move)
                    self.setJogada(self.jogador_atual, best_move)
                if self.checarEstadoJogo():
                    self.rodando = False
                else:
                    self.jogador_atual = not self.jogador_atual
            else:
                print("Vez das pretas")
                best_move, debug_info = ia.selecionarMovimento(
                    profundidade, self.tabuleiro)

                nodes.append(debug_info[0])
                tempo.append(debug_info[1])

                if best_move != None:
                    self.tabuleiro.push(best_move)
                    self.setJogada(self.jogador_atual, best_move)
                if self.checarEstadoJogo():
                    self.rodando = False
                else:
                    self.jogador_atual = not self.jogador_atual
            if self.tabuleiro.can_claim_fifty_moves() or self.tabuleiro.can_claim_draw():
                self.rodando = False
                self.ganhador = 2

            self.debug_info_nodes.append(nodes)
            self.debug_info_time.append(tempo)

            self.imprimirTabuleiro()
            print()
            count += 1

        self.salvarArquivoLog(True)

    def finalizar(self):
        # Finalizando o pygame
        pygame.quit()
