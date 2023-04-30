"""
File for overarching bird classes.
"""
from abc import ABC, abstractmethod
import pygame


class BirdCharacter(pygame.sprite.Sprite, ABC):
    """
    Abstract class representing all bird characters (player and enemies).

    Attributes:
        _max_hp: an integer representing the max health of the character
        _remaining_hp: an integer representing the remaining health
        of the character
        _atk: an integer representing the amount of damage the character
        does in a single attack
        _ms: an integer representing how fast the character moves across
        the screen
        _width: an integer representing the width of the character image
        _height: an integer representing the height of the character
        image
        _image: a pygame image representing the image of the character
        _start_pos: a tuple containing the (x,y) starting position
        of the character
        _rect: a pygame rectangle mapped to the character's image
        _screen: the surface that the game is displayed on
        _is_facing_right: a boolean representing if the character is facing
        right
        _is_facing_forward: a boolean representing if the character is
        facing forward
        _is_atking: a boolean representing if the character is attacking
        _char_name: a string representing the first section of the character
        image file path
    """

    def __init__(self, image_path, screen):
        """
        Initializes some BirdCharacter attributes for subclasses.
        """
        pygame.sprite.Sprite.__init__(self)
        # Declare attributes to be initialized more specifically in subclasses.
        self._max_hp = None
        self._remaining_hp = self._max_hp
        self._atk = None
        self._ms = None
        self._width = None
        self._height = None
        self._start_pos = None
        self._rect = None
        self._attack_hitbox = pygame.sprite.Sprite()

        # Set up universal attributes that are same for all subclasses
        self._image = pygame.image.load(image_path).convert_alpha()
        self._screen = screen
        self._is_facing_right = True
        self._is_facing_forward = True
        self._is_atking = False
        self._char_name = image_path.partition("_")[0]
        self._heading = 0

    @property
    def image(self):
        """
        Returns the character's pygame image.
        """
        return self._image

    @property
    def rect(self):
        """
        Returns the character's pygame rectangle.
        """
        return self._rect

    @property
    def atk(self):
        """
        Returns the character's integer attack stat.
        """
        return self._atk

    @property
    def width(self):
        """
        Returns the character's integer width.
        """
        return self._width

    @property
    def height(self):
        """
        Returns the character's integer width.
        """
        return self._height

    @property
    def heading(self):
        """
        Returns the integer heading.
        """
        return self._heading

    def take_damage(self, opponent_atk):
        """
        Lose an amount of HP based on opponent's ATK stat.

        Args:
            opponent_atk: an integer representing the opponent's atk stat
        """
        self._remaining_hp -= opponent_atk
        if self._remaining_hp <= 0:
            self.kill()

    def update(self):
        """
        Updates status of characters.
        """
        # Health bar
        hp_bar_thickness = 7
        hp_bar_gap = 15
        hp_bar_percent = self._remaining_hp / self._max_hp * self._width
        pygame.draw.rect(
            self._screen,
            "Green",
            pygame.Rect(
                self._rect.x,
                self._rect.y - hp_bar_gap,
                hp_bar_percent,
                hp_bar_thickness,
            ),
        )

        # Force characters to stay within screen bounds
        self.rect.x = max(0, self.rect.x)
        self.rect.x = min(self.rect.x, self._screen.get_width() - self.width)
        self.rect.y = max(hp_bar_gap + hp_bar_thickness, self.rect.y)
        self.rect.y = min(self.rect.y, self._screen.get_height() - self.height)

    def update_img(self):
        """
        Updates the character image to be correct according to the current
        attack and heading position.
        """
        if self._is_facing_forward:
            front_or_back = "front"
        else:
            front_or_back = "back"

        if self._is_facing_right:
            left_or_right = "right"
        else:
            left_or_right = "left"

        if self._is_atking:
            atk_or_idle = "atk"
        else:
            atk_or_idle = "idle"

        updated_img_path = (
            f"{self._char_name}_{front_or_back}_{left_or_right}_"
            + f"{atk_or_idle}.png"
        )

        self._image = pygame.image.load(updated_img_path).convert_alpha()
        self._image = pygame.transform.scale(
            self._image, (self._width, self._height)
        )

    # @abstractmethod
    # def attack(self):
    #     """
    #     Initializes an Attack instance that is associated with a BirdCharacter.
    #     Will be implemented in subclasses.
    #     MAKE LATER IF WE HAVE TIME
    #     """
