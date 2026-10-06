"""
Enemy System for GEMMA WORLD
Implements 3 original enemy archetypes: Walker, Chaser, Fast Enemy.
Supports dynamic speed scaling from the Gemma AI Director.
"""
import pygame
from game.asset_factory import create_enemy_surface

class Enemy:
    def __init__(self, x, y, enemy_type="walker", patrol_distance=160):
        self.x = float(x)
        self.y = float(y)
        self.start_x = float(x)
        self.enemy_type = enemy_type
        self.patrol_distance = patrol_distance
        
        self.direction = 1  # 1 = Right, -1 = Left
        self.vx = 0.0
        self.vy = 0.0
        self.is_alive = True
        self.anim_tick = 0
        self.is_grounded = False

        # Archetype configuration
        if enemy_type == "walker":
            self.width = 40
            self.height = 36
            self.base_speed = 1.6
            self.health = 1
            self.damage = 20
        elif enemy_type == "chaser":
            self.width = 38
            self.height = 38
            self.base_speed = 2.4
            self.health = 2
            self.damage = 25
            self.aggro_radius = 280
            self.is_chasing = False
        elif enemy_type == "fast":
            self.width = 42
            self.height = 28
            self.base_speed = 4.0
            self.health = 1
            self.damage = 15
        else:
            self.width = 40
            self.height = 36
            self.base_speed = 1.6
            self.health = 1
            self.damage = 20

        self.speed_multiplier = 1.0

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, dt, player, platforms):
        """Updates movement AI and platform edge detection."""
        if not self.is_alive:
            return

        self.anim_tick += 1
        effective_speed = self.base_speed * self.speed_multiplier

        if self.enemy_type == "walker":
            # Patrol back and forth around start position
            self.vx = self.direction * effective_speed
            if abs(self.x - self.start_x) > self.patrol_distance:
                self.direction *= -1
                self.x += self.direction * 2

        elif self.enemy_type == "chaser":
            # Check distance to player
            dist_x = player.x - self.x
            dist_y = player.y - self.y
            dist = (dist_x**2 + dist_y**2)**0.5

            if dist < self.aggro_radius:
                self.is_chasing = True
                self.direction = 1 if dist_x > 0 else -1
                self.vx = self.direction * (effective_speed * 1.25)
            else:
                self.is_chasing = False
                self.vx = self.direction * effective_speed
                if abs(self.x - self.start_x) > self.patrol_distance:
                    self.direction *= -1

        elif self.enemy_type == "fast":
            # Rapid back and forth
            self.vx = self.direction * effective_speed
            if abs(self.x - self.start_x) > (self.patrol_distance * 1.5):
                self.direction *= -1

        # Apply gravity
        self.vy += 0.6
        if self.vy > 12.0:
            self.vy = 12.0

        # Update X position
        self.x += self.vx

        # Check platform edge or wall collisions in X
        for p in platforms:
            if not p.is_oneway and self.rect.colliderect(p.rect):
                if self.vx > 0:
                    self.x = p.rect.left - self.width
                    self.direction = -1
                elif self.vx < 0:
                    self.x = p.rect.right
                    self.direction = 1

        # Update Y position and collision
        self.y += self.vy
        self.is_grounded = False
        for p in platforms:
            if self.rect.colliderect(p.rect):
                if self.vy > 0 and self.y + self.height - self.vy <= p.rect.top + 10:
                    self.y = p.rect.top - self.height
                    self.vy = 0
                    self.is_grounded = True

    def take_stomp(self):
        """Called when Nova jumps on top of the enemy."""
        self.health -= 1
        if self.health <= 0:
            self.is_alive = False
            return True  # Defeated
        return False  # Still alive

    def draw(self, surface, camera_offset_x=0, camera_offset_y=0):
        """Renders enemy sprite."""
        if not self.is_alive:
            return

        render_x = int(self.x - camera_offset_x)
        render_y = int(self.y - camera_offset_y)

        sprite = create_enemy_surface(
            self.enemy_type, self.width, self.height, self.anim_tick
        )
        # Flip if facing left
        if self.direction < 0:
            sprite = pygame.transform.flip(sprite, True, False)

        surface.blit(sprite, (render_x, render_y))
