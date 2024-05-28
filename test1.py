import pygame
import sys
import random

# Inicializace Pygame
pygame.init()

#hudba
pygame.mixer.music.load("menu_music.mp3")
game_music = pygame.mixer.Sound("game_music.mp3")
game_over_music = pygame.mixer.Sound("game_over_music.mp3")

# Nastavení rozměrů okna na celou obrazovku
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Flappy Bird")

# Definování barev
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Načtení obrázků
BIRD_IMG = pygame.image.load('ptak.png').convert_alpha()
BIRD_IMG = pygame.transform.scale(BIRD_IMG, (100, 100))  # Zvětšení ptáka
BG_IMG = pygame.image.load('pozadi.jpg').convert()
BG_IMG = pygame.transform.scale(BG_IMG, (WIDTH, HEIGHT))

# Herní proměnné
bird_x = 50
bird_y = HEIGHT // 2
bird_width = 100  # Nová velikost ptáka
bird_height = 100  # Nová velikost ptáka
bird_speed = 0
gravity = 0.5
jump = -10

pipe_width = 70
pipe_gap = 300  # Zvětšení mezery mezi trubkami
pipe_distance = 400  # Zmenšení vzdálenosti mezi trubkami pro zvýšení obtížnosti
pipes = []

score = 0
high_score = 0
font = pygame.font.Font(None, 72)

clock = pygame.time.Clock()
FPS = 60

# Funkce pro vytvoření trubek
def create_pipe(distance):
    pipe_height = random.randint(150, HEIGHT - pipe_gap - 150)
    top_pipe = pygame.Rect(WIDTH + distance, 0, pipe_width, pipe_height)
    bottom_pipe = pygame.Rect(WIDTH + distance, pipe_height + pipe_gap, pipe_width, HEIGHT - pipe_height - pipe_gap)
    return top_pipe, bottom_pipe

# Funkce pro pohyb trubek
def move_pipes(pipes):
    for pipe_pair in pipes:
        pipe_pair[0].x -= 5
        pipe_pair[1].x -= 5
    if pipes and pipes[0][0].x < -pipe_width:
        pipes.pop(0)

# Funkce pro vykreslení okna
def draw_window():
    WIN.blit(BG_IMG, (0, 0))
    WIN.blit(BIRD_IMG, (bird_x, bird_y))

    for top_pipe, bottom_pipe in pipes:
        pygame.draw.rect(WIN, GREEN, top_pipe)
        pygame.draw.rect(WIN, GREEN, bottom_pipe)

    score_text = font.render(f"Score: {int(score)}", True, BLACK)
    WIN.blit(score_text, (10, 10))

    high_score_text = font.render(f"High Score: {int(high_score)}", True, BLACK)
    WIN.blit(high_score_text, (10, 80))

    pygame.draw.rect(WIN, RED, (0, 0, WIDTH, 10))  # Horní hranice
    pygame.draw.rect(WIN, RED, (0, HEIGHT - 10, WIDTH, 10))  # Spodní hranice

    pygame.display.update()

# Funkce pro detekci kolizí
def check_collision():
    bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
    for pipe_pair in pipes:
        if pipe_pair[0].colliderect(bird_rect) or pipe_pair[1].colliderect(bird_rect):
            return True
    return False

# Funkce pro aktualizaci skóre
def update_score():
    global score, high_score
    score += 1
    if score > high_score:
        high_score = score

# Funkce pro hlavní herní smyčku
def main():
    global bird_y, bird_speed, pipes, score, high_score, passed_pipes

    bird_y = HEIGHT // 2
    bird_speed = 0
    pipes = [create_pipe(pipe_distance * i) for i in range(9999)]
    score = 0
    passed_pipes = []

    # Přehrávání hudby během hry
    pygame.mixer.music.load("game_music.mp3")
    pygame.mixer.music.play(-1)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_speed = jump
                if event.key == pygame.K_p:
                    pause_game()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        bird_speed += gravity
        bird_y += bird_speed

        move_pipes(pipes)

        global pipe_distance
        last_pipe_x = pipes[-1][0].x
        if last_pipe_x < WIDTH - pipe_distance:
            pipe_distance = random.randint(400, 600)
            pipes.append(create_pipe(pipe_distance))

        for pipe_pair in pipes:
            if pipe_pair not in passed_pipes and pipe_pair[0].x + pipe_width < bird_x:
                update_score()
                passed_pipes.append(pipe_pair)

        if check_collision() or bird_y < 0 or bird_y + bird_height > HEIGHT:
            game_over()
            return

        draw_window()

# Funkce pro pozastavení hry
def pause_game():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        pause_text = font.render("Paused. Press P to resume.", True, BLACK)
        WIN.blit(pause_text, (WIDTH // 4, HEIGHT // 2))
        pygame.display.update()
        clock.tick(5)

# Funkce pro odpočet před začátkem hry
def countdown():
    for i in range(3, 0, -1):
        WIN.blit(BG_IMG, (0, 0))
        countdown_text = font.render(str(i), True, BLACK)
        WIN.blit(countdown_text, (WIDTH // 2 - countdown_text.get_width() // 2, HEIGHT // 2 - countdown_text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(1000)

# Funkce pro ukončení hry
def game_over():
    global score, high_score
    over = True
    pygame.mixer.music.load("game_over_music.mp3")
    pygame.mixer.music.play(-1)
    if score > high_score:
        high_score = score
    while over:
        WIN.blit(BG_IMG, (0, 0))
        game_over_text = font.render("Game Over", True, BLACK)
        retry_text = font.render("Press R to Retry", True, BLACK)
        menu_text = font.render("Press M for Menu", True, BLACK)
        WIN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))
        WIN.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2))
        WIN.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 1.5))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    over = False
                    countdown()
                    main()
                if event.key == pygame.K_m:
                    over = False
                    game_menu()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Funkce pro menu
def game_menu():
    menu = True
    play_music()
    while menu:
        WIN.blit(BG_IMG, (0, 0))
        title_text = font.render("Fluffy Bird", True, BLACK)
        start_text = font.render("Press S to Start", True, BLACK)
        settings_text = font.render("Press C for Controls", True, BLACK)
        quit_text = font.render("Press Q to Quit", True, BLACK)

        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        WIN.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        WIN.blit(settings_text, (WIDTH // 2 - settings_text.get_width() // 2, HEIGHT // 1.5))
        WIN.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 1.2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    menu = False
                    countdown()
                    main()
                if event.key == pygame.K_c:
                    controls_menu()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Funkce pro menu s ovládáním
def controls_menu():
    controls = True
    volume = pygame.mixer.music.get_volume()
    while controls:
        WIN.blit(BG_IMG, (0, 0))
        controls_text = font.render("Press SPACE to fly", True, BLACK)
        volume_text = font.render(f"Volume: {int(volume * 100)}%", True, BLACK)
        back_text = font.render("Press B to go back", True, BLACK)
        increase_volume_text = font.render("Press + to increase volume", True, BLACK)
        decrease_volume_text = font.render("Press - to decrease volume", True, BLACK)
        stop_text = font.render("Press P to stop the game", True, BLACK)  # Přidáno tlačítko pro zastavení hry

        WIN.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT // 5))
        WIN.blit(volume_text, (WIDTH // 2 - volume_text.get_width() // 2, HEIGHT // 4))
        WIN.blit(increase_volume_text, (WIDTH // 2 - increase_volume_text.get_width() // 2, HEIGHT // 3))
        WIN.blit(decrease_volume_text, (WIDTH // 2 - decrease_volume_text.get_width() // 2, HEIGHT // 2.5))
        WIN.blit(stop_text, (WIDTH // 2 - stop_text.get_width() // 2, HEIGHT // 2))  # Zobrazení tlačítka pro zastavení hry
        WIN.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT // 1.2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    controls = False
                if event.key == pygame.K_UP:
                    volume = min(1, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
                if event.key == pygame.K_DOWN:
                    volume = max(0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)
                if event.key == pygame.K_p:  # Zastavení hry
                    controls = False

# Hlavní funkce pro přehrávání hudby
def play_music():
    pygame.mixer.music.load("menu_music.mp3")  # Načtení hudby
    pygame.mixer.music.play(-1)  # Nastavení opakování na nekonečno

game_menu()