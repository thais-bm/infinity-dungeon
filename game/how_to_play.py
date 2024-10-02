import sys

import pygame
import phase_1

pygame.init()
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tower Of God")

bg_img = pygame.image.load('assets/ins_basic.png')

def begin():
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



