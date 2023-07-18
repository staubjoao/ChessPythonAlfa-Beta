import pygame
import chess


LIGHT_COLOR = (107, 142, 35)
DARK_COLOR = (85, 107, 47)
SELECTED_COLOR = (0, 255, 0)
VALID_MOVE_COLOR = (100, 100, 100)


class ChessGame:
    def __init__(self, width, height, rows, cols) -> None:
        self.width = width
        self.height = height
        self.rows = rows
        self.cols = cols
        self.square_size = width // cols

        self.running = True

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))

        self.pieces_images = {}
        pieces = ["wp", "wr", "wn", "wb", "wq", "wk", "bp", "br", "bn", "bb", "bq", "bk"]
        for piece in pieces:
            self.pieces_images[piece] = pygame.image.load(
                f"images/{piece}.png")

        self.board = chess.Board()

        self.current_player = chess.WHITE
        self.selected_square = None
        self.valid_moves = []

    def get_valid_moves(self, square):
        self.valid_moves = []
        for move in self.board.legal_moves:
            if move.from_square == square:
                self.valid_moves.append(move.to_square)

    def check_game_state(self):
        if self.board.is_checkmate():
            print("Xeque-mate!")
            return True
        elif self.board.is_insufficient_material() or self.board.is_stalemate():
            print("Empate!")
            return True
        else:
            return False

    def desenhar_tabuleiro(self):
        for row in range(self.rows):
            for col in range(self.cols):
                square_color = LIGHT_COLOR if (
                    row + col) % 2 == 0 else DARK_COLOR
                pygame.draw.rect(self.screen, square_color, (col * self.square_size,
                                                             row * self.square_size, self.square_size, self.square_size))

                # Destacar o quadrado selecionado
                if self.selected_square and chess.square(col, self.rows - 1 - row) == self.selected_square:
                    pygame.draw.rect(self.screen, SELECTED_COLOR, (col * self.square_size,
                                                                   row * self.square_size, self.square_size, self.square_size))

                # Destacar as posições válidas para movimento com círculos
                if chess.square(col, self.rows - 1 - row) in self.valid_moves:
                    circle_center = (col * self.square_size + self.square_size //
                                     2, row * self.square_size + self.square_size // 2)
                    pygame.draw.circle(self.screen, VALID_MOVE_COLOR,
                                       circle_center, self.square_size // 4)

                # Desenhar as peças no tabuleiro
                piece = self.board.piece_at(
                    chess.square(col, self.rows - 1 - row))
                if piece is not None:
                    if piece.symbol().islower():
                        piece_image = self.pieces_images["b"+piece.symbol()]
                    else:
                        piece_image = self.pieces_images["w"+piece.symbol().lower()]
                    self.screen.blit(pygame.transform.scale(piece_image, (self.square_size, self.square_size)),
                                     (col * self.square_size, row * self.square_size))

    def loop_game(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Obtendo a posição do clique do mouse
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // self.square_size
                    row = pos[1] // self.square_size
                    square = chess.square(col, self.rows - 1 - row)

                    if self.selected_square is None:
                        # Se a posição inicial for válida e tiver uma peça do jogador atual
                        piece = self.board.piece_at(square)
                        if piece is not None and piece.color == self.current_player:
                            self.selected_square = square
                            self.get_valid_moves(self.selected_square)
                    else:
                        if square in self.valid_moves:
                            move = chess.Move(self.selected_square, square)
                            self.board.push(move)
                            self.selected_square = None
                            self.valid_moves = []
                            self.current_player = not self.current_player
                            if self.check_game_state():
                                self.running = False
                        else:
                            self.selected_square = None
                            self.valid_moves = []

            # Desenhar o tabuleiro
            self.desenhar_tabuleiro()

            pygame.display.flip()
        self.finalizar()

    def finalizar(self):
        # Finalizando o pygame
        pygame.quit()


def main():
    chessGame = ChessGame(800, 800, 8, 8)
    chessGame.desenhar_tabuleiro()
    chessGame.loop_game()


main()
