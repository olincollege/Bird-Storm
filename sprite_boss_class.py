"""
File for ProjectileBoss class.
"""
import random
import pygame
from sprite_bird_class import BirdCharacter

BOSS_IMG_SCALE = 0.25


class ProjectileBoss(BirdCharacter):
    def __init__(
        self,
        max_health,
        attack,
        movespeed,
        image_path,
        start_pos,
        bg,
        player,
    ):
        super().__init__(image_path, bg)
        self._max_hp = max_health
        self._atk = attack
        self._ms = movespeed
        self._remaining_hp = self._max_hp
        self.player = player
        self.incomplete_intro = True
        self.position = "center"
        self._img_scale_factor = BOSS_IMG_SCALE
        self._image = pygame.transform.scale_by(
            self._image, self._img_scale_factor
        )
        self._width = self._image.get_width()
        self._height = self._image.get_height()
        self._rect = self._image.get_rect(center=start_pos)
        self.complete_move = False
        self._is_facing_right = True
        self._new_pos = random.choice(
            ["center", "bottom left", "bottom right", "top left", "top right"]
        )
        self._hp_bar_width = self._width
        self.timer = 0

    def take_damage(self, opponent_atk, environment):
        """
        Lose an amount of HP based on opponent's ATK stat.

        Args:
            opponent_atk: an integer representing the opponent's atk stat
            environment: an Environment object representing the game
            environment.
        """
        self._remaining_hp -= opponent_atk
        if self._remaining_hp <= 0:
            self.kill()
            environment.set_boss_slain_true()

    def update(self):
        """
        Updates status of Boss.
        """
        super().update()

        if (
            self._rect.y < self._screen.get_height() / 2 - 100
            and self.incomplete_intro
            and self.timer % 10 == 0
        ):
            # change back to 1 later
            # Moves boss
            self._rect.y += 40
            # Forces player in place
            self.player.rect.y = self._screen.get_height() - 100
            self.player.rect.x = self._screen.get_width() / 2 - 50
            # Ends intro
            if self._rect.y >= self._screen.get_height() / 2 - 100:
                self.incomplete_intro = False

        if not self.incomplete_intro:
            if self.timer % 100 == 0:
                self._new_pos = random.choice(
                    [
                        "center",
                        "bottom left",
                        "bottom right",
                        "top left",
                        "top right",
                    ]
                )
            self.move_to_pos(self._new_pos)
        self.update_img()

        # increment timer
        self.timer += 1

    def move_to_pos(self, new_pos):
        """
        Moves boss enemy to the new position based on what string position
        is inputted.

        Args:
            new_pos: a string input representing the new location
        """
        edge_gap = 0

        if "bottom" in new_pos:
            new_y = self._screen.get_height() - self._height - edge_gap
        else:
            new_y = edge_gap

        if "left" in new_pos:
            new_x = edge_gap
        else:
            new_x = self._screen.get_width() - self._width - edge_gap

        if new_pos == "center":
            new_x = self._screen.get_width() / 2 - self._width / 2
            new_y = self._screen.get_height() / 2 - self._height / 2

        if new_x > self.rect.x:
            self._is_facing_right = True
            self._rect.x += self._ms
        elif new_x < self.rect.x:
            self._is_facing_right = False
            self._rect.x -= self._ms

        if new_y > self.rect.y:
            self._rect.y += self._ms
        elif new_y < self.rect.y:
            self._rect.y -= self._ms
