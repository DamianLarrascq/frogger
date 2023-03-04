import pygame
import sys
from settings import *
from player import Player
from random import choice
from car import Car
from random import randint
from sprite import SimpleSprite, LongSprite


class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.bg = pygame.image.load('../graphics/main/map.png').convert()
        self.fg = pygame.image.load('../graphics/main/overlay.png').convert_alpha()

    def customize_draw(self):

        self.offset.x = player.rect.centerx - W_WIDTH / 2
        self.offset.y = player.rect.centery - W_HEIGHT / 2

        DP_SURF.blit(self.bg, -self.offset)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            DP_SURF.blit(sprite.image, offset_pos)

        DP_SURF.blit(self.fg, -self.offset)


# init pygame
pygame.init()
clock = pygame.time.Clock()
DP_SURF = pygame.display.set_mode((W_WIDTH,W_HEIGHT))
pygame.display.set_caption('Frogger')

# sprite groups
all_sprites = AllSprites()

# sprites
player = Player(all_sprites,(2062,3274))
# car = Car(all_sprites, (800,200))

# timer
car_timer = pygame.event.custom_type()
pygame.time.set_timer(car_timer, 100)
pos_list = []

# sprite setup
for file_name, pos_list in SIMPLE_OBJECTS.items():
    path = f'../graphics/objects/simple/{file_name}.png'
    surf = pygame.image.load(path).convert_alpha()

    for pos in pos_list:
        SimpleSprite(surf, pos, all_sprites)

for file, pos_list in LONG_OBJECTS.items():
    long_path = f'../graphics/objects/long/{file}.png'
    long_surf = pygame.image.load(long_path).convert_alpha()

    for pos in pos_list:
        LongSprite(long_surf, pos, all_sprites)

# game loop
while True:

    # framerate limit
    dt = clock.tick(60) / 1000

    # 1. event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == car_timer:
            random_pos = choice(CAR_START_POSITIONS)
            if random_pos not in pos_list:
                pos_list.append(random_pos)
                pos = (random_pos[0], random_pos[1] + randint(-8, 8))
                Car(all_sprites, pos)
            if len(pos_list) > 5:
                del pos_list[0]

    # 2. update graphics
    all_sprites.update(dt)

    # 3. draw graphics
    DP_SURF.fill('black')

    # all_sprites.draw(DP_SURF)
    all_sprites.customize_draw()

    # 3. draw frame
    pygame.display.update()
