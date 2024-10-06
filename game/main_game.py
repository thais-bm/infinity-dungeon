import pygame
import phase_1
import sys

pygame.init()

COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 180, 0)
COLOR_RED = (194, 24, 7)
COLOR_PINK = (255, 182, 193)
COLOR_BLACK = (0, 0, 0)

play_text = 'PLAY'
exit_text = 'EXIT'

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
size = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tower Of God")

# Menu loop
main_menu = True
ins = True
game_clock = pygame.time.Clock()

# Song
sound = pygame.mixer.Sound("assets/audio/mists-in-the-elven-lands-127808.mp3")
pygame.mixer.Sound.play(sound, loops=-1)

def how_to_play():
    bg_img = pygame.image.load('assets/ins_basic.png')
    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        break

            screen.blit(bg_img, (0, 0))
            pygame.display.flip()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                break

    pygame.quit()
    phase_1.iniciar()
    sys.exit()


while main_menu:
    # Menu background
    screen.fill(COLOR_BLACK)

    # Mouse position
    MENU_MOUSE_POS = pygame.mouse.get_pos()

    # Game name in Menu
    menu_font = pygame.font.Font('assets/SegaArcadeFont-Regular.ttf', 50)
    game_name = menu_font.render('Infinite Dungeon', True, COLOR_WHITE)
    game_name_rect = game_name.get_rect(center=(SCREEN_WIDTH//4, SCREEN_HEIGHT//4))

    # Options (play)
    play_font = pygame.font.Font('assets/SegaArcadeFont-Regular.ttf', 40)
    play_button = play_font.render(play_text, True, COLOR_WHITE)
    play_button_rect = play_button.get_rect()
    play_button_rect.center = (SCREEN_WIDTH//4, 420)

    # Options (Exit)
    exit_button = play_font.render(exit_text, True, COLOR_WHITE)
    exit_button_rect = exit_button.get_rect()
    exit_button_rect.center = (SCREEN_WIDTH//4, 480)

    # Change color and adds a > when mouse is above a button
    if play_button_rect.collidepoint(MENU_MOUSE_POS):
        play_button = play_font.render(play_text, True, COLOR_PINK)
        if play_text.find('- ') != -1:
            play_text = play_text
        else:
            play_text = '- ' + play_text
    else:
        play_button = play_font.render(play_text, True, COLOR_WHITE)
        play_text = play_text.replace('- ', '')
    if exit_button_rect.collidepoint(MENU_MOUSE_POS):
        exit_button = play_font.render(exit_text, True, COLOR_PINK)
        if exit_text.find('- ') != -1:
            exit_text = exit_text
        else:
            exit_text = '- ' + exit_text
    else:
        exit_button = play_font.render(exit_text, True, COLOR_WHITE)
        exit_text = exit_text.replace('- ', '')

    # Menu Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main_menu = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main_menu = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button_rect.collidepoint(MENU_MOUSE_POS):
                how_to_play()
            if exit_button_rect.collidepoint(MENU_MOUSE_POS):
                main_menu = False

    # Draw items on screen
    screen.blit(game_name, game_name_rect)
    screen.blit(play_button, play_button_rect)
    screen.blit(exit_button, exit_button_rect)

    # Update screen
    pygame.display.flip()
    game_clock.tick(60)

pygame.quit()
sys.exit()
