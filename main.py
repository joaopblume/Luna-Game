import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

gravity = 10
HEIGHT = 500
WIDTH = 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

FPS = 20

SCORE_FONT = pygame.font.SysFont("comicsans", 40)
GAME_OVER_FONT = pygame.font.SysFont("comicsans", 100)

BACKGROUND_SONG = pygame.mixer.Sound(os.path.join("sounds", "background_song.wav"))
JUMP_SOUND = pygame.mixer.Sound(os.path.join("sounds", "jump_sound.wav"))
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join("sounds", "game_over.wav"))
BANANA_SOUND = pygame.mixer.Sound(os.path.join("sounds", "banana.wav"))

cloud_speed = 3
game_speed = 10
points = 0

GROUND_WIDTH = 2 * WIDTH
GROUND_HEIGHT = 80
pygame.display.set_caption("Luna's Game")

BACKGROUND = pygame.image.load(os.path.join("sprites", "night.png"))
BACKGROUND = pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT))


class Cloud(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join("sprites", "cloud.png"))
        self.image = pygame.transform.scale(self.image, (200, 80))
        self.rect = self.image.get_rect()

        self.rect[0] = xpos
        self.rect[1] = 100

    def update(self):
        self.rect[0] -= cloud_speed

class Luna(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.jumping = False
        self.gravity = 14

        self.images = [pygame.image.load(os.path.join("sprites", "luna1.png")).convert_alpha(),
                       pygame.image.load(os.path.join("sprites", "luna2.png")).convert_alpha(),
                       pygame.image.load(os.path.join("sprites", "luna3.png")).convert_alpha()]

        self.current_image = 0

        self.image = pygame.image.load(os.path.join("sprites", "luna2.png"))
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()

        self.rect[0] = 0
        self.rect[1] = 275

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.image = pygame.transform.scale(self.image, (200, 200))

        if self.jumping:
            self.rect[1] -= self.gravity
            self.gravity -= 1
            if self.gravity <= - 15:
                self.jumping = False
                self.gravity = 14

    def jump(self):
        self.jumping = True
        JUMP_SOUND.play()


class Ground(pygame.sprite.Sprite):
    def __init__(self, g_width, g_height, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join("sprites", "platform-ground.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (g_width, g_height))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = 435

    def update(self):
        self.rect[0] -= game_speed


class Banana(pygame.sprite.Sprite):
    def __init__(self, banana_x, banana_y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join("sprites", "banana.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))

        self.rect = self.image.get_rect()
        self.rect[0] = banana_x
        self.rect[1] = banana_y

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= game_speed


class Tomato(pygame.sprite.Sprite):
    def __init__(self, tomato_x, tomato_y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(os.path.join("sprites", "tomato.png")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))

        self.rect = self.image.get_rect()
        self.rect[0] = tomato_x
        self.rect[1] = tomato_y

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= game_speed


def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])


def get_banana(xpos):

    x = xpos
    y = random.choice([240, 350])

    banana = Banana(x, y)
    return banana


def get_tomato(xpos):

    x = xpos
    y = random.choice([240, 350])

    tomato = Tomato(x, y)
    return tomato


def score(text):

    score_text = SCORE_FONT.render("Score: " + text, True, (255, 255, 255))
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))


def lose():
    lose_text = GAME_OVER_FONT.render("GAME OVER!", True, (255, 255, 255))
    WIN. blit(lose_text, (WIDTH / 2 - lose_text.get_width() / 2,  HEIGHT / 2 - lose_text.get_height() / 2))
    pygame.display.update()
    GAME_OVER_SOUND.play()
    BACKGROUND_SONG.stop()
    pygame.time.delay(5000)


def draw_window():

    WIN.blit(BACKGROUND, (0, 0))

    ground_group.update()
    ground_group.draw(WIN)

    luna_group.update()
    luna_group.draw(WIN)

    banana_group.update()
    banana_group.draw(WIN)

    tomato_group.update()
    tomato_group.draw(WIN)

    cloud_group.update()
    cloud_group.draw(WIN)

    score(str(points))
    pygame.display.update()


def main():
    global points
    global game_speed
    BACKGROUND_SONG.play(loops=True)
    clock = pygame.time.Clock()
    run = True
    while run:
        game_speed += 0.05
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    luna.jump()

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDTH, GROUND_HEIGHT, GROUND_WIDTH - 100)
            ground_group.add(new_ground)

        if is_off_screen(cloud_group.sprites()[0]):
            cloud_group.remove(cloud_group.sprites()[0])
            new_cloud = Cloud(WIDTH * 2)
            cloud_group.add(new_cloud)

        if pygame.sprite.groupcollide(luna_group, banana_group, False, True, pygame.sprite.collide_mask):
            points += 1
            BANANA_SOUND.play()

        if pygame.sprite.groupcollide(luna_group, tomato_group, False, False, pygame.sprite.collide_mask):
            lose()
            run = False

        pygame.display.update()
        draw_window()

    pygame.quit()


luna_group = pygame.sprite.Group()
luna = Luna()
luna_group.add(luna)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH, GROUND_HEIGHT, GROUND_WIDTH * i)
    ground_group.add(ground)

banana_group = pygame.sprite.Group()
for i in range(30):
    bananas = get_banana(WIDTH * i + 600)
    banana_group.add(bananas)

tomato_group = pygame.sprite.Group()
for i in range(30):
    tomatoes = get_tomato((WIDTH * i * 3) + 900)
    tomato_group.add(tomatoes)

cloud_group = pygame.sprite.Group()
for i in range(2):
    cloud = Cloud(WIDTH * i)
    cloud_group.add(cloud)

if __name__ == "__main__":
    main()
