import pygame
import sys
import numpy as np
import random

# Constantes del juego
ROWS = 6
COLUMNS = 7
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)
width = COLUMNS * SQUARE_SIZE
height = (ROWS + 1) * SQUARE_SIZE
size = (width, height)

# Colores
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Inicializar Pygame
pygame.init()
font = pygame.font.SysFont("monospace", 75)
small_font = pygame.font.SysFont("monospace", 24)

# Crear el tablero
def create_board():
    board = np.zeros((ROWS, COLUMNS))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROWS-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Verificar horizontalmente
    for c in range(COLUMNS-3):
        for r in range(ROWS):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Verificar verticalmente
    for c in range(COLUMNS):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Verificar diagonales positivas
    for c in range(COLUMNS-3):
        for r in range(ROWS-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Verificar diagonales negativas
    for c in range(COLUMNS-3):
        for r in range(3, ROWS):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    for c in range(COLUMNS):
        for r in range(ROWS):
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
    
    for c in range(COLUMNS):
        for r in range(ROWS):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARE_SIZE+SQUARE_SIZE/2), height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
    pygame.display.update()

def main_menu():
    while True:
        screen.fill(BLACK)
        title = font.render("Conecta 4", True, BLUE)
        play_button = font.render("Jugar", True, RED)
        play_ai_button = font.render("Jugar contra IA", True, RED)
        how_to_button = font.render("Como Jugar", True, RED)
        exit_button = font.render("Salir", True, RED)

        title_rect = title.get_rect(center=(width / 2, height / 6))
        play_button_rect = play_button.get_rect(center=(width / 2, height / 3))
        play_ai_button_rect = play_ai_button.get_rect(center=(width / 2, height / 2))
        how_to_button_rect = how_to_button.get_rect(center=(width / 2, height / 1.5))
        exit_button_rect = exit_button.get_rect(center=(width / 2, height / 1.2))

        screen.blit(title, title_rect)
        screen.blit(play_button, play_button_rect)
        screen.blit(play_ai_button, play_ai_button_rect)
        screen.blit(how_to_button, how_to_button_rect)
        screen.blit(exit_button, exit_button_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    game_loop(False)
                if play_ai_button_rect.collidepoint(event.pos):
                    game_loop(True)
                if how_to_button_rect.collidepoint(event.pos):
                    how_to_play()
                if exit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def how_to_play():
    running = True
    while running:
        screen.fill(BLACK)
        instructions = [
            "Conecta 4 es un juego de dos jugadores.",
            "El objetivo es conectar 4 fichas del",
            "mismo color en una fila, columna o",
            "diagonal. Los jugadores se turnan",
            "para soltar una ficha en una columna.",
            "La ficha cae hasta la posición más baja",
            "disponible. El juego termina cuando",
            "un jugador gana o el tablero está lleno."
        ]

        y_offset = 50
        for line in instructions:
            text = small_font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(width / 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 40

        back_button = small_font.render("Volver", True, RED)
        back_button_rect = back_button.get_rect(center=(width / 2, height - 50))
        screen.blit(back_button, back_button_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    running = False

def pick_best_move(board, piece):
    valid_locations = [c for c in range(COLUMNS) if is_valid_location(board, c)]
    return random.choice(valid_locations)

def game_loop(vs_ai):
    board = create_board()
    game_over = False
    turn = 0

    draw_board(board)
    pygame.display.update()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE_SIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    posx = event.pos[0]
                    col = int(posx // SQUARE_SIZE)

                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1 if turn == 0 else 2)

                        if winning_move(board, 1 if turn == 0 else 2):
                            label = font.render(f"Jugador {1 if turn == 0 else 2} gana!!", True, RED if turn == 0 else YELLOW)
                            screen.blit(label, (40,10))
                            game_over = True

                        print_board(board)
                        draw_board(board)

                        turn = (turn + 1) % 2

        if turn == 1 and vs_ai and not game_over:
            col = pick_best_move(board, 2)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                pygame.time.wait(500)
                drop_piece(board, row, col, 2)

                if winning_move(board, 2):
                    label = font.render("Jugador 2 gana!!", True, YELLOW)
                    screen.blit(label, (40,10))
                    game_over = True

                print_board(board)
                draw_board(board)

                turn = 0

        if game_over:
            pygame.time.wait(3000)
            main_menu()

if __name__ == "__main__":
    screen = pygame.display.set_mode(size)
    main_menu()
