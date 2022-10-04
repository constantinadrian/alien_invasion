import pygame.font
import shelve
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
    """A class to report scoring information."""
    
    def __init__(self, ai_settings, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen

        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        
        # Font settings for scoring information.
        self.text_color = (230, 230, 230)
        self.font = pygame.font.SysFont(None, 48)

        # Declare new variable for saved high score
        # because we don't want to update high score during the game
        # especialy if user quits the game before it's over (game over)
        self.saved_high_score = 0

        # Get the high score
        self.get_high_score()
       
        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()

        # Prepare game level
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        """Turn the score into a rendered image."""
        self.rounded_score = int(round(self.stats.score, -1))
        self.score_str = "{:,}".format(self.rounded_score)

        self.score_image = self.font.render(self.score_str, True, self.text_color)
        
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20


    def save_high_score(self):
        """Save the high score with shelve - Python object persistence"""

        # Save the high score only if higher than previous
        if self.stats.high_score > self.saved_high_score:
            # Save the high score in key-value pair
            d = shelve.open('score.txt')    
            # d['high_score'] = self.score_str
            d['high_score'] = self.stats.high_score
            d.close()


    def get_high_score(self):
        """Read the high score with shelve - Python object persistence"""
        # Access the high score
        # Use a try - except block in case is the first
        # time we open the game and we have a key error
        try :
            d = shelve.open('score.txt')
            self.saved_high_score = d['high_score']
            d.close()
        except KeyError:
            self.saved_high_score = 0


    def prep_high_score(self):
        """Turn the high score into a rendered image."""

        if self.saved_high_score:
            high_score = self.saved_high_score
        else:
            high_score = int(round(self.stats.high_score, -1))
            
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
        self.text_color)
        
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        self.level_image = self.font.render(str(self.stats.level), True, self.text_color)
        
        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

        # Draw ships.
        self.ships.draw(self.screen)
