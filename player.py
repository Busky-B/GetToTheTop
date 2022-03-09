import pygame
import game_settings
class Player(pygame.sprite.Sprite):
    def __init__(self) -> None:
        self.init_player_variables()
        self.init_player_sprite()

    def init_player_sprite(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_surface = self.load_sprite_image("./assets/MascotBunnyCharacter/Bunny1/__Bunny1_Idle_000.png")
        self.rect = self.image_surface.get_rect()
        self.rect.top = game_settings.window_height - 200 # starting position

    def load_sprite_image(self, image_url):
        image = self.image.load(image_url)
        return pygame.transform.scale(image, (50, 60))

    def init_player_variables(self):
        # Setup player variables
        self._grounded = False
        self._jumping = False # Maybe use this instead of grounded for checking if grounded ?
        self._falling = False # Needed since consecutive jumps are not allowed
        self._reversed_sprite = False # Determines if playersprite.png should be reversed or not (left/right)
        self._win_condition = False # Use to check if game should end or not
        self._standing_on_platform = False # If standing on platform, jumping is allowed again
        self._points = 0
        self._gravity = game_settings.gravity
        self.acceleration = game_settings.acceleration 

    def add_points(self):
        self._points += 1

    def toggle_jumping(self):
        self._jumping = not self._jumping

    def toggle_falling(self):
        self._falling = not self._falling
        
    def toggle_sprite_direction(self):
        self._reversed_sprite = not self._reversed_sprite