import pygame


class Sounds():
    """A class to store all sounds for Alien Invasion."""
    def __init__(self):
        """Initialize the game sounds."""
        pygame.mixer.init()

        # Game background music
        self.game_music = 'sounds/gamemusic-6082.wav'

        # Game sound music
        self.bullet_sound = pygame.mixer.Sound('sounds/blaster-2-81267.wav')
        self.alien_sound = pygame.mixer.Sound('sounds/hq-explosion-6288.wav')
        self.ship_sound = pygame.mixer.Sound('sounds/explosion-36210.wav')
        self.game_start_sound = pygame.mixer.Sound('sounds/game-start-6104.wav')
        self.level_up_sound = pygame.mixer.Sound('sounds/level-up-47165.wav')
        self.game_over_sound = pygame.mixer.Sound('sounds/videogame-gameover-sound-43894.wav')

        # Set volume for individual sounds as some sounds
        # may play louder due to how they were created
        self.bullet_sound.set_volume(0.2)
        self.alien_sound.set_volume(0.1)

    def play_game_music(self):
        """Play the game backgound music."""
        pygame.mixer.music.load(self.game_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(loops=-1)
        pygame.event.wait()
        
    def stop_game_music(self):
        """Stop the game backgound music."""
        pygame.mixer.music.stop()
