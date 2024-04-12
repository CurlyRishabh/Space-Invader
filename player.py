import pygame
from laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        '''
            using convert_alpha() on that image converts it into a format
            that is optimized for faster blitting onto the screen while
            preserving the alpha transparency information. This optimization
            can improve the performance of your Pygame application, especially
            when dealing with images with transparency.
        '''
        self.image = pygame.image.load('./graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        # varibles for player movements
        self.speed = speed
        self.max_constraint = constraint

        # variables for laser shoot
        self.ready = True
        self.laser_time = 0
        self.laser_cooldown = 60

        self.lasers = pygame.sprite.Group()

        # shoot sound
        self.laser_sound = pygame.mixer.Sound('./audio/laser.wav')
        self.laser_sound.set_volume(0.5)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_SPACE] and self.ready:
            self.shoot_laser()
            self.laser_sound.play()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_constraint:
            self.rect.right = self.max_constraint

    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center))

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()
