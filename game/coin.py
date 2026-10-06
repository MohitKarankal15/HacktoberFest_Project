"""
Coin collectible system for GEMMA WORLD
Supports magnetic attraction when Nova has the Coin Magnet power-up.
"""
import pygame
from config import MAGNET_RADIUS
from game.asset_factory import create_item_surface

class Coin:
    def __init__(self, x, y, value=1):
        self.x = float(x)
        self.y = float(y)
        self.start_y = float(y)
        self.size = 26
        self.value = value
        self.is_collected = False
        self.anim_tick = 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def update(self, dt, player):
        """Updates gentle hovering and magnetic pull toward player."""
        if self.is_collected:
            return

        self.anim_tick += 1

        # Coin Magnet pull effect
        if player.magnet_timer > 0:
            dx = player.x + player.width / 2 - (self.x + self.size / 2)
            dy = player.y + player.height / 2 - (self.y + self.size / 2)
            dist = (dx**2 + dy**2)**0.5
            if dist < MAGNET_RADIUS and dist > 1:
                pull_speed = 7.5
                self.x += (dx / dist) * pull_speed
                self.y += (dy / dist) * pull_speed
        else:
            # Gentle hover bobbing
            hover_offset = ((self.anim_tick // 4) % 6) - 3
            self.y = self.start_y + (hover_offset * 0.7)

    def draw(self, surface, camera_offset_x=0, camera_offset_y=0):
        """Renders animated rotating coin."""
        if self.is_collected:
            return

        render_x = int(self.x - camera_offset_x)
        render_y = int(self.y - camera_offset_y)

        sprite = create_item_surface("coin", self.size, self.anim_tick)
        surface.blit(sprite, (render_x, render_y))
