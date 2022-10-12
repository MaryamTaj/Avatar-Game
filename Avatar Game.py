# Name: Jackson Montgomery, Kevin Hearn, Maryam Taj, and Miqdad Valji
# Program Name: The Savior
# Program Description: After the earth, water and fire tribes attack \
# Aaang's village and take his community hostage, he must use his \
# air-bending skills to get past the tribes, and free his people.
# Date of Last Revision:

# Import Statements
import pygame
from pygame import mixer
import os

# Initialize Pygame
pygame.init()

# Window
window = pygame.display.set_mode((600, 600))
pygame.display.set_caption('The Savior')
pygame.display.set_icon(pygame.image.load(os.path.join('Background', 'Avatar.jpg')))

# Backgrounds
Lvl1 = pygame.image.load(os.path.join('Background', 'Level1_background.png'))
Lvl1 = pygame.transform.scale(Lvl1, (600, 600))
Lvl2 = pygame.image.load(os.path.join('Background', 'Level2_background.png'))
Lvl2 = pygame.transform.scale(Lvl2, (600, 600))
Lvl3 = pygame.image.load(os.path.join('Background', 'Level3_background.png'))
Lvl3 = pygame.transform.scale(Lvl3, (600, 600))
background_list = [Lvl1, Lvl2, Lvl3]
level = 0

# Music
w_sound = mixer.Sound('p_wins.mp3')
h_sound = mixer.Sound('p_hit.mp3')
l_sound = mixer.Sound('p_loses.mp3')


# Player Class
class Player(pygame.sprite.Sprite):
    # Player's Basic Characteristics
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('Avatar', 'Avatar.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 15
        self.f_up = True
        self.f_down = False
        self.f_right = False
        self.f_left = False
        self.winds = []
        self.cool_down_count = 0
        self.health = 60
        self.health_counter = 3
        self.zuko = 0
        self.iroh = 0
        self.azula = 0

    # Player's Movement
    def move(self, user):
        if user[pygame.K_UP] and self.rect.y >= 40:
            self.rect.y -= self.velocity
            self.f_up = True
            self.f_down = False
            self.f_right = False
            self.f_left = False
        elif user[pygame.K_DOWN] and self.rect.y <= 500:
            self.rect.y += self.velocity
            self.f_up = False
            self.f_down = True
            self.f_right = False
            self.f_left = False
        elif user[pygame.K_RIGHT] and self.rect.x <= 500:
            self.rect.x += self.velocity
            self.f_up = False
            self.f_down = False
            self.f_right = True
            self.f_left = False
        elif user[pygame.K_LEFT] and self.rect.x >= 5:
            self.rect.x -= self.velocity
            self.f_up = False
            self.f_down = False
            self.f_right = False
            self.f_left = True

    # Player's Shooting
    def shoot(self):
        self.cooldown()
        if user[pygame.K_SPACE] and self.cool_down_count == 0 and self.health > 0:
            wind = Wind(self.rect.x, self.rect.y)
            self.winds.append(wind)
            self.cool_down_count = 1
        for wind in self.winds:
            wind.move()
            if wind.off_screen():
                self.winds.remove(wind)

    # Player's Cooldown
    def cooldown(self):
        if self.cool_down_count > 0:
            self.cool_down_count += 1
        if self.cool_down_count >= 10 - self.zuko:
            self.cool_down_count = 0

    # Player's Drawn Image
    def draw(self, window):
        self.hitbox = (self.rect.x, self.rect.y, 90, 90)
        pygame.draw.rect(window, (0, 0, 0), self.hitbox, 1)
        if self.health > 0:
            window.blit(self.image, (self.rect.x, self.rect.y))


# Enemy Class
class Enemy(pygame.sprite.Sprite):
    # Enemy's Basic Characteristics
    def __init__(self, x, y, width, height, end):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('Earth', 'EarthLord.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.path = [x, end]
        self.velocity = 4
        self.health = 60
        self.attacks = []
        self.cool_down_count = 0
        self.zuko = 0
        self.iroh = 0

    # Enemy's Movement
    def move(self):
        if self.velocity > 0:
            if self.rect.x < self.path[1]:
                self.rect.x += self.velocity
            else:
                self.velocity = self.velocity * -1
                self.rect.x += self.velocity
        else:
            if self.rect.x > self.path[0]:
                self.rect.x += self.velocity
            else:
                self.velocity = self.velocity * -1

    # Enemy's Shooting
    def shoot(self):
        self.cooldown()
        if self.cool_down_count == 0 and self.health > 0:
            earth = Earth(self.rect.x, self.rect.y)
            self.attacks.append(earth)
            self.cool_down_count = 1
        for earth in self.attacks:
            earth.move()
            if earth.off_screen():
                self.attacks.remove(earth)

    # Enemy's Cooldown
    def cooldown(self):
        if self.cool_down_count > 0:
            self.cool_down_count += 1
        if self.cool_down_count >= 50 - self.zuko:
            self.cool_down_count = 0

    # Enemy's Drawn Image
    def draw(self, window):
        self.move()
        self.hitbox = (self.rect.x, self.rect.y, 90, 90)
        pygame.draw.rect(window, (0, 0, 0), self.hitbox, 1)
        if self.health > 0:
            pygame.draw.rect(window, (255, 0, 0), (self.rect.x + 15, self.rect.y - 20, 60, 10))
            pygame.draw.rect(window, (0, 255, 0), (self.rect.x + 15, self.rect.y - 20, self.health, 10))
            window.blit(self.image, (self.rect.x, self.rect.y))
        if self.health == 0:
            pygame.draw.rect(window, (255, 0, 0), (self.rect.x + 15, self.rect.y - 20, 0, 0))


# Wind Class
class Wind(pygame.sprite.Sprite):
    def __init__(self, x, y):
        # Wind's Basic Characteristics
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('Wind', 'wind_up.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # Wind's Movement
    def move(self):
        self.rect.y -= 15

    # Wind's Screen Presence
    def off_screen(self):
        return not (-60 <= self.rect.x <= 600 and -30 <= self.rect.y <= 600)

    # Wind's Drawn Image
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Earth Class
class Earth(pygame.sprite.Sprite):
    # Earth's Basic Characteristics
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('Earth', 'earth_up.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # Earth's Movement
    def move(self):
        self.rect.y += 15

    # Earth's Screen Presence
    def off_screen(self):
        return not (-60 <= self.rect.x <= 600 and -30 <= self.rect.y <= 600)

    # Earth's Drawn Image
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y + 40))


# Scroll Class
class Scroll(pygame.sprite.Sprite):
    # Scroll's Basic Characteristics
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('Upgrades', 'scroll.png'))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.alive = True

    # Scroll's Drawn Image
    def draw(self, window):
        if self.alive:
            window.blit(self.image, (self.rect.x, self.rect.y))


# Wall Class
class Wall(pygame.sprite.Sprite):
    # Wall's Basic Characteristics
    def __init__(self, x, y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


# Draw Game
def draw_game():
    window.fill((0, 0, 0))
    window.blit(background_list[level], (0, 0))
    player.draw(window)
    enemy1.draw(window)
    enemy2.draw(window)
    for wind in player.winds:
        wind.draw()
    for attacks in enemy1.attacks:
        attacks.draw()
    for attacks in enemy2.attacks:
        attacks.draw()
    if level == 0:
        scroll1.draw(window)
        scroll2.draw(window)
    if level == 1:
        scroll3.draw(window)
        scroll4.draw(window)
        scroll5.draw(window)
    if level == 2:
        scroll6.draw(window)
        scroll7.draw(window)
        scroll8.draw(window)
        scroll9.draw(window)

    font = pygame.font.SysFont('Consolas', 32)
    text = font.render('Lives:' + str(player.health_counter), True, (0, 0, 0))

    if level == 1:
        window.blit(text, (415, 520))
    else:
        window.blit(text, (460, 560))
    pygame.time.delay(50)
    pygame.display.update()


# Object's Positions
player = Player(250, 445)
enemy1 = Enemy(50, 40, 90, 90, 150)
enemy2 = Enemy(300, 40, 90, 90, 400)
scroll1 = Scroll(80, 200)
scroll2 = Scroll(515, 350)
scroll3 = Scroll(150, 450)
scroll4 = Scroll(515, 430)
scroll5 = Scroll(420, 200)
scroll6 = Scroll(453, 160)
scroll7 = Scroll(455, 543)
scroll8 = Scroll(70, 543)
scroll9 = Scroll(70, 285)
wall1 = Wall(185, 115, 225, 185)
wall3 = Wall(90, 175, 120, 140)
wall4 = Wall(395, 275, 120, 140)
wall5 = Wall(0, 130, 150, 60)
wall6 = Wall(260, 260, 75, 75)
wall7 = Wall(370, 260, 230, 105)

# Game's State
unpause, pause = 1, 0
state = pause

# Main Loop
run = True
while run:
    # Main Menu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                level = 0
                enemy1.health = 60
                enemy2.health = 60
                player.health = 60
                player.health_counter = 3
                scroll1.alive = True
                scroll2.alive = True
                scroll3.alive = True
                scroll4.alive = True
                scroll5.alive = True
                scroll6.alive = True
                scroll7.alive = True
                scroll8.alive = True
                scroll9.alive = True
                state = unpause
            if event.key == pygame.K_p:
                state = pause
            if event.key == pygame.K_r:
                state = unpause

    # Game Begins
    if state == unpause:
        user = pygame.key.get_pressed()
        player.move(user)
        player.shoot()
        enemy1.shoot()
        enemy2.shoot()

        # Player-Enemy Collision
        enemy_list = pygame.sprite.Group(enemy1, enemy2)
        if pygame.sprite.spritecollide(player, enemy_list, False):
            if player.health > 0 and enemy1.health > 0 and enemy2.health > 0:
                player.health -= 20
                player.health_counter -= 1
                player.rect.x = 250
                player.rect.y = 445

        # Player-Attacks-Enemy Collision
        for wind in player.winds:
            w_attack = pygame.sprite.Group(wind)
            if pygame.sprite.spritecollide(enemy1, w_attack, False):
                if enemy1.health > 0:
                    enemy1.health -= (20 + player.iroh)
                    player.winds.remove(wind)
            if pygame.sprite.spritecollide(enemy2, w_attack, False):
                if enemy2.health > 0:
                    enemy2.health -= (20 + player.iroh)
                    player.winds.remove(wind)

        # Enemy-Attacks-Player Collision
        for earth in enemy1.attacks:
            e_attack = pygame.sprite.Group(earth)
            if pygame.sprite.spritecollide(player, e_attack, False):
                if player.health > 0:
                    player.health -= (20 + enemy1.iroh)
                    player.health_counter -= 1
                    enemy1.attacks.remove(earth)
                    h_sound.play(0)

        for earth in enemy2.attacks:
            e_attack = pygame.sprite.Group(earth)
            if pygame.sprite.spritecollide(player, e_attack, False):
                if player.health > 0:
                    player.health -= (20 + enemy2.iroh)
                    player.health_counter -= 1
                    enemy2.attacks.remove(earth)
                    h_sound.play(0)

        # Level One
        if level == 0:
            enemy1.image = pygame.image.load(os.path.join('Earth', 'EarthLord.png'))
            enemy2.image = pygame.image.load(os.path.join('Earth', 'EarthLord.png'))
            for attack in enemy1.attacks:
                attack.image = pygame.image.load(os.path.join('Earth', 'earth_up.png'))
            for attack in enemy2.attacks:
                attack.image = pygame.image.load(os.path.join('Earth', 'earth_up.png'))

            # Level One - Wall Collisions
            wall_list = pygame.sprite.Group(wall1)
            player_hit_list = pygame.sprite.spritecollide(player, wall_list, False)
            for block in player_hit_list:
                if player.f_right:
                    player.rect.right = block.rect.left
                elif player.f_left:
                    player.rect.left = block.rect.right
                elif player.f_up:
                    player.rect.top = block.rect.bottom
                elif player.f_down:
                    player.rect.bottom = block.rect.top

        # Level One - Scroll Collisions
        scroll_a = pygame.sprite.Group(scroll1)
        if pygame.sprite.spritecollide(player, scroll_a, False):
            scroll1.alive = False
        scroll_b = pygame.sprite.Group(scroll2)
        if pygame.sprite.spritecollide(player, scroll_b, False):
            scroll2.alive = False

        # Level One - Zuko Upgrade
        if scroll1.alive is False and scroll2.alive is False and user[pygame.K_1]:
            player.zuko = 4

        # Level Two
        if level == 1:
            player.zuko = 0
            enemy1.zuko = 6
            enemy2.zuko = 6
            enemy1.image = pygame.image.load(os.path.join('Water', 'WaterLord.png'))
            enemy2.image = pygame.image.load(os.path.join('Water', 'WaterLord.png'))
            for attack in enemy1.attacks:
                attack.image = pygame.image.load(os.path.join('Water', 'water_up.png'))
            for attack in enemy2.attacks:
                attack.image = pygame.image.load(os.path.join('Water', 'water_up.png'))

            # Level Two - Wall Collisions
            wall_list = pygame.sprite.Group(wall3, wall4)
            player_hit_list = pygame.sprite.spritecollide(player, wall_list, False)
            for block in player_hit_list:
                if player.f_right:
                    player.rect.right = block.rect.left
                elif player.f_left:
                    player.rect.left = block.rect.right
                elif player.f_up:
                    player.rect.top = block.rect.bottom
                elif player.f_down:
                    player.rect.bottom = block.rect.top

            # Level Two - Scroll Collisions
            scroll_a = pygame.sprite.Group(scroll3)
            if pygame.sprite.spritecollide(player, scroll_a, False):
                scroll3.alive = False
            scroll_b = pygame.sprite.Group(scroll4)
            if pygame.sprite.spritecollide(player, scroll_b, False):
                scroll4.alive = False
            scroll_c = pygame.sprite.Group(scroll5)
            if pygame.sprite.spritecollide(player, scroll_c, False):
                scroll5.alive = False

        # Level Two - Iroh Upgrade
        if scroll3.alive is False and scroll4.alive is False and scroll5.alive is False and user[pygame.K_2]:
            player.iroh = 10

        # Level Three
        if level == 2:
            player.zuko = 0
            enemy1.zuko = 0
            enemy2.zuko = 0
            player.iroh = 0
            enemy1.iroh = 10
            enemy2.iroh = 10
            enemy1.image = pygame.image.load(os.path.join('Fire', 'FireLord.png'))
            enemy2.image = pygame.image.load(os.path.join('Fire', 'FireLord.png'))
            for attack in enemy1.attacks:
                attack.image = pygame.image.load(os.path.join('Fire', 'fire_up.png'))
            for attack in enemy2.attacks:
                attack.image = pygame.image.load(os.path.join('Fire', 'fire_up.png'))

            # Level Three - Wall Collisions
            wall_list = pygame.sprite.Group(wall5, wall6, wall7)
            player_hit_list = pygame.sprite.spritecollide(player, wall_list, False)
            for block in player_hit_list:
                if player.f_right:
                    player.rect.right = block.rect.left
                elif player.f_left:
                    player.rect.left = block.rect.right
                elif player.f_up:
                    player.rect.top = block.rect.bottom
                elif player.f_down:
                    player.rect.bottom = block.rect.top

            # Level Three - Scroll Collisions
            scroll_a = pygame.sprite.Group(scroll6)
            if pygame.sprite.spritecollide(player, scroll_a, False):
                scroll6.alive = False
            scroll_b = pygame.sprite.Group(scroll7)
            if pygame.sprite.spritecollide(player, scroll_b, False):
                scroll7.alive = False
            scroll_c = pygame.sprite.Group(scroll8)
            if pygame.sprite.spritecollide(player, scroll_c, False):
                scroll8.alive = False
            scroll_d = pygame.sprite.Group(scroll9)
            if pygame.sprite.spritecollide(player, scroll_d, False):
                scroll9.alive = False

            # Level Three - Azula Upgrade
            if scroll6.alive is False and scroll7.alive is False and scroll8.alive is False and scroll9.alive is False and \
                    user[pygame.K_3]:
                player.azula += 1
                if player.azula == 1:
                    player.health += 20
                    if player.health_counter < 3:
                        player.health_counter += 1

        # Player Wins
        if enemy1.health <= 0 and enemy2.health <= 0 and level < 2:
            level += 1
            enemy1.health = 60
            enemy2.health = 60
            player.rect.x = 250
            player.rect.y = 445
            player.health = 60
            player.health_counter = 3

        if enemy1.health == 0 and enemy2.health == 0 and level == 2:
            window.blit(pygame.font.SysFont('Consolas', 32).render('Congratulations, you won!', True,
                                                                   pygame.color.Color('Black')),
                        (100, 280))
            pygame.display.flip()
            w_sound.play(0)
            pygame.time.delay(1500)
            state = pause
            level = 0
            enemy1.health = 60
            enemy2.health = 60
            player.health = 60
            player.health_counter = 3

        # Player Loses
        if player.health == 0:
            window.blit(
                pygame.font.SysFont('Consolas', 32).render('Sorry, you lost!', True, pygame.color.Color('Black')),
                (145, 280))
            pygame.display.flip()
            l_sound.play(0)
            pygame.time.delay(1500)
            state = pause
            level = 0
            enemy1.health = 60
            enemy2.health = 60
            player.health = 60
            player.health_counter = 3

        draw_game()

    # Tutorial
    elif state == pause:
        if pygame.key.get_pressed()[pygame.K_t]:
            window.fill((0, 0, 0))
            window.blit(pygame.font.SysFont('Consolas', 20).render(
                "After the earth, water and fire tribes attack Aaang's"
                , True, pygame.color.Color('White')), (0, 10))
            window.blit(pygame.font.SysFont('Consolas', 20).render(
                'village and take his community hostage, he must use'
                , True, pygame.color.Color('White')), (0, 30))
            window.blit(pygame.font.SysFont('Consolas', 20).render(
                'his air-bending skills to get past the tribes, and'
                , True, pygame.color.Color('White')), (0, 50))
            window.blit(pygame.font.SysFont('Consolas', 20).render(
                'free his people.', True, pygame.color.Color('White')), (0, 70))
            window.blit(pygame.font.SysFont('Consolas', 32).render(
                '[s] = Start'
                , True, pygame.color.Color('Green')), (0, 110))
            window.blit(pygame.font.SysFont('Consolas', 32).render(
                '[p] = Pause'
                , True, pygame.color.Color('Green')), (0, 140))
            window.blit(pygame.font.SysFont('Consolas', 32).render(
                '[r] = Resume'
                , True, pygame.color.Color('Green')), (0, 170))
            window.blit(pygame.font.SysFont('Consolas', 32).render(
                '[^] = Up'
                , True, pygame.color.Color('Green')), (0, 220))
            window.blit(pygame.font.SysFont('Consolas', 32).render(
                '[v] = Down'
                , True, pygame.color.Color('Green')), (0, 250))
            window.blit(pygame.font.SysFont('Consolas', 32).render(
                '[>] = Right'
                , True, pygame.color.Color('Green')), (0, 280))
            window.blit(pygame.font.SysFont('Consolas', 32).render(
                '[<] = Left'
                , True, pygame.color.Color('Green')), (0, 310))
            window.blit(pygame.font.SysFont('Consolas', 32).render(
                '[space bar] = Shoot'
                , True, pygame.color.Color('Green')), (0, 340))
            window.blit(pygame.font.SysFont('Consolas', 20).render(
                'After collecting two scrolls in the first level, press'
                , True, pygame.color.Color('Green')), (0, 390))
            window.blit(pygame.font.SysFont('Consolas', 20).render(
                '[1] to increase your rate of fire.'
                , True, pygame.color.Color('Green')), (0, 410))
            window.blit(pygame.font.SysFont('Consolas', 20).render(
                'After collecting three scrolls in the second level,'
                , True, pygame.color.Color('Green')), (0, 430))
            window.blit(pygame.font.SysFont('Consolas', 20).render(
                "press [2] to increase damage to the enemy."
                , True, pygame.color.Color('Green')), (0, 450))
            window.blit(pygame.font.SysFont('Consolas', 20).render(
                'After collecting four scrolls in the third level,'
                , True, pygame.color.Color('Green')), (0, 470))
            window.blit(pygame.font.SysFont('Consolas', 20).render(
                'press [3] to boost health.'
                , True, pygame.color.Color('Green')), (0, 490))
            pygame.display.flip()

        # Main Display
        else:
            window.fill((0, 0, 0))
            window.blit(
                pygame.font.SysFont('Consolas', 64).render('The Savior', True, pygame.color.Color('Light Blue')),
                (130, 70))
            window.blit(pygame.font.SysFont('Consolas', 32).render('Menu', True, pygame.color.Color('White')),
                        (250, 160))
            window.blit(
                pygame.font.SysFont('Consolas', 18).render('Start [Press "s"]', True, pygame.color.Color('White')),
                (200, 220))
            window.blit(
                pygame.font.SysFont('Consolas', 18).render('Pause [Press "p"]', True, pygame.color.Color('White')),
                (200, 280))
            window.blit(
                pygame.font.SysFont('Consolas', 18).render('Resume [Press "r"]', True, pygame.color.Color('White')),
                (195, 340))
            window.blit(
                pygame.font.SysFont('Consolas', 18).render('Tutorial [Hold "t"]', True, pygame.color.Color('White')),
                (190, 400))
            pygame.display.flip()
        continue
