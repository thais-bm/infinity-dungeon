import random
import pygame
import sys
import phase_2, phase_3, phase_5, phase_6




def iniciar():
    # Matriz
    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    # Pygame Setup
    pygame.init()
    SCREEN_WIDTH = 624
    SCREEN_HEIGHT = 724
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Infinite Dungeon")

    # Colors
    COLOR_WHITE = (255, 255, 255)
    COLOR_BLACK = (0, 0, 0)
    TILE_SIZE = 48

    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, direction):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("assets/magic.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = 20
            self.direction = direction

        def update(self):
            if self.direction == 'Up':
                self.image = pygame.image.load('assets/bullet.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.image = pygame.transform.rotate(self.image, 180)
                self.rect.y -= self.speed
                self.rect.x -= 1
            elif self.direction == 'Down':
                self.image = pygame.image.load('assets/bullet.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.image = pygame.transform.rotate(self.image, 0)
                self.rect.y += self.speed
                self.rect.x -= 1
            elif self.direction == 'Left':
                self.image = pygame.image.load('assets/bullet.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.image = pygame.transform.rotate(self.image, -90)
                self.rect.x -= self.speed
                self.rect.x -= 1
            elif self.direction == 'Right':
                self.image = pygame.image.load('assets/bullet.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (50, 50))
                self.image = pygame.transform.rotate(self.image, 90)
                self.rect.x += self.speed
                self.rect.x -= 1
            if self.rect.bottom <= 0 or self.rect.top >= 624 or self.rect.right <= 0 or self.rect.left >= 624:
                self.kill()

            for lane in range(len(maze)):
                for col in range(len(maze[lane])):
                    if maze[lane][col] == 1:
                        wall_rect = pygame.Rect(col * TILE_SIZE, lane * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if self.rect.colliderect(wall_rect):
                            self.kill()

    class Monster(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y):
            pygame.sprite.Sprite.__init__(self)
            self.position = [pos_x, pos_y]
            self.image = pygame.image.load('assets/final_boss.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (100, 100))
            self.rect = self.image.get_rect(
                center=(
                    (self.position[0] * TILE_SIZE) + (TILE_SIZE // 2),
                    (self.position[1] * TILE_SIZE) + (TILE_SIZE // 2)
                )
            )
            self.health = 30

        def take_damage(self):
            self.health -= 1
            if self.health <= 0:
                self.kill()

        def update(self, player_pos):
            # Monster actual position in the 'Maze'
            row = int(self.rect.y // TILE_SIZE)
            column = int(self.rect.x // TILE_SIZE)

            # Obtém a posição de outros monstros e adiciona a uma lista
            busy_position = set()
            for monster in all_monsters:
                if monster != self:
                    other_row = int(monster.rect.y // TILE_SIZE)
                    other_column = int(monster.rect.x // TILE_SIZE)
                    busy_position.add((other_column, other_row))



    # Under construction
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.life = 3
            self.position = [10, 6]
            self.invulnerable = False
            self.invulnerable_timer = 0
            self.direction = 'Up'  # Up, Down, Left, Right
            self.image = pygame.image.load(f'assets/player_walking/tile00{0}.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.x = self.position[1] * TILE_SIZE
            self.rect.y = self.position[0] * TILE_SIZE
            self.last_shot_time = pygame.time.get_ticks()
            self.shoot_delay = 700

        def move(self, keys):
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                if can_move(self.position[0], self.position[1] - 1):
                    self.position[1] -= 1
                    self.direction = 'Left'
                    self.image = pygame.image.load(f'assets/player_walking/tile003.png').convert_alpha()
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                if can_move(self.position[0], self.position[1] + 1):
                    self.position[1] += 1
                    self.direction = 'Right'
                    self.image = pygame.image.load(f'assets/player_walking/tile006.png').convert_alpha()
            elif keys[pygame.K_UP] or keys[pygame.K_w]:
                if can_move(self.position[0] - 1, self.position[1]):
                    self.position[0] -= 1
                    self.direction = 'Up'
                    self.image = pygame.image.load(f'assets/player_walking/tile009.png').convert_alpha()
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                if can_move(self.position[0] + 1, self.position[1]):
                    self.position[0] += 1
                    self.direction = 'Down'
                    self.image = pygame.image.load(f'assets/player_walking/tile000.png').convert_alpha()

        def shoot(self):
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= self.shoot_delay:
                bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
                all_bullets.add(bullet)
                self.last_shot_time = current_time
                print('piu piu')

        def take_damage(self):
            if not self.invulnerable:
                self.life -= 1
                self.invulnerable = True
                self.image = pygame.image.load(f'assets/monster_1/tile000.png').convert_alpha() # So pra piscar
                print('Invencivel')
                self.invulnerable_timer = pygame.time.get_ticks()
                if self.life <= 0:
                    print('game ouver hihi')


        def draw(self, screen):
            screen.blit(self.image, self.rect)


        def update(self):
            if self.invulnerable:
                if pygame.time.get_ticks() - self.invulnerable_timer > 5000:  # 2s of invunerable
                    self.invulnerable = False
                    self.image = pygame.image.load(f'assets/player_walking/tile000.png').convert_alpha()
                    print('Nao ta invencivel')
            self.rect.x = self.position[1] * TILE_SIZE
            self.rect.y = self.position[0] * TILE_SIZE

    # Player
    player = Player()

    # bullet
    all_bullets = pygame.sprite.Group()
    all_monsters = pygame.sprite.Group()

    # Fiz hardcoded até saber o que fazer
    monster = Monster(6, 4)
    all_monsters.add(monster)


    # Menu loop
    game_loop = True

    # Map
    bg = pygame.image.load('assets/assets_wall/Map013.png').convert()

    def show_stats():
        stats_bg = pygame.Surface((624, 100))
        stats_bg.fill(COLOR_BLACK)
        font = pygame.font.Font('assets/SegaArcadeFont-Regular.ttf', 30)
        life = font.render(f'VIDA: {player.life}', True, COLOR_WHITE)
        life_rect = life.get_rect(bottomleft=(100, 700))
        screen.blit(stats_bg, (0, 624))
        screen.blit(life, life_rect)


    def can_move(x, y):
        return maze[x][y] == 0


    while game_loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_loop = False

        # Player Movement
        keys = pygame.key.get_pressed()
        player.move(keys)
        if keys[pygame.K_z]:
            player.shoot()


        # Load Map + player + bullet + monster
        screen.blit(bg, (0, 0))
        player.update()
        player.draw(screen)
        all_bullets.draw(screen)
        all_monsters.draw(screen)
        all_bullets.update()
        all_monsters.update(player.position)

        # Bullet-Monsters Collision
        for bullet in all_bullets:
            hit_monsters = pygame.sprite.spritecollide(bullet, all_monsters, False)
            if hit_monsters:
                bullet.kill()  # Remove o tiro
                for monster in hit_monsters:
                    monster.take_damage()

        # Bullet-Monsters Collision
        for bullet in all_bullets:
            hit_monsters = pygame.sprite.spritecollide(bullet, all_monsters, True)
            if hit_monsters:
                bullet.kill()
        # Monster-Player collision
        for monster in all_monsters:
            if player.rect.colliderect(monster.rect):
                # Ideal -> invunerabilidade
                player.take_damage()

        show_stats()

        if player.life <= 0:
            print("Game ouver")
            game_loop = False

        # Debub Monster part
        print('Debug mode')
        for index, monster in enumerate(all_monsters):
            print(f'{index} ---> X: {monster.rect.x // TILE_SIZE} and Y: {monster.rect.y // TILE_SIZE}')

        pygame.display.update()
        pygame.display.flip()

        pygame.time.Clock().tick(10)

    pygame.quit()
    sys.exit()

iniciar()