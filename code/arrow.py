import pygame
from settings import *
from random import randint

class Arrow(pygame.sprite.Sprite):
    def __init__(self, player, groups, obstacle_sprites, attackable_sprites):
        super().__init__(groups)
        self.sprite_type = 'weapon'
        direction = player.status.split('_')[0]
        self.image = pygame.image.load(os.path.join(dir_path, 'graphics', 'weapons', 'arrow', f'{direction}.png')).convert_alpha()
        # placement
        self.get_placement(player, direction)
        self.obstacle_sprites = obstacle_sprites
        self.attackable_sprites = attackable_sprites
        self.pos = pygame.math.Vector2(self.rect.center)
        self.velocity = pygame.math.Vector2(ARROW_SPEED * self.get_shoot_direction(direction).x, ARROW_SPEED * self.get_shoot_direction(direction).y)

    def get_placement(self, player, direction):
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(0, 16))
        elif direction == 'left':
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(0, 16))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10, 0))
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10, 0))

    def get_shoot_direction(self, direction):
        direction_map = {
            'up': pygame.math.Vector2(0, -1),
            'down': pygame.math.Vector2(0, 1),
            'left': pygame.math.Vector2(-1, 0),
            'right': pygame.math.Vector2(1, 0),
        }
        return direction_map.get(direction, pygame.math.Vector2(0, 0))

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos