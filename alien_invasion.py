import sys

import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
from sound_effects import Sounds
# import sound_effects as se 


def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Create an instance to store game statistics and create a scoreboard.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Create a sound instance
    se = Sounds()

    # Start the game background music
    se.play_game_music()

    # Transform backgound image to fill the screen
    bg_image = pygame.transform.smoothscale(ai_settings.bg_image, screen.get_size())

    # Make a ship.
    ship = Ship(ai_settings, screen)

    # Make a group to store bullets in.
    bullets = Group()

    # Make an alien.
    aliens = Group()

    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # Make the Play button.
    play_button = Button(ai_settings, screen, "Play")

    # Start the main loop for the game.
    while True:
        # Watch for keyboard and mouse events.
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb, se)


        if stats.game_active:
            # Update ship   
            ship.update()

            # Update bullets
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb, se)

            # Update Move from alien
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb, se)
        
        # Redraw the screen during each pass through the loop.
        gf.update_screen(ai_settings, screen, ship, bullets, aliens, bg_image, stats, play_button, sb)

run_game()
