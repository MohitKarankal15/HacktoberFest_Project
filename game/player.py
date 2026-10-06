"""
Player Controller for Nova
Protagonist in GEMMA WORLD: AI Adaptive Platformer
"""
import pygame
from config import (
    PLAYER_SPEED, PLAYER_ACCEL, PLAYER_FRICTION, GRAVITY,
    TERMINAL_VELOCITY, JUMP_FORCE, MIN_JUMP_FORCE,
    PLAYER_MAX_HEALTH, PLAYER_INITIAL_LIVES, INVULNERABILITY_DURATION,
    SPEED_BOOST_DURATION, MAGNET_DURATION, COLOR_NOVA_SHIELD
)
from game.asset_factory import create_nova_surface

class Player:
    def __init__(self, x, y):
        self.spawn_x = x
        self.spawn_y = y
        self.width = 40
        self.height = 52

        # Physics
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.is_grounded = False
        self.facing_right = True

        # Stats
        self.max_health = PLAYER_MAX_HEALTH
        self.health = self.max_health
        self.lives = PLAYER_INITIAL_LIVES
        self.coins = 0
        self.score = 0
        self.is_dead = False

        # Status & Power-ups
        self.invulnerable_timer = 0.0
        self.has_shield = False
        self.speed_boost_timer = 0.0
        self.magnet_timer = 0.0

        # Animation state
        self.anim_tick = 0
        self.state = "idle"  # idle, run, jump, hurt
        
        # Trail effects for speed boost
        self.trails = []  # [(x, y, alpha, facing_right)]

    @property
    def rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def handle_input(self, keys):
        """Processes keyboard input for Nova."""
        move_dir = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move_dir -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move_dir += 1

        # Calculate max speed with potential power-up
        current_speed = PLAYER_SPEED * (1.5 if self.speed_boost_timer > 0 else 1.0)

        if move_dir != 0:
            self.vx += move_dir * PLAYER_ACCEL
            # Clamp to max speed
            if self.vx > current_speed:
                self.vx = current_speed
            elif self.vx < -current_speed:
                self.vx = -current_speed
            self.facing_right = (move_dir > 0)
        else:
            # Apply friction when no input
            self.vx *= PLAYER_FRICTION
            if abs(self.vx) < 0.1:
                self.vx = 0.0

    def jump(self):
        """Initiates jump if grounded."""
        if self.is_grounded:
            self.vy = JUMP_FORCE
            self.is_grounded = False
            return True
        return False

    def cut_jump(self):
        """Shortens jump if key released early for variable height."""
        if self.vy < MIN_JUMP_FORCE:
            self.vy = MIN_JUMP_FORCE

    def apply_gravity(self):
        """Applies downward gravitational acceleration."""
        self.vy += GRAVITY
        if self.vy > TERMINAL_VELOCITY:
            self.vy = TERMINAL_VELOCITY

    def update(self, dt):
        """Updates timers, state, and animation frames."""
        self.anim_tick += 1

        # Power-up timers
        if self.speed_boost_timer > 0:
            self.speed_boost_timer = max(0.0, self.speed_boost_timer - dt)
            # Record trail
            if self.anim_tick % 3 == 0 and abs(self.vx) > 1.0:
                self.trails.append([self.x, self.y, 160, self.facing_right])

        if self.magnet_timer > 0:
            self.magnet_timer = max(0.0, self.magnet_timer - dt)

        # Decay trails
        for trail in self.trails:
            trail[2] -= 15  # Alpha decrease
        self.trails = [t for t in self.trails if t[2] > 0]

        # Invulnerability timer
        if self.invulnerable_timer > 0:
            self.invulnerable_timer = max(0.0, self.invulnerable_timer - dt)

        # Determine animation state
        if not self.is_grounded:
            self.state = "jump"
        elif abs(self.vx) > 0.4:
            self.state = "run"
        else:
            self.state = "idle"

    def take_damage(self, amount):
        """Damages player, taking shield into account."""
        if self.invulnerable_timer > 0:
            return False  # Protected by i-frames

        if self.has_shield:
            self.has_shield = False
            self.invulnerable_timer = INVULNERABILITY_DURATION
            return "shield_absorbed"

        self.health -= amount
        self.invulnerable_timer = INVULNERABILITY_DURATION
        
        if self.health <= 0:
            self.health = 0
            self.die()
            return "died"
        return "hurt"

    def die(self):
        """Handles player death and life deduction."""
        self.lives -= 1
        self.is_dead = True
        if self.lives > 0:
            self.respawn()

    def respawn(self):
        """Respawns Nova at spawn position."""
        self.x = float(self.spawn_x)
        self.y = float(self.spawn_y)
        self.vx = 0.0
        self.vy = 0.0
        self.health = self.max_health
        self.is_dead = False
        self.invulnerable_timer = INVULNERABILITY_DURATION * 1.5
        self.has_shield = False
        self.speed_boost_timer = 0.0
        self.magnet_timer = 0.0

    def heal(self, amount):
        """Restores health capped at maximum."""
        self.health = min(self.max_health, self.health + amount)

    def add_coins(self, count=1):
        """Adds coins and updates score."""
        self.coins += count
        self.score += count * 50

    def activate_powerup(self, powerup_type):
        """Applies a power-up effect."""
        if powerup_type == "health_crystal":
            self.heal(35)
            self.score += 100
        elif powerup_type == "speed_boost":
            self.speed_boost_timer = SPEED_BOOST_DURATION
            self.score += 100
        elif powerup_type == "shield":
            self.has_shield = True
            self.score += 100
        elif powerup_type == "magnet":
            self.magnet_timer = MAGNET_DURATION
            self.score += 100

    def draw(self, surface, camera_offset_x=0, camera_offset_y=0):
        """Renders Nova and visual status effects with camera offset."""
        render_x = int(self.x - camera_offset_x)
        render_y = int(self.y - camera_offset_y)

        # Draw speed boost ghost trails
        for tx, ty, alpha, tfacing in self.trails:
            trail_surf = create_nova_surface(self.width, self.height, tfacing, "run", 0)
            trail_surf.set_alpha(max(0, int(alpha)))
            surface.blit(trail_surf, (int(tx - camera_offset_x), int(ty - camera_offset_y)))

        # Invulnerability flicker (skip rendering every 4th frame)
        if self.invulnerable_timer > 0 and (self.anim_tick // 4) % 2 == 0:
            return

        # Main character sprite
        sprite = create_nova_surface(
            self.width, self.height, self.facing_right, self.state, self.anim_tick
        )
        surface.blit(sprite, (render_x, render_y))

        # Shield energy barrier bubble
        if self.has_shield:
            shield_surf = pygame.Surface((self.width + 16, self.height + 16), pygame.SRCALPHA)
            pygame.draw.ellipse(
                shield_surf,
                (100, 200, 255, 110),
                (0, 0, self.width + 16, self.height + 16)
            )
            pygame.draw.ellipse(
                shield_surf,
                (200, 240, 255, 200),
                (0, 0, self.width + 16, self.height + 16),
                width=2
            )
            surface.blit(shield_surf, (render_x - 8, render_y - 8))
