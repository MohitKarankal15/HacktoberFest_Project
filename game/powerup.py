"""
Power-Up System for GEMMA WORLD
Implements 4 original power-ups:
1. Health Crystal
2. Speed Boost
3. Shield
4. Coin Magnet
"""
import pygame
from game.asset_factory import create_item_surface

class PowerUp:
    def __init__(self, x, y, powerup_type="health_crystal"):
        self.x = float(x)
        self.y = float(y)
        self.start_y = float(y)
        self.size = 30
        self.powerup_type = powerup_type
        self.is_collected = False
        self.anim_tick = 0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)

    def update(self, dt):
        """Animates floating bobbing effect."""
        if self.is_collected:
            return
        self.anim_tick += 1
        hover = ((self.anim_tick // 5) % 6) - 3
        self.y = self.start_y + (hover * 0.9)

    def draw(self, surface, camera_offset_x=0, camera_offset_y=0):
        """Renders powerup item with radiant glow."""
        if self.is_collected:
            return

        render_x = int(self.x - camera_offset_x)
        render_y = int(self.y - camera_offset_y)

        # Subtle halo aura
        halo_surf = pygame.Surface((self.size + 14, self.size + 14), pygame.SRCALPHA)
        pygame.draw.circle(
            halo_surf,
            (255, 255, 255, 45),
            ((self.size + 14) // 2, (self.size + 14) // 2),
            (self.size + 10) // 2
        )
        surface.blit(halo_surf, (render_x - 7, render_y - 7))

        sprite = create_item_surface(self.powerup_type, self.size, self.anim_tick)
        surface.blit(sprite, (render_x, render_y))
