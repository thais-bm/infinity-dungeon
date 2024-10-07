import random
import pygame
import sys
import math
import phase_2, phase_3, phase_5, phase_6

pygame.mixer.init()
move_fx = pygame.mixer.Sound("assets/audio/Move1.ogg")
evasion = pygame.mixer.Sound("assets/audio/Evasion.ogg")
attack = pygame.mixer.Sound("assets/audio/Attack.ogg")
hit = pygame.mixer.Sound("assets/audio/Slash.ogg")


def iniciar(life):
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
    COLOR_ZERO = (255, 255, 255, 255)
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

    class BossProjectile(pygame.sprite.Sprite):
        def __init__(self, x, y, direction, angle=0):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load("assets/magic.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (20, 20))
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = 5
            self.direction = direction
            self.angle = math.radians(angle)  # Convertemos o ângulo para radianos
            self.hit = 0

        def update(self):
            if self.direction == 'Down':
                self.rect.x += math.sin(self.angle) * self.speed
                self.rect.y += math.cos(self.angle) * self.speed
            elif self.direction == 'Left':
                self.rect.x -= self.speed
            elif self.direction == 'Right':
                self.rect.x += self.speed
            elif self.direction == 'Up':
                self.rect.x += -(math.sin(self.angle)) * self.speed
                self.rect.y += -(math.cos(self.angle)) * self.speed

            # Remove o projétil se sair da tela
            if (self.rect.bottom <= 0 or self.rect.top >= 624 or
                    self.rect.right <= 0 or self.rect.left >= 624):
                self.kill()

            # Colisão com paredes
            for lane in range(len(maze)):
                for col in range(len(maze[lane])):
                    if maze[lane][col] == 1:
                        wall_rect = pygame.Rect(col * TILE_SIZE, lane * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                        if self.rect.colliderect(wall_rect):
                            self.hit += 1
                            if self.hit >= 2:
                                self.kill()
                                return

                            if self.direction == 'Down':
                                self.direction = 'Up'
                            elif self.direction == 'Left':
                                self.direction = 'Right'
                            elif self.direction == 'Right':
                                self.direction = 'Left'

    all_boss_projectiles = pygame.sprite.Group()

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
            self.health = 50
            self.max_health = 50
            self.current_moveset = None
            self.moveset_timer = 0
            self.moveset_delay = 3000  # 3 segundos entre movesets
            self.projectile_timer = 0
            self.projectile_delay = 750

        def take_damage(self):
            self.health -= 1
            if self.health <= 0:
                self.kill()

        def update(self, player_pos):
            current_time = pygame.time.get_ticks()

            # Alterna movesets
            if current_time - self.moveset_timer > self.moveset_delay:
                self.current_moveset = random.choice(['triple_shot', 'spread_shot', 'circle_shot'])
                self.moveset_timer = current_time

            # Executa o moveset atual
            if current_time - self.projectile_timer > self.projectile_delay:
                if self.current_moveset == 'triple_shot':
                    self.triple_shot()
                elif self.current_moveset == 'spread_shot':
                    self.spread_shot()
                elif self.current_moveset == 'circle_shot':
                    self.circle_shot()
                self.projectile_timer = current_time

        def triple_shot(self):
            directions = ['Left', 'Down', 'Right']
            for direction in directions:
                projectile = BossProjectile(self.rect.centerx, self.rect.centery, direction)
                all_boss_projectiles.add(projectile)

        def spread_shot(self):
            angles = [-45, -30, -15, 0, 15, 30, 45]
            for angle in angles:
                projectile = BossProjectile(self.rect.centerx, self.rect.centery, 'Down', angle)
                all_boss_projectiles.add(projectile)

        def circle_shot(self):
            for angle in range(0, 360, 45):
                projectile = BossProjectile(self.rect.centerx, self.rect.centery, 'Down', angle)
                all_boss_projectiles.add(projectile)

    class HealthBar:
        def __init__(self, x, y, width, height, hp, max_hp):
            self.x = x
            self.y = y
            self.width = width
            self.height = height
            self.hp = hp
            self.max_hp = max_hp
            self.frame = pygame.image.load('assets/health_bar.png').convert_alpha()

        def draw(self, surface):
            hp_ratio = self.hp / self.max_hp
            pygame.draw.rect(surface, "red", (self.x+28, self.y+10, self.width, self.height))
            pygame.draw.rect(surface, "green", (self.x+28, self.y+10, self.width * hp_ratio, self.height))
            screen.blit(self.frame, (self.x, self.y))

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.life = life
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
                pygame.mixer.Sound.play(attack)
                self.last_shot_time = current_time
                print('piu piu')

        def take_damage(self):
            if not self.invulnerable:
                self.life -= 1
                self.invulnerable = True
                self.image = pygame.image.load(f'assets/player_damaged/tile001.png').convert_alpha() # just blink
                print('Invencivel')
                pygame.mixer.Sound.play(evasion)
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

    boss_projectile_hits = pygame.sprite.spritecollide(player, all_boss_projectiles, True)
    if boss_projectile_hits:
        player.take_damage()


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

        if player.invulnerable:
            vunerable = 'Sim'
        else:
            vunerable = 'Nao'

        life = font.render(f'VIDA: {player.life}', True, COLOR_WHITE)
        power = font.render(f'Invencivel: {vunerable}',True, COLOR_WHITE)

        life_rect = life.get_rect(topleft=(100, 630))
        power_rect = power.get_rect(topleft=(100, 660))
        screen.blit(stats_bg, (0, 624))
        screen.blit(life, life_rect)
        screen.blit(power, power_rect)


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
        health_bar = HealthBar(72, 55, 440, 10, monster.health, monster.max_health)
        player.update()
        all_bullets.update()
        all_monsters.update(player.position)
        all_boss_projectiles.update()

       # Draw elements
        player.draw(screen)
        all_bullets.draw(screen)
        all_monsters.draw(screen)
        all_boss_projectiles.draw(screen)
        health_bar.draw(screen)

        # Collisions
        for bullet in all_bullets:
            hit_monsters = pygame.sprite.spritecollide(bullet, all_monsters, False)
            if hit_monsters:
                bullet.kill()
                for monster in hit_monsters:
                    pygame.mixer.Sound.play(hit)
                    monster.take_damage()

        # Colisão entre projéteis do chefe e jogador
        boss_projectile_hits = pygame.sprite.spritecollide(player, all_boss_projectiles, True)
        if boss_projectile_hits:
            player.take_damage()

        # Monster-Player collision
        for monster in all_monsters:
            if player.rect.colliderect(monster.rect):
                player.take_damage()

        show_stats()

        if monster.health <= 0:
            pygame.mixer.stop()
            bg_img = pygame.image.load('assets/the_end.png')
            the_end = pygame.mixer.Sound("assets/audio/Victory.ogg")
            pygame.mixer.Sound.play(the_end)
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
            sys.exit()

        if player.life <= 0:
            pygame.mixer.Sound.stop()
            bg_img = pygame.image.load('assets/game_over.png')
            gameover = pygame.mixer.Sound("assets/audio/Gameover.ogg")
            pygame.mixer.Sound.play(gameover)
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
            sys.exit()

        pygame.display.update()
        pygame.time.Clock().tick(10)

#iniciar(20)
