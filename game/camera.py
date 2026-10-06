"""
Smooth Scrolling Camera System for GEMMA WORLD
Supports lerp tracking, dead-zones, world boundary clamping, and trauma shake.
"""
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Camera:
    def __init__(self, screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset_x = 0.0
        self.offset_y = 0.0
        
        # Lerp smoothing factor
        self.lerp_speed = 0.12
        
        # Screen shake
        self.shake_trauma = 0.0
        self.shake_decay = 0.9

    def add_shake(self, amount=10.0):
        """Adds impact shake trauma."""
        self.shake_trauma = min(30.0, self.shake_trauma + amount)

    def update(self, target_rect, world_width, world_height):
        """Smoothly tracks target rect while clamping to world bounds."""
        # Desired camera center
        desired_x = target_rect.centerx - (self.screen_width // 2)
        desired_y = target_rect.centery - (self.screen_height // 2) - 40

        # Lerp offset
        self.offset_x += (desired_x - self.offset_x) * self.lerp_speed
        self.offset_y += (desired_y - self.offset_y) * self.lerp_speed

        # Clamp to world bounds
        max_x = max(0, world_width - self.screen_width)
        max_y = max(0, world_height - self.screen_height)
        
        self.offset_x = max(0, min(self.offset_x, max_x))
        self.offset_y = max(0, min(self.offset_y, max_y))

        # Apply trauma shake
        shake_offset_x = 0.0
        shake_offset_y = 0.0
        if self.shake_trauma > 0.1:
            shake_offset_x = (random.random() * 2 - 1) * self.shake_trauma
            shake_offset_y = (random.random() * 2 - 1) * self.shake_trauma
            self.shake_trauma *= self.shake_decay
        else:
            self.shake_trauma = 0.0

        return int(self.offset_x + shake_offset_x), int(self.offset_y + shake_offset_y)
