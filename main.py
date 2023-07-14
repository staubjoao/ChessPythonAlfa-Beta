import pygame
import chess

# Definindo constantes
WIDTH = 800
HEIGHT = 800
ROWS = 8
COLS = 8
SQUARE_SIZE = WIDTH // COLS

# Cores
LIGHT_COLOR = (107,142,35)
DARK_COLOR = (85,107,47)
SELECTED_COLOR = (0, 255, 0)
VALID_MOVE_COLOR = (100, 100, 100)

# Inicializando o pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tabuleiro de Xadrez')

# Carregando as imagens das peças
pieces_images = {}
pieces = ["P", "R", "N", "B", "Q", "K", "p", "r", "n", "b", "q", "k"]
for piece in pieces:
    pieces_images[piece] = pygame.image.load(f"images/{piece}.png")

# Criando o objeto de tabuleiro de xadrez
board = chess.Board()

# Variáveis para armazenar o jogador atual e a seleção atual
current_player = chess.WHITE
selected_square = None
valid_moves = []

# Função para obter as posições válidas para movimento da peça selecionada
def get_valid_moves(square):
    valid_moves = []
    for move in board.legal_moves:
        if move.from_square == square:
            valid_moves.append(move.to_square)
    return valid_moves

# Função para verificar o estado do jogo
def check_game_state():
    if board.is_checkmate():
        print("Xeque-mate!")
        return True
    elif board.is_insufficient_material() or board.is_stalemate():
        print("Empate!")
        return True
    else:
        return False

# Loop principal do jogo
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Obtendo a posição do clique do mouse
            pos = pygame.mouse.get_pos()
            col = pos[0] // SQUARE_SIZE
            row = pos[1] // SQUARE_SIZE
            square = chess.square(col, ROWS - 1 - row)

            if selected_square is None:
                # Se a posição inicial for válida e tiver uma peça do jogador atual
                piece = board.piece_at(square)
                if piece is not None and piece.color == current_player:
                    selected_square = square
                    valid_moves = get_valid_moves(selected_square)
            else:
                # Movimento da peça
                if square in valid_moves:
                    move = chess.Move(selected_square, square)
                    board.push(move)
                    selected_square = None
                    valid_moves = []
                    current_player = not current_player
                    if check_game_state():
                        running = False
                else:
                    selected_square = None
                    valid_moves = []

    # Desenhar o tabuleiro
    for row in range(ROWS):
        for col in range(COLS):
            square_color = LIGHT_COLOR if (row + col) % 2 == 0 else DARK_COLOR
            pygame.draw.rect(screen, square_color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Destacar o quadrado selecionado
            if selected_square and chess.square(col, ROWS - 1 - row) == selected_square:
                pygame.draw.rect(screen, SELECTED_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Destacar as posições válidas para movimento com círculos
            if chess.square(col, ROWS - 1 - row) in valid_moves:
                circle_center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                pygame.draw.circle(screen, VALID_MOVE_COLOR, circle_center, SQUARE_SIZE // 4)

            # Desenhar as peças no tabuleiro
            piece = board.piece_at(chess.square(col, ROWS - 1 - row))
            if piece is not None:
                piece_image = pieces_images[piece.symbol()]
                screen.blit(pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE)),
                            (col * SQUARE_SIZE, row * SQUARE_SIZE))

    pygame.display.flip()

# Finalizando o pygame
pygame.quit()