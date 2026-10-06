import pygame
import math

class BaseProjectile:
    def __init__(self, x, y, target_x, target_y, speed, damage, lifetime):
        self.x = float(x)
        self.y = float(y)
        self.damage = damage
        self.lifetime = lifetime
        self.speed = speed
        self.is_active = True
        self.width = 10
        self.height = 10
        
        # Calculate direction
        dx = target_x - x
        dy = target_y - y
        dist = math.hypot(dx, dy)
        if dist == 0:
            self.vx = speed
            self.vy = 0
        else:
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed
            
        self.angle = math.degrees(math.atan2(-dy, dx)) # for drawing

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, dt):
        if not self.is_active:
            return
        
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= dt
        
        if self.lifetime <= 0:
            self.is_active = False

    def draw(self, surface, camera_offset_x, camera_offset_y):
        pass


class WebProjectile(BaseProjectile):
    def __init__(self, x, y, target_x, target_y):
        super().__init__(x, y, target_x, target_y, speed=6.0, damage=0, lifetime=3.0)
        self.width = 12
        self.height = 12

    def draw(self, surface, camera_offset_x, camera_offset_y):
        if not self.is_active: return
        rx = int(self.x - camera_offset_x)
        ry = int(self.y - camera_offset_y)
        pygame.draw.circle(surface, (200, 200, 220), (rx + self.width//2, ry + self.height//2), self.width//2)
        pygame.draw.circle(surface, (255, 255, 255), (rx + self.width//2, ry + self.height//2), self.width//2 - 2)


class EnergyBlast(BaseProjectile):
    def __init__(self, x, y, target_x, target_y):
        super().__init__(x, y, target_x, target_y, speed=8.0, damage=15, lifetime=2.5)
        self.width = 16
        self.height = 16

    def draw(self, surface, camera_offset_x, camera_offset_y):
        if not self.is_active: return
        rx = int(self.x - camera_offset_x)
        ry = int(self.y - camera_offset_y)
        # Bright energy visual
        pygame.draw.circle(surface, (255, 255, 0), (rx + self.width//2, ry + self.height//2), self.width//2 + 2)
        pygame.draw.circle(surface, (255, 100, 0), (rx + self.width//2, ry + self.height//2), self.width//2)
        pygame.draw.circle(surface, (255, 255, 255), (rx + self.width//2, ry + self.height//2), self.width//2 - 4)


class Batarang(BaseProjectile):
    def __init__(self, x, y, target_x, target_y):
        super().__init__(x, y, target_x, target_y, speed=7.5, damage=10, lifetime=2.0)
        self.width = 14
        self.height = 14
        self.rotation = 0

    def update(self, dt):
        super().update(dt)
        self.rotation = (self.rotation + 20) % 360

    def draw(self, surface, camera_offset_x, camera_offset_y):
        if not self.is_active: return
        rx = int(self.x - camera_offset_x)
        ry = int(self.y - camera_offset_y)
        
        # Draw rotating cross for batarang
        surf = pygame.Surface((self.width*2, self.height*2), pygame.SRCALPHA)
        center = (self.width, self.height)
        
        # A batarang-like shape (curved or cross)
        color = (30, 30, 30)
        pygame.draw.line(surf, color, (center[0]-self.width, center[1]), (center[0]+self.width, center[1]), 3)
        pygame.draw.line(surf, color, (center[0], center[1]-self.height//2), (center[0], center[1]+self.height//2), 3)
        
        surf = pygame.transform.rotate(surf, self.rotation)
        surf_rect = surf.get_rect(center=(rx + self.width//2, ry + self.height//2))
        surface.blit(surf, surf_rect)
