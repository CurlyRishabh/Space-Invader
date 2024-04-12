'''space invader'''
import pygame
from alien import Alien
from player import Player
import obstacle


class Game:
    def __init__(self):
        # player setup
        player_sprite = Player(
            (SCREEN_WIDTH / 2, SCREEN_HEIGHT),
            SCREEN_WIDTH,
            speed=5
        )
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_number = 3
        self.obstacle_x_positions = [
            float((num + (1/self.obstacle_number))
                  *
                  (SCREEN_WIDTH / (self.obstacle_number)))
            for num in range(self.obstacle_number)
        ]
        self.create_multiple_obstacle(x_start=0,
                                      y_start=480,
                                      offset=self.obstacle_x_positions
                                      )

        # alien
        self.alien = pygame.sprite.Group()
        self.create_alien()

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == 'x':

                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size,
                                           (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacle(self, x_start, y_start, offset):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)

    # alien functions
    def create_alien(self):
        for i in range(4):
            for j in range(3):
                if j == 0:
                    color = "green"
                elif j == 1:
                    color = "red"
                elif j == 2:
                    color = "yellow"
                x = Alien(color, (100+(i*50), 100+(j*50)),
                          SCREEN_HEIGHT,
                          SCREEN_WIDTH)
                self.alien.add(x)

    def update_alien_group(self):
        self.alien.update()
        self.alien.draw(screen)
        for alien in self.alien:
            alien.lasers.draw(screen)

    # collision function
    def collision_check(self):
        # player laser
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # obstacle collision
                if pygame.sprite.spritecollide(laser,
                                               self.blocks, dokill=True
                                               ):
                    laser.kill()
                # alien collision
                if pygame.sprite.spritecollide(laser,
                                               self.alien, dokill=True
                                               ):
                    laser.kill()
        #
        for alien in self.alien:
            for laser in alien.lasers:
                if pygame.sprite.spritecollide(laser, self.blocks,
                                               dokill=True):
                    laser.kill()
                if pygame.sprite.spritecollide(laser,
                                               self.player,
                                               dokill=True):
                    laser.kill()

    def run(self):
        'update/draw sprite groups'
        # player update
        self.player.update()
        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)

        self.blocks.draw(screen)

        self.update_alien_group()

        self.collision_check()


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
    SCREEN_WIDTH = 600
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Some game")
    clock = pygame.time.Clock()
    execute()
