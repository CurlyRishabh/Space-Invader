'''space invader'''
import pygame
from player import Player


class Game:
    def __init__(self):
        player_sprite = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT))
        self.player = pygame.sprite.GroupSingle(player_sprite)

    def run(self):
        'update/draw sprite groups'
        self.player.draw(screen)
        self.player.update()


def execute():
    run = True
    game = Game()
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        screen.fill((30, 3, 30))
        game.run()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    pygame.init()
    SCREEN_WIDTH = 750
    SCREEN_HEIGHT = 700
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Some game")
    clock = pygame.time.Clock()
    execute()
