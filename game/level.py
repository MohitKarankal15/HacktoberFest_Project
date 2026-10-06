"""
Level Loader and Manager for GEMMA WORLD
Loads JSON levels, handles entity updates, checkpoints, and exit portal logic.
"""
import json
import os
import pygame
from config import LEVELS_DIR, COLOR_PLATFORM_ACCENT, COLOR_WHITE
from game.platform import Platform
from game.enemy import Enemy
from game.coin import Coin
from game.powerup import PowerUp

class Level:
    def __init__(self, level_index=1):
        self.level_index = level_index
        self.name = f"Level {level_index}"
        self.world_width = 3200
        self.world_height = 800
        self.spawn_x = 100
        self.spawn_y = 600
        self.exit_rect = pygame.Rect(3000, 550, 64, 90)
        
        self.platforms = []
        self.enemies = []
        self.coins = []
        self.powerups = []
        self.checkpoints = []  # [{'x': x, 'y': y, 'reached': False}]
        
        self.portal_tick = 0
        self.load_level(level_index)

    def load_level(self, level_index):
        """Loads level layout from levels/level<N>.json."""
        self.level_index = level_index
        file_path = os.path.join(LEVELS_DIR, f"level{level_index}.json")
        
        if not os.path.exists(file_path):
            # Fallback procedural generation if level file missing
            self._generate_fallback_level()
            return

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.name = data.get("name", f"Level {level_index}")
        self.world_width = data.get("world_width", 3600)
        self.world_height = data.get("world_height", 850)
        
        spawn = data.get("spawn", {"x": 100, "y": 600})
        self.spawn_x = spawn["x"]
        self.spawn_y = spawn["y"]

        exit_info = data.get("exit", {"x": self.world_width - 150, "y": 600, "width": 64, "height": 90})
        self.exit_rect = pygame.Rect(
            exit_info["x"], exit_info["y"], exit_info["width"], exit_info["height"]
        )

        # Platforms
        self.platforms = []
        for p in data.get("platforms", []):
            self.platforms.append(
                Platform(p["x"], p["y"], p["width"], p["height"], p.get("type", "ground"))
            )

        # Enemies
        self.enemies = []
        for e in data.get("enemies", []):
            self.enemies.append(
                Enemy(e["x"], e["y"], e.get("type", "walker"), e.get("patrol", 120))
            )

        # Coins
        self.coins = []
        for c in data.get("coins", []):
            self.coins.append(Coin(c["x"], c["y"]))

        # Power-ups
        self.powerups = []
        for pu in data.get("powerups", []):
            self.powerups.append(PowerUp(pu["x"], pu["y"], pu.get("type", "health_crystal")))

        # Checkpoints
        self.checkpoints = []
        for cp in data.get("checkpoints", []):
            self.checkpoints.append({"x": cp["x"], "y": cp["y"], "reached": False})

    def _generate_fallback_level(self):
        """Procedural fallback if JSON file is missing."""
        self.platforms = [
            Platform(0, 680, 1200, 120, "ground"),
            Platform(1350, 680, 1800, 120, "ground"),
            Platform(400, 540, 180, 24, "floating"),
            Platform(700, 460, 180, 24, "floating"),
            Platform(1500, 540, 180, 24, "floating")
        ]
        self.enemies = [Enemy(500, 640, "walker"), Enemy(1600, 640, "chaser")]
        self.coins = [Coin(450, 490), Coin(750, 410)]
        self.powerups = [PowerUp(800, 410, "health_crystal")]
        self.checkpoints = [{"x": 1400, "y": 640, "reached": False}]

    def update(self, dt, player):
        """Updates entities, checks collection and checkpoints."""
        self.portal_tick += 1

        # Update dynamic platforms
        self.platforms = [p for p in self.platforms if p.update(dt)]

        # Update enemies
        for e in self.enemies:
            e.update(dt, player, self.platforms)

        # Update coins
        for c in self.coins:
            c.update(dt, player)

        # Update powerups
        for pu in self.powerups:
            pu.update(dt)

        # Checkpoint trigger
        for cp in self.checkpoints:
            if not cp["reached"]:
                cp_rect = pygame.Rect(cp["x"], cp["y"] - 60, 40, 60)
                if player.rect.colliderect(cp_rect):
                    cp["reached"] = True
                    player.spawn_x = cp["x"]
                    player.spawn_y = cp["y"] - player.height
                    return "checkpoint_reached"

        # Check exit portal
        if player.rect.colliderect(self.exit_rect):
            return "level_complete"

        return None

    def draw(self, surface, camera_offset_x=0, camera_offset_y=0):
        """Renders level platforms, portal, checkpoints, and entities."""
        # 1. Platforms
        for p in self.platforms:
            p.draw(surface, camera_offset_x, camera_offset_y)

        # 2. Checkpoints
        for cp in self.checkpoints:
            rx = int(cp["x"] - camera_offset_x)
            ry = int(cp["y"] - camera_offset_y)
            # Pole
            pygame.draw.rect(surface, (160, 170, 190), (rx, ry - 60, 6, 60))
            # Flag / Crystal beacon
            color = (80, 255, 140) if cp["reached"] else (255, 80, 80)
            pygame.draw.polygon(surface, color, [(rx + 6, ry - 60), (rx + 30, ry - 48), (rx + 6, ry - 36)])

        # 3. Exit Gateway Portal
        ex = int(self.exit_rect.x - camera_offset_x)
        ey = int(self.exit_rect.y - camera_offset_y)
        ew = self.exit_rect.width
        eh = self.exit_rect.height

        # Portal arch
        pygame.draw.rect(surface, (60, 70, 100), (ex - 4, ey - 4, ew + 8, eh + 4), border_radius=8)
        # Swirling energy vortex
        portal_surf = pygame.Surface((ew, eh), pygame.SRCALPHA)
        pulse = 140 + int(70 * ((self.portal_tick % 40) / 40.0))
        pygame.draw.ellipse(portal_surf, (0, 200, 255, pulse), (0, 0, ew, eh))
        pygame.draw.ellipse(portal_surf, (255, 230, 120, 200), (8, 12, ew - 16, eh - 24))
        surface.blit(portal_surf, (ex, ey))

        # 4. Items and Collectibles
        for c in self.coins:
            c.draw(surface, camera_offset_x, camera_offset_y)
        for pu in self.powerups:
            pu.draw(surface, camera_offset_x, camera_offset_y)

        # 5. Enemies
        for e in self.enemies:
            e.draw(surface, camera_offset_x, camera_offset_y)
