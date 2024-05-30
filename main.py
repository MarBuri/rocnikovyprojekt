import pygame
import sys
import random

# Inicializace Pygame
pygame.init()

# Hudba
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
AVATARS = ['avatar1.png', 'avatar2.png', 'avatar3.png','avatar4.png','avatar5.png']  # Přidány další avatary
BG_IMG = pygame.image.load('pozadi1.jpg').convert()
BG_IMG = pygame.transform.scale(BG_IMG, (WIDTH, HEIGHT))

# Herní proměnné
bird_x = 50
bird_y = HEIGHT // 2
bird_width = 100
bird_height = 100
bird_speed = 0
gravity = 0.5
jump = -10

pipe_width = 70
pipe_gap = 300
pipe_distance = 400
pipes = []

score = 0
high_score = 0
font = pygame.font.Font(None, 72)

clock = pygame.time.Clock()
FPS = 60

current_avatar = 0
current_level = 'normální'

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
    BIRD_IMG = pygame.image.load(AVATARS[current_avatar]).convert_alpha()
    BIRD_IMG = pygame.transform.scale(BIRD_IMG, (100, 100))
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
    global bird_y, bird_speed, pipes, score, high_score, passed_pipes, pipe_gap

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
        pause_text = font.render("Paused. Press P to resume.", True, '#FFFF00')
        WIN.blit(pause_text, (WIDTH // 4, HEIGHT // 2))
        pygame.display.update()
        clock.tick(5)

# Funkce pro odpočet před začátkem hry
def countdown():
    for i in range(3, 0, -1):
        WIN.blit(BG_IMG, (0, 0))
        countdown_text = font.render(str(i), True, '#FFFF00')
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
        game_over_text = font.render("Game Over", True, '#FFFF00')
        retry_text = font.render("Press R to Retry", True, '#FFFF00')
        menu_text = font.render("Press M for Menu", True, '#FFFF00')
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
    global current_level, current_avatar, pipe_gap
    menu = True
    play_music()
    while menu:
        WIN.blit(BG_IMG, (0, 0))
        title_text = font.render("Flappy Bird", True, '#FFFF00')
        start_text = font.render("Press S to Start", True, '#FFFF00')
        settings_text = font.render("Press C for Controls", True, '#FFFF00')
        quit_text = font.render("Press Q to Quit", True, '#FFFF00')
        level_text = font.render(f"Level: {current_level}", True, '#FFFF00')
        avatar_text = font.render(f"Avatar: {current_avatar + 1}", True, '#FFFF00')

        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))
        WIN.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
        WIN.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 1.8))
        WIN.blit(avatar_text, (WIDTH // 2 - avatar_text.get_width() // 2, HEIGHT // 1.6))
        WIN.blit(settings_text, (WIDTH // 2 - settings_text.get_width() // 2, HEIGHT // 1.4))
        WIN.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 1.2))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    if current_level == 'jednoduchá':
                        pipe_gap = 400
                    elif current_level == 'normální':
                        pipe_gap = 300
                    elif current_level == 'těžká':
                        pipe_gap = 200
                    menu = False
                    countdown()
                    main()
                if event.key == pygame.K_c:
                    controls_menu()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_l:
                    current_level = choose_level()
                if event.key == pygame.K_a:
                    current_avatar = choose_avatar()

# Funkce pro výběr obtížnosti
def choose_level():
    choosing = True
    while choosing:
        WIN.blit(BG_IMG, (0, 0))
        easy_text = font.render("Press 1 for Easy", True, '#FFFF00')
        normal_text = font.render("Press 2 for Normal", True, '#FFFF00')
        hard_text = font.render("Press 3 for Hard", True, '#FFFF00')

        WIN.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2.5))
        WIN.blit(normal_text, (WIDTH // 2 - normal_text.get_width() // 2, HEIGHT // 2))
        WIN.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 1.5))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'jednoduchá'
                if event.key == pygame.K_2:
                    return 'normální'
                if event.key == pygame.K_3:
                    return 'těžká'

# Funkce pro výběr avataru
def choose_avatar():
    choosing = True
    while choosing:
        WIN.blit(BG_IMG, (0, 0))

        # Vykreslení textu pro výběr avatara
        avatar1_text = font.render("Press 1 for Avatar 1", True, '#FFFF00')
        avatar2_text = font.render("Press 2 for Avatar 2", True,'#FFFF00')
        avatar3_text = font.render("Press 3 for Avatar 3", True, '#FFFF00')
        avatar4_text = font.render("Press 4 for Avatar 4", True, '#FFFF00')
        avatar5_text = font.render("Press 5 for Avatar 5", True, '#FFFF00')

        # Posunutí textu pro každý avatar
        y_offset = HEIGHT // 2
        for avatar_text in [avatar1_text, avatar2_text, avatar3_text, avatar4_text, avatar5_text]:
            WIN.blit(avatar_text, (WIDTH // 2 - avatar_text.get_width() // 2, y_offset))
            y_offset += 100  # Posun o 50 pixelů dolů pro každý další text

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 0
                if event.key == pygame.K_2:
                    return 1
                if event.key == pygame.K_3:
                    return 2
                if event.key == pygame.K_4:
                    return 3
                if event.key == pygame.K_5:
                    return 4

# Funkce pro menu s ovládáním
def controls_menu():
    controls = True
    volume = pygame.mixer.music.get_volume()
    while controls:
        WIN.blit(BG_IMG, (0, 0))
        controls_text = font.render("Press SPACE to fly", True, '#FFFF00')
        volume_text = font.render(f"Volume: {int(volume * 100)}%", True, '#FFFF00')
        back_text = font.render("Press B to go back", True, BLACK)
        increase_volume_text = font.render("Press + to increase volume", True, '#FFFF00')
        decrease_volume_text = font.render("Press - to decrease volume", True, '#FFFF00')
        stop_text = font.render("Press P to stop the game", True, '#FFFF00')
        level_text = font.render("Press L to choose level", True, '#FFFF00')
        avatar_text = font.render("Press A to choose avatar", True, '#FFFF00')

        WIN.blit(controls_text, (WIDTH // 2 - controls_text.get_width() // 2, HEIGHT // 5))
        WIN.blit(volume_text, (WIDTH // 2 - volume_text.get_width() // 2, HEIGHT // 4))
        WIN.blit(increase_volume_text, (WIDTH // 2 - increase_volume_text.get_width() // 2, HEIGHT // 3))
        WIN.blit(decrease_volume_text, (WIDTH // 2 - decrease_volume_text.get_width() // 2, HEIGHT // 2.5))
        WIN.blit(stop_text, (WIDTH // 2 - stop_text.get_width() // 2, HEIGHT // 2))
        WIN.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, HEIGHT // 1.8))
        WIN.blit(avatar_text, (WIDTH // 2 - avatar_text.get_width() // 2, HEIGHT // 1.6))
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

# Hlavní funkce pro přehrávání hudby
def play_music():
    pygame.mixer.music.load("menu_music.mp3")  # Načtení hudby
    pygame.mixer.music.play(-1)  # Nastavení opakování na nekonečno

game_menu()