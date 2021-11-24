import pygame, os, sys, random, time
from CONST import *
from player import Player
from enemy import Enemy
from projectile import Projectile
from boss import Boss
from tank import Tank
import button

class Game():
    def __init__(self):
        self.run = False
        self.width = SCREEN_SIZE[0]
        self.height = SCREEN_SIZE[1]
        pygame.init()
        pygame.font.init()
        self.mad = 6
        self.score = 0
        self.wave = 0
        self.spawn_start = 1
        self.n = 0
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.draw_screen = pygame.Surface(DRAW_SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.dt = 1
        self.number_of_enemies = 0
        self.font = pygame.font.Font("TF2.ttf", 20)
        self.game()

    def load_textures(self):
        self.textures = {}
        for img in os.listdir("img"):
            texture = pygame.image.load("img/" + img)
            self.textures[img.replace(".png", "")] = texture

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYUP:
                self.click = False
            if event.type == pygame.QUIT:
                self.close()
            if event.type == self.ENEMYMOVE:
                for enemy in self.enemies:
                    enemy.move()
                for boss in self.boss:
                    boss.move()
                for tank in self.tank:
                    tank.move()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click2 = True


    def projectile_move(self):
        for projectile in self.projectiles:
            projectile.move()
            if projectile.x < 0 or projectile.x > DRAW_SCREEN_SIZE[0]:
                self.projectiles.remove(projectile)

    def colision_check(self):
        for projectile in self.projectiles:
            for enemy in self.enemies:
                if projectile.colliderect(enemy) and projectile.type == "1":
                    self.score += 1
                    self.enemies.remove(enemy)
                    try:
                        self.projectiles.remove(projectile)
                    except:
                        print("Projectile error")
            for boss in self.boss:
                if projectile.colliderect(boss) and projectile.type == "1":
                    self.score += 2
                    try:
                        self.boss.remove(boss)
                    except:
                        print("Mage error")
            if projectile.colliderect(self.player) and projectile.type == "2":
                try:
                    self.projectiles.remove(projectile)
                    self.player.hp -= 1
                except:
                    print("Projectile error")
            for tank in self.tank:
                if projectile.colliderect(tank) and projectile.type == "1":
                    self.boss_hp -= 1
                    try:
                        self.projectiles.remove(projectile)
                    except:
                        print("Projectile error")
                    if self.boss_hp <= 0:
                        self.boss_hp = 6
                        self.tank.remove(tank)


        for enemy in self.enemies:
            if enemy and enemy.colliderect(self.player) or enemy.x == 0:
                self.player.hp -= 1
                self.enemies.remove(enemy)
        for boss in self.boss:
            if boss and boss.colliderect(self.player) or boss.x == 0:
                self.player.hp -= 1
                try:
                    self.boss.remove(boss)
                except:
                    print("mage error")
        for tank in self.tank:
            if tank and tank.colliderect(self.player) or tank.x == 0:
                self.player.hp -= 1
                try:
                    self.tank.remove(tank)
                except:
                    print("Tank error")

    def end(self, text):
        surf = self.font.render(text, True, (255, 255, 255))
        rect = surf.get_rect(center=(int(DRAW_SCREEN_SIZE[0] / 2), int(DRAW_SCREEN_SIZE[0] / 2)))
        self.draw_screen.blit(surf, rect)
        timer = END_TIME
        while timer > 0:
            timer -= self.dt
            self.refresh_screen()
        self.__init__()
        self.menu()

    def close(self):
        pygame.quit()
        sys.exit(0)

    def enemy_spawn(self):
        self.number_of_enemies = len(self.enemies)
        if self.number_of_enemies <= self.mad:
            enemy = Enemy(x=random.randint(310, 320), y=random.randint(5, 150), type=random.randint(1, 3))
            self.enemies.append(enemy)
        if self.score == 100:
            self.mad = 8
        if self.score == 200:
            self.boss_spawn = 2
            self.mad = 10
        if self.score == 300:
            self.mad = 12
        if self.score == 500:
            self.boss_spawn = 3
            self.mad = 15
        if self.score == 1000:
            self.mad = 17
        if self.score == 3000:
            self.boss_spawn = 4
            self.mad = 19

    def check_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.player.y -= int(round(PLAYER_SPEED * self.dt))
            self.boss1()
        if keys[pygame.K_DOWN]:
            self.player.y += int(round(PLAYER_SPEED * self.dt))
        if keys[pygame.K_SPACE] and not self.click:
            if len(self.projectiles) <= 4:
                self.click = True
                projectile = Projectile(self.player.centerx,self.player.centery - 6, "1")
                self.projectiles.append(projectile)
        if keys[pygame.K_ESCAPE]:
            self.pause = True
            self.menu()

    def mage_shoot(self):
        for boss in self.boss:
            if random.randint(1, ENEMY_SHOT_RATIO) == 1:
                projectile = Projectile(boss.centerx, boss.centery - 25, "2")
                self.projectiles.append(projectile)

    def check_p_hp(self):
        if self.player.hp <= 0:
            self.end("GAME OVER! SCORE: " + str(self.score))

    def menu(self):
        while True:
            self.screen.fill((0, 0, 0))
            if self.start_button.draw(self.screen):
                self.run = True
                break
            if self.exit_button.draw(self.screen):
                self.close()
            self.check_events()
            pygame.display.update()

    def game(self):
        self.start_img = pygame.image.load('start_btn.png').convert_alpha()
        self.exit_img = pygame.image.load('exit_btn.png').convert_alpha()
        self.start_button = button.Button(530, 200, self.start_img, 0.8)
        self.exit_button = button.Button(530, 350, self.exit_img, 0.8)
        self.run = False
        self.boss_hp = 6
        self.tank = []
        self.running = True
        self.pause = 0
        self.boss_spawn = 1
        self.tank_spawn = 1
        self.click = False
        self.boss = []
        self.ENEMYMOVE = pygame.USEREVENT
        pygame.time.set_timer(self.ENEMYMOVE, MOVE_RATIO)
        self.player = Player()
        self.projectiles = []
        self.enemies = []
        self.load_textures()
        self.menu()
        while self.run:
            self.boss1()
            self.check_p_hp()
            self.colision_check()
            self.projectile_move()
            self.enemy_spawn()
            self.player.check_player()
            self.check_events()
            self.check_keys()
            self.mage_shoot()
            self.tank_f()
            self.draw()
            self.refresh_screen()

    def show_hp_and_score(self, text, score, spawn_rate, fps):
        self.textsurface = self.font.render(text, True, (0, 0, 0))
        self.draw_screen.blit(self.textsurface, (250, 5))
        self.textsurface = self.font.render(score, True, (0, 0, 0))
        self.draw_screen.blit(self.textsurface, (150, 5))
        self.textsurface = self.font.render(spawn_rate, True, (0, 0, 0))
        self.draw_screen.blit(self.textsurface, (60, 5))
        self.textsurface = self.font.render(fps, True, (0, 0, 0))
        self.draw_screen.blit(self.textsurface, (0, 5))

    def boss1(self):
        if len(self.boss) != self.boss_spawn:
            boss_info = Boss(x=random.randint(310, 320), y=random.randint(5, 150), hp=10)
            self.boss.append(boss_info)

    def tank_f(self):
        if len(self.tank) != self.tank_spawn:
            tank_i = Tank(x=random.randint(310, 320), y=random.randint(5, 150))
            self.tank.append(tank_i)

    def refresh_screen(self):
        scaled = pygame.transform.scale(self.draw_screen, SCREEN_SIZE)
        self.screen.blit(scaled, (0, 0))
        pygame.display.update()
        self.dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000

    def draw(self):
        self.draw_screen.blit(self.textures["background"], (0, 0))
        self.draw_screen.blit(self.textures["player"], self.player)
        for tank_i in self.tank:
            self.draw_screen.blit(self.textures["tank"], tank_i)
        for boss_info in self.boss:
            self.draw_screen.blit(self.textures["boss"], boss_info)
        for enemy in self.enemies:
            self.draw_screen.blit(self.textures["enemy" + enemy.type], enemy)
        for projectile in self.projectiles:
            self.draw_screen.blit(self.textures["projectile" + projectile.type], projectile)
        self.show_hp_and_score("HP: " + str(self.player.hp), "SCORE: " + str(self.score), "Spawn: " + str(self.mad), "FPS:" + str(round(self.clock.get_fps())))
Game()