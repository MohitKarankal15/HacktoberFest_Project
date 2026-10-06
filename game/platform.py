"""
Platform System for GEMMA WORLD
Handles solid ground, floating tech-metal platforms, and one-way jump-through beams.
"""
import pygame
from game.asset_factory import create_platform_surface

class Platform:
    def __init__(self, x, y, width, height, platform_type="solid", is_dynamic=False, lifetime=None):
        self.x = float(x)
        self.y = float(y)
        self.width = width
        self.height = height
        self.platform_type = platform_type  # "ground", "floating", "oneway"
        self.is_oneway = (platform_type == "oneway")
        self.is_dynamic = is_dynamic        # Created by Gemma AI Director
        self.lifetime = lifetime            # Optional decay timer in seconds
        
        # Pre-render platform surface
        self.surface = create_platform_surface(width, height, platform_type)

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, dt):
        """Updates lifetime if dynamic."""
        if self.lifetime is not None:
            self.lifetime -= dt
            if self.lifetime <= 0:
                return False  # Mark for removal
        return True

    def draw(self, surface, camera_offset_x=0, camera_offset_y=0):
        """Renders platform with camera translation."""
        render_x = int(self.x - camera_offset_x)
        render_y = int(self.y - camera_offset_y)
        
        surface.blit(self.surface, (render_x, render_y))

        # Visual indicator if spawned by Gemma AI
        if self.is_dynamic:
            glow_surf = pygame.Surface((self.width, 3), pygame.SRCALPHA)
            pygame.draw.rect(glow_surf, (140, 90, 255, 180), (0, 0, self.width, 3))
            surface.blit(glow_surf, (render_x, render_y))
