import pygame, os, sys, random, time
from CONST import *
from player import Player
from enemy import Enemy
from projectile import Projectile
from boss import Boss
from tank import Tank
import button
import threading
from heart import Heart
from blow import Blow

class Game():
    def __init__(self):
        self.read_data_file()
        self.mage_shoot_ready = True
        self.z = False
        self.heart_spawn_z = True
        self.coin_c = 0
        self.run = False
        self.shot = True
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
        self.draw_screen2 = pygame.Surface(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.dt = 1
        self.number_of_enemies = 0
        self.font = pygame.font.Font("TF2.ttf", 20)
        self.read_data_file()
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

    def trigger(self):
        time.sleep(0.11)
        self.shot = True

    def colision_check(self):
        for projectile in self.projectiles:
            for heart in self.hearts:
                if projectile.colliderect(heart) and not projectile.type == "2":
                    self.player.hp += 1
                    self.hearts.remove(heart)
                    try:
                        self.projectiles.remove(projectile)
                    except:
                        print("Projectile error")
            for enemy in self.enemies:
                if projectile.colliderect(enemy) and projectile.type == "1":
                    self.score += 1
                    self.enemies.remove(enemy)
                    self.draw_screen.blit(self.textures["blow"], projectile)
                    self.refresh_screen()
                    try:
                        self.projectiles.remove(projectile)
                    except:
                        print("Projectile error")
                if projectile.colliderect(enemy) and projectile.type == "3":
                    self.score += 1
                    self.enemies.remove(enemy)
            for boss in self.boss:
                if projectile.colliderect(boss) and projectile.type == "3":
                    self.score += 2
                    try:
                        self.boss.remove(boss)
                    except:
                        print("Mage error")
                    self.draw_screen.blit(self.textures["blow"], projectile)
                    self.refresh_screen()
                if projectile.colliderect(boss) and projectile.type == "1":
                    self.score += 2
                    self.draw_screen.blit(self.textures["blow"], projectile)
                    self.refresh_screen()
                    try:
                        self.boss.remove(boss)
                    except:
                        print("Mage error")
            if projectile.colliderect(self.player) and projectile.type == "2":
                self.armors -= 1
                if self.armors <= 0:
                    self.player.hp -= 1
                self.draw_screen.blit(self.textures["blow"], projectile)
                self.refresh_screen()
                try:
                    self.projectiles.remove(projectile)
                except:
                    print("Projectile error")
            for tank in self.tank:
                if projectile.colliderect(tank) and projectile.type == "3":
                    self.thread = threading.Thread(target=self.trigger)
                    self.thread.daemon = True
                    self.thread.start()
                    if self.shot == True:
                        self.boss_hp -= 2
                        self.shot = False
                    if self.boss_hp <= 0:
                        self.boss_hp = 6
                        self.tank.remove(tank)

                if projectile.colliderect(tank) and projectile.type == "1":
                    self.boss_hp -= 1
                    self.draw_screen.blit(self.textures["blow"], projectile)
                    self.refresh_screen()
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
        if self.armors < 0:
            self.armors = 0
        self.save_to_data_file(self.data[0], self.data[1], self.data[2], self.data[3], self.armors)
        if int(self.data[0]) < self.score:
            self.save_to_data_file(self.score, self.data[1], self.data[2], self.data[3], self.armors)
        self.read_data_file()
        self.add_coins()
        self.__init__()
        self.menu()

    def close(self):
        pygame.quit()
        sys.exit(0)

    def cooldown(self):
        time.sleep(15)
        self.heart_spawn_z = True

    def enemy_spawn(self):
        if self.heart_spawn_z == False and self.z == True:
            self.thread = threading.Thread(target=self.cooldown)
            self.thread.daemon = True
            self.thread.start()
            self.z = False
        if len(self.hearts) == 0 and self.score >= 350:
            self.heart_s_rate = random.randint(1, 3000)
            if self.heart_s_rate == 69 and self.heart_spawn_z == True:
                heart = Heart(x=random.randint(50, 320), y=random.randint(5, 150))
                self.hearts.append(heart)
                self.heart_spawn_z = False
                self.z = True
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
        if keys[pygame.K_r]:
            x, y = pygame.mouse.get_pos()
            print(x, y)
            self.draw_screen.blit(self.textures["blow"], (x, y))
            self.refresh_screen()
        if keys[pygame.K_UP]:
            self.player.y -= int(round(PLAYER_SPEED * self.dt))
            self.boss1()
        if keys[pygame.K_DOWN]:
            self.player.y += int(round(PLAYER_SPEED * self.dt))
        if keys[pygame.K_SPACE] and not self.click:
            if len(self.projectiles) <= 3 and self.ak_chosen == True:
                self.click = True
                projectile = Projectile(self.player.centerx,self.player.centery - 6, "1")
                self.projectiles.append(projectile)
            if len(self.projectiles) <= 1 and self.rpg_chosen == True:
                self.click = True
                projectile = Projectile(self.player.centerx,self.player.centery - 6, "3")
                self.projectiles.append(projectile)
        if len(self.projectiles) <= 8 and self.aak_chosen == True and self.shot == True and keys[pygame.K_SPACE]:
            self.shot = False
            projectile = Projectile(self.player.centerx, self.player.centery - 6, "1")
            self.projectiles.append(projectile)
            self.thread = threading.Thread(target=self.trigger)
            self.thread.daemon = True
            self.thread.start()
        if keys[pygame.K_ESCAPE]:
            self.end("NOOB")
            self.menu()

    def mage_shoot_ready_check(self):
        time.sleep(0.4)
        self.mage_shoot_ready = True

    def mage_shoot(self):
        for boss in self.boss:
            if self.mage_shoot_ready == False and self.b == True:
                self.thread = threading.Thread(target=self.mage_shoot_ready_check)
                self.thread.daemon = True
                self.thread.start()
                self.b = False
            if random.randint(1, ENEMY_SHOT_RATIO) == 1 and self.mage_shoot_ready == True:
                projectile = Projectile(boss.centerx, boss.centery - 25, "2")
                self.projectiles.append(projectile)
                self.mage_shoot_ready = False
                self.b = True

    def check_p_hp(self):
        if self.player.hp <= 0:
            self.end("GAME OVER! SCORE: " + str(self.score))

    def menu(self):
        self.ak_chosen = False
        self.rpg_chosen = False
        self.aak_chosen = False
        while True:
            self.draw_screen2.blit(self.textures["menu_bckg"], (0, 0))
            self.kurwa = self.font.render("Highest Score: " + str(self.data[0]) + " Coins: " + str(self.data[1] + " KEVLARS: ") + str(self.data[4]) , True, (0, 0, 0))
            self.draw_screen2.blit(self.kurwa, (600, 100))
            if self.pause  == True:
                self.run = False
            if self.start_button.draw(self.draw_screen2):
                self.run = True
                break
            if self.exit_button.draw(self.draw_screen2):
                self.close()
            if self.shop_button.draw(self.draw_screen2):
                self.shop()
            if self.choose_btn.draw(self.draw_screen2):
                self.ak_chosen = True
                self.rpg_chosen = False
                self.aak_chosen = False
            if self.choose_btn2.draw(self.draw_screen2) and self.data[3] == "1":
                self.rpg_chosen = True
                self.aak_chosen = False
                self.ak_chosen = False
            if self.choose_btn3.draw(self.draw_screen2) and self.data[2] == "1":
                self.aak_chosen = True
                self.ak_chosen = False
                self.rpg_chosen = False
            if self.ak_chosen == True:
                self.draw_screen2.blit(self.textures["choosed_btn"], (72, 25))
            if self.rpg_chosen == True:
                self.draw_screen2.blit(self.textures["choosed_btn"], (193, 67))
            if self.aak_chosen == True:
                self.draw_screen2.blit(self.textures["choosed_btn"], (185, 110))
            self.check_events()
            self.refresh_screen2()

    def buy_aak(self):
        self.coin_c = float(self.data[1])
        if float(self.coin_c) >= 500 and not self.data[2] == "1":
            self.coin_c -= 500
            print(self.coin_c)
            self.save_to_data_file(self.data[0], self.coin_c, "1", self.data[3], self.data[4])
            self.__init__()
    def buy_par(self):
        self.coin_c = float(self.data[1])
        if self.coin_c >= 300 and not self.data[3] == "1":
            self.coin_c -= 300
            print(self.coin_c)
            self.save_to_data_file(self.data[0], self.coin_c, self.data[2], "1", self.data[4])
            self.__init__()

    def shop(self):
        while True:
            self.draw_screen2.blit(self.textures["shop_bckg"], (0, 0))
            if self.exit_button2.draw(self.draw_screen2):
                break
            if self.buy_button.draw(self.draw_screen2):
                self.buy_par()
            if self.buy_button2.draw(self.draw_screen2):
                self.buy_aak()
            if self.buy_button3.draw(self.draw_screen2):
                self.buy_armor()
            self.check_events()
            self.refresh_screen2()
        self.menu()

    def buy_armor(self):
        self.coins = float(self.data[1])
        self.armors = int(self.data[4])
        print(self.coins, self.armors)
        if self.coins >= 100 and self.armors <= 2:
            self.armors += 1
            self.coins -= 100
            self.save_to_data_file(self.data[0], self.coins, self.data[2], self.data[3], self.armors)
            self.__init__()

    def save_to_data_file(self, a, b, c, d, e):
        self.f = open("data.txt", 'w')
        self.f.write(str(a) + "\n" + str(b) + "\n" + str(c) + "\n" + str(d) + "\n" + str(e) + "\n")
        self.f.close()

    def read_data_file(self):
        self.data = []
        self.f = open("data.txt", "r")
        for self.a in self.f:
            self.data.append(self.a.strip())
        print(self.data)

    def add_coins(self):
        self.coins = float(self.score / 10)
        self.coins = self.coins + float(self.data[1])
        round(self.coins)
        self.save_to_data_file(self.data[0], self.coins, self.data[2], self.data[3], self.data[4])

    def game(self):
        self.armors = int(self.data[4])
        self.choose_img = pygame.image.load('choose_btn.png').convert_alpha()
        self.start_img = pygame.image.load('start_btn.png').convert_alpha()
        self.exit_img = pygame.image.load('exit_btn.png').convert_alpha()
        self.shop_img = pygame.image.load('shop_btn.png').convert_alpha()
        self.buy_img = pygame.image.load('buy_btn.png').convert_alpha()
        self.choose_btn = button.Button(72, 25, self.choose_img, 0.8)
        self.choose_btn2 = button.Button(193, 67, self.choose_img, 0.8)
        self.choose_btn3 = button.Button(185, 110, self.choose_img, 0.8)
        self.buy_button = button.Button(900, 180, self.buy_img, 0.8)
        self.buy_button2 = button.Button(900,500, self.buy_img, 0.8)
        self.buy_button3 = button.Button(900, 600, self.buy_img, 0.8)
        self.start_button = button.Button(530, 200, self.start_img, 0.8)
        self.exit_button = button.Button(530, 450, self.exit_img, 0.8)
        self.exit_button2 = button.Button(1050, 0, self.exit_img, 0.8)
        self.shop_button = button.Button(530, 350, self.shop_img, 0.8)
        self.run = False
        self.boss_hp = 6
        self.tank = []
        self.hearts = []
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

    def refresh_screen2(self):
        scaled2 = pygame.transform.scale(self.draw_screen2, SCREEN_SIZE)
        self.screen.blit(scaled2, (0, 0))
        pygame.display.update()
        #self.dt = self.clock.tick(FRAMERATE) * FRAMERATE / 1000

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
        for heart in self.hearts:
            self.draw_screen.blit(self.textures["heart"], heart)
            #str(round(self.clock.get_fps()
        self.show_hp_and_score("HP: " + str(self.player.hp), "SCORE: " + str(self.score), "Spawn: " + str(self.mad), "KEV: " + str(self.armors))
Game()
