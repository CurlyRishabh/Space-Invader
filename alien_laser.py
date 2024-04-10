import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed=6, color='red'):
        super().__init__()
        self.image = pygame.Surface((4, 20))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed

    def destroy(self):
        if self.rect.y >= 600:
            print("kill_alien")
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()
