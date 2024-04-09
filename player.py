import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
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
