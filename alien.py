import pygame
from alien_laser import Laser


class Alien(pygame.sprite.Sprite):
    def __init__(self, color, pos, x_constraint, y_constraint):
        super().__init__()
        self.color = color
        file_path = './graphics/'+self.color+'.png'
        self.image = pygame.image.load(file_path).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.lasers = pygame.sprite.Group()
        self.speed = 2
        self.x_constraint = x_constraint
        self.y_constraint = y_constraint
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 2000
        self.movement_state_x = True
        if color == 'red':
            self.value = 100
        elif color == 'green':
            self.value = 200
        else:
            self.value = 300

    def movement_x(self):
        if self.movement_state_x:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, color=self.color))
        self.ready = False
        self.laser_time = pygame.time.get_ticks()

    def constraint(self):
        if self.rect.x <= 0:
            self.rect.x = 0
            self.movement_state_x = True

        if self.rect.y <= 0:
            self.rect.y = 0

        if self.rect.y >= self.y_constraint:
            self.rect.y = self.y_constraint

        if self.rect.x >= self.x_constraint:
            self.rect.x = self.x_constraint
            self.movement_state_x = False

        if self.ready:
            self.shoot_laser()
        current_time = pygame.time.get_ticks()

        if current_time - self.laser_time >= self.laser_cooldown:
            self.ready = True

    def update(self):
        self.movement_x()
        self.constraint()
        self.lasers.update()


span_group_level = [
    [
        "rrrr",
        'yggy',
        'yyyy'
    ],
    [
        "yyyyy",
        'ygggy',
        'yyyyy'
    ],
    [
        "rrrrrrrr",
        'rrryyyrr',
        'gggggggg'
    ],
    [
        'rgrgrgrgrgrgr',
        '  rr  rr  rr ',
        ' yyyyyyyyyyyy',
        'gggg      ggg'
    ],
    ['rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',
     'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy',
     'ggggggggggggggggggggggggggggggg',
     'yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy'
     ]
]
