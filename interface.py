import pygame
import time

def print_grid(carac_screen, colors, size, puzzle):
    font = pygame.font.Font(None, 100)
    size_case = carac_screen["width"] / size

    color_line = colors["BLACK"]
    
    for i in range(1, size):
        pygame.draw.line(carac_screen["screen"], color_line, (0, size_case * i), (800, size_case * i), width=3)
        pygame.draw.line(carac_screen["screen"], color_line, (size_case * i, 0), (size_case * i, 800), width=3)

    for idx, value in enumerate(puzzle):
        if value == 0:
            continue

        row = idx // size
        col = idx % size

        x = col * size_case + size_case / 2
        y = row * size_case + size_case / 2

        text = font.render(str(value), True, colors["BLACK"])
        text_rect = text.get_rect(center=(x, y))
        carac_screen["screen"].blit(text, text_rect)

def make_swap(carac_screen, colors, size, puzzle, i1, i2):
    font = pygame.font.Font(None, 100)
    size_case = carac_screen["width"] / size
    duration = 0.7

    val1, val2 = puzzle[i1], puzzle[i2]
    moving_tile = val1 if val1 != 0 else val2

    start_row, start_col = divmod(i1, size)
    end_row, end_col = divmod(i2, size)

    end_x, end_y = start_col * size_case, start_row * size_case
    start_x, start_y = end_col * size_case, end_row * size_case

    steps = int(duration * 60)
    for step in range(steps + 1):
        t = step / steps
        current_x = start_x + (end_x - start_x) * t
        current_y = start_y + (end_y - start_y) * t

        carac_screen["screen"].fill(colors["WHITE"])
        print_grid(carac_screen, colors, size, puzzle)

        text = font.render(str(moving_tile), True, colors["BLACK"])
        text_rect = text.get_rect(center=(current_x + size_case/2, current_y + size_case/2))
        carac_screen["screen"].blit(text, text_rect)

        pygame.display.flip()
        carac_screen["clock"].tick(60)

    puzzle[i1], puzzle[i2] = puzzle[i2], puzzle[i1]

def animate_path(carac_screen, colors, size, chemin, puzzle):
    for i in range(len(chemin) - 1):
        next_puzzle = chemin[i + 1]
        i1 = puzzle.index(0)
        i2 = next_puzzle.index(0)
        make_swap(carac_screen, colors, size, puzzle, i1, i2)
    carac_screen["running"] = False

def show_game(size, puzzle, chemin):
    pygame.init()

    # Créer une fenêtre
    lenght = 800
    width = 800
    screen = pygame.display.set_mode((lenght, width))
    pygame.display.set_caption("n_puzzle")
    clock = pygame.time.Clock()

    colors = {
        "WHITE": (255, 255, 255),
        "BLACK": (0, 0, 0),
        "RED": (255, 0, 0),
        "GREEN": (0, 255, 0),
        "LIGHT_GREEN": (144, 238, 144),
        "BLUE": (0, 0, 255),
        "YELLOW": (255, 255, 0),
        "CYAN": (0, 255, 255),
        "MAGENTA": (255, 0, 255),
        "ORANGE": (255, 165, 0),
        "PURPLE": (128, 0, 128),
        "PINK": (255, 192, 203),
        "GREY": (128, 128, 128),
        "LIGHT_GREY": (200, 200, 200),
        "DARK_GREY": (50, 50, 50),
        "BROWN": (139, 69, 19),
        "LIGHT_BLUE": (173, 216, 230),
        "DARK_GREEN": (0, 100, 0)
    }

    carac_screen = {
        "screen": screen,
        "width": width,
        "lenght": lenght,
        "running": True,
        "clock": clock
    }

    carac_screen["screen"].fill(colors["WHITE"])
    print_grid(carac_screen, colors, size, puzzle)
    pygame.display.flip()
    time.sleep(2)

    # Boucle principale
    while carac_screen["running"]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carac_screen["running"] = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    carac_screen["running"] = False

        carac_screen["screen"].fill(colors["WHITE"])

        if carac_screen["running"]:
            animate_path(carac_screen, colors, size, chemin, puzzle)

    carac_screen["screen"].fill(colors["LIGHT_GREEN"])
    print_grid(carac_screen, colors, size, puzzle)
    pygame.display.flip()

    count = 0
    stop_game = False
    while count < 1000 and not stop_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                stop_game = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    stop_game = True
        time.sleep(0.01)
        count += 1
        
    pygame.quit()