"""
Asset Factory for GEMMA WORLD
Procedurally generates high-quality, original retro neo-arcade sprites
for Nova, enemies, tiles, and power-up items.
"""
import pygame
from config import (
    COLOR_NOVA, COLOR_NOVA_ACCENT, COLOR_NOVA_SHIELD,
    COLOR_WALKER, COLOR_CHASER, COLOR_FAST,
    COLOR_COIN, COLOR_COIN_GLOW,
    COLOR_HEALTH_CRYSTAL, COLOR_SPEED_BOOST, COLOR_SHIELD, COLOR_MAGNET,
    COLOR_GROUND, COLOR_DIRT, COLOR_PLATFORM, COLOR_PLATFORM_ACCENT,
    COLOR_ONEWAY_PLATFORM, COLOR_WHITE, COLOR_BLACK
)

def create_nova_surface(width=40, height=52, facing_right=True, state="idle", frame_tick=0):
    """
    Generates procedural sprite for original protagonist Nova:
    A high-tech cyber explorer with cyan energy suit and golden visor.
    """
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Body bobbing for idle/run
    bob = 0
    if state == "run":
        bob = (frame_tick // 4) % 3
    elif state == "jump":
        bob = -2

    # Outer Energy Aura / Suit Body
    body_rect = pygame.Rect(8, 14 + bob, 24, 28)
    pygame.draw.rect(surf, COLOR_NOVA, body_rect, border_radius=6)
    
    # Cyber Chest Armor
    chest_rect = pygame.Rect(12, 18 + bob, 16, 14)
    pygame.draw.rect(surf, (20, 60, 90), chest_rect, border_radius=3)
    # Energy Core (Pulse)
    pulse_val = 180 + (frame_tick * 8) % 75
    pygame.draw.circle(surf, (pulse_val, 255, 255), (20, 25 + bob), 4)

    # Helmet
    helmet_rect = pygame.Rect(10, 4 + bob, 20, 16)
    pygame.draw.rect(surf, (20, 35, 55), helmet_rect, border_radius=5)
    
    # Visor (Golden neon visor)
    if facing_right:
        visor_rect = pygame.Rect(18, 9 + bob, 12, 6)
    else:
        visor_rect = pygame.Rect(10, 9 + bob, 12, 6)
    pygame.draw.rect(surf, COLOR_NOVA_ACCENT, visor_rect, border_radius=2)

    # Feet / Thrusters
    leg_l = pygame.Rect(10, 42 + bob, 8, 8)
    leg_r = pygame.Rect(22, 42 + bob, 8, 8)
    pygame.draw.rect(surf, (30, 40, 60), leg_l, border_radius=2)
    pygame.draw.rect(surf, (30, 40, 60), leg_r, border_radius=2)

    return surf

def create_enemy_surface(enemy_type="walker", width=40, height=40, frame_tick=0):
    """Generates procedural sprite for original enemies."""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    
    if enemy_type == "walker":
        # Purple bio-mechanical crawler with spiked armor
        pygame.draw.ellipse(surf, COLOR_WALKER, (4, 10, 32, 26))
        pygame.draw.ellipse(surf, (110, 30, 130), (8, 14, 24, 18))
        # Glowing eye
        eye_x = 26 if (frame_tick // 15) % 2 == 0 else 24
        pygame.draw.circle(surf, (255, 240, 80), (eye_x, 22), 4)
        pygame.draw.circle(surf, (20, 20, 20), (eye_x + 1, 22), 2)
        # Antenna / spikes
        pygame.draw.line(surf, COLOR_WALKER, (12, 10), (8, 2), 2)
        pygame.draw.line(surf, COLOR_WALKER, (28, 10), (32, 2), 2)

    elif enemy_type == "chaser":
        # Blazing orange angular stalker drone
        pts = [(20, 4), (36, 32), (20, 26), (4, 32)]
        pygame.draw.polygon(surf, COLOR_CHASER, pts)
        pygame.draw.polygon(surf, (255, 180, 50), [(20, 10), (30, 28), (20, 24), (10, 28)])
        # Heat thruster flame
        flame_len = 30 + (frame_tick * 4) % 8
        pygame.draw.line(surf, (255, 255, 100), (20, 26), (20, flame_len), 3)

    elif enemy_type == "fast":
        # Aerodynamic Crimson hover-blade
        pygame.draw.ellipse(surf, COLOR_FAST, (2, 12, 36, 16))
        pygame.draw.line(surf, (255, 120, 150), (2, 20), (38, 20), 2)
        # Razor tip
        pygame.draw.polygon(surf, (255, 220, 230), [(38, 20), (30, 14), (30, 26)])

    return surf

def create_item_surface(item_type="coin", size=28, frame_tick=0):
    """Generates procedural sprite for collectibles and power-ups."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size // 2
    
    if item_type == "coin":
        # Rotating golden coin
        scale_x = abs(round(size * 0.4 * abs(((frame_tick % 30) - 15) / 15.0))) + 4
        rect = pygame.Rect(center - scale_x, 3, scale_x * 2, size - 6)
        pygame.draw.ellipse(surf, COLOR_COIN, rect)
        pygame.draw.ellipse(surf, COLOR_COIN_GLOW, (center - scale_x + 2, 5, max(1, scale_x * 2 - 4), size - 10))

    elif item_type == "health_crystal":
        # Green rhomboid health crystal
        pts = [(center, 2), (size - 4, center), (center, size - 2), (4, center)]
        pygame.draw.polygon(surf, COLOR_HEALTH_CRYSTAL, pts)
        inner_pts = [(center, 6), (size - 8, center), (center, size - 6), (8, center)]
        pygame.draw.polygon(surf, (180, 255, 210), inner_pts)

    elif item_type == "speed_boost":
        # Cyan lightning bolt
        pts = [(16, 2), (6, 15), (14, 15), (10, 26), (22, 12), (15, 12)]
        pygame.draw.polygon(surf, COLOR_SPEED_BOOST, pts)
        pygame.draw.lines(surf, COLOR_WHITE, False, pts, 1)

    elif item_type == "shield":
        # Cobalt crest shield
        pts = [(center, 2), (size - 3, 7), (size - 5, 20), (center, size - 2), (5, 20), (3, 7)]
        pygame.draw.polygon(surf, COLOR_SHIELD, pts)
        pygame.draw.lines(surf, (200, 220, 255), True, pts, 2)

    elif item_type == "magnet":
        # Horseshoe magnet
        rect = pygame.Rect(4, 4, size - 8, size - 8)
        pygame.draw.arc(surf, COLOR_MAGNET, rect, 0, 3.14, 6)
        pygame.draw.rect(surf, (240, 240, 240), (4, center, 6, 8))
        pygame.draw.rect(surf, (240, 240, 240), (size - 10, center, 6, 8))

    return surf

def create_platform_surface(width, height, platform_type="solid"):
    """Generates procedural platform tiles."""
    surf = pygame.Surface((width, height), pygame.SRCALPHA)
    
    if platform_type == "ground":
        # Top grass border
        pygame.draw.rect(surf, COLOR_GROUND, (0, 0, width, 10))
        # Dirt underfill with stone flecks
        pygame.draw.rect(surf, COLOR_DIRT, (0, 10, width, height - 10))
        # Subtle texture lines
        for x in range(12, width, 32):
            pygame.draw.rect(surf, (80, 50, 25), (x, 14, 8, 6), border_radius=2)

    elif platform_type == "floating":
        # Tech-metal floating platform
        pygame.draw.rect(surf, COLOR_PLATFORM, (0, 0, width, height), border_radius=4)
        pygame.draw.rect(surf, COLOR_PLATFORM_ACCENT, (0, 0, width, 4), border_top_left_radius=4, border_top_right_radius=4)
        pygame.draw.rect(surf, (40, 50, 70), (0, 0, width, height), width=2, border_radius=4)

    elif platform_type == "oneway":
        # Golden semi-permeable beam
        pygame.draw.rect(surf, COLOR_ONEWAY_PLATFORM, (0, 0, width, height), border_radius=3)
        for x in range(0, width, 16):
            pygame.draw.line(surf, (240, 225, 140), (x, 0), (x + 8, height), 2)

    return surf
