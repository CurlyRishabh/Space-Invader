'''space invader'''
import pygame
from alien import Alien, span_group_level
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
        self.alien_row = 2
        self.create_level(0)
        self.level = 0
        self.max_level = len(span_group_level)-1

        # health and score
        self.live_surf = pygame.image.load(
            './graphics/player.png').convert_alpha()
        self.live = 3
        self.score = 0
        self.font = pygame.font.Font('./font/Pixeled.ttf', 20)

        # sound
        music = pygame.mixer.Sound('./audio/music.wav')
        music.set_volume(0.8)
        music.play(loops=-1)
        self.explosion_sound = pygame.mixer.Sound('./audio/explosion.wav')
        self.explosion_sound.set_volume(0.4)

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

    def create_level(self, level):
        spawn_area = span_group_level[level]
        color = ''
        for row_index, row in enumerate(spawn_area):
            for col_index, col in enumerate(row):
                x = 100 + col_index * 50 + 50
                y = 100 + row_index * 50
                if col == 'g':
                    color = "green"
                elif col == 'r':
                    color = "red"
                elif col == 'y':
                    color = "yellow"
                alien = Alien(color, (x, y), SCREEN_HEIGHT, SCREEN_WIDTH)
                self.alien.add(alien)

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
                alien_hit = pygame.sprite.spritecollide(laser,
                                                        self.alien,
                                                        dokill=True)
                if alien_hit:
                    for alien in alien_hit:
                        self.score += alien.value
                        self.explosion_sound.play()
                    laser.kill()
                if len(self.alien) == 0:
                    self.level += 1
                    if self.level > self.max_level:
                        self.level = 0
                    self.create_level(self.level)
        # alien laser
        for alien in self.alien:
            for laser in alien.lasers:
                # obstacle collide
                if pygame.sprite.spritecollide(laser, self.blocks,
                                               dokill=True):
                    laser.kill()
                # player collide
                if pygame.sprite.spritecollide(laser,
                                               self.player,
                                               dokill=False):
                    laser.kill()
                    self.live -= 1
                    self.explosion_sound.play()

    def display_lives(self):
        for live in range(self.live):
            live_surf_rect = self.live_surf.get_rect(
                topleft=(350 + live*80, 0)
            )
            screen.blit(self.live_surf, live_surf_rect)

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}', False, 'white')
        score_rect = score_surf.get_rect(topleft=(0, 0))
        screen.blit(score_surf, score_rect)

    def game_over(self):
        if self.live <= 0:
            end_surf = self.font.render('GAME OVER', False, 'white')
            end_rect = end_surf.get_rect(topleft=(200, 300))
            screen.blit(end_surf, end_rect)
            self.alien.empty()
            self.player.empty()

    def run(self):
        'update/draw sprite groups'
        # player update
        if self.player:
            self.player.update()
            self.player.sprite.lasers.draw(screen)
            self.player.draw(screen)
            self.blocks.draw(screen)
            self.update_alien_group()
            self.collision_check()
            self.display_lives()
        self.display_score()
        self.game_over()


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
    pygame.display.set_caption("Space Invader")
    clock = pygame.time.Clock()
    execute()
