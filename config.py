"""
Configuration constants for GEMMA WORLD: AI Adaptive Platformer
"""
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
LEVELS_DIR = os.path.join(BASE_DIR, "levels")

# Window & Display
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "GEMMA WORLD: AI Adaptive Platformer"

# Color Palette (Curated Modern/Retro Neo-Arcade)
COLOR_BLACK = (10, 12, 18)
COLOR_WHITE = (245, 247, 250)
COLOR_DARK_BG = (15, 18, 28)

# Sky gradients
SKY_DAY_TOP = (45, 105, 225)
SKY_DAY_BOTTOM = (135, 206, 250)
SKY_NIGHT_TOP = (10, 15, 40)
SKY_NIGHT_BOTTOM = (30, 45, 85)
SKY_SUNSET_TOP = (180, 60, 90)
SKY_SUNSET_BOTTOM = (255, 160, 90)

# Environment
COLOR_GROUND = (46, 139, 87)
COLOR_DIRT = (101, 67, 33)
COLOR_PLATFORM = (70, 80, 105)
COLOR_PLATFORM_ACCENT = (110, 130, 170)
COLOR_ONEWAY_PLATFORM = (180, 160, 90)

# Characters & Entities
COLOR_NOVA = (0, 230, 240)          # Cyan energy suit
COLOR_NOVA_ACCENT = (255, 215, 0)   # Golden visor
COLOR_NOVA_SHIELD = (100, 200, 255) # Translucent aura

# Enemies
COLOR_WALKER = (180, 60, 200)       # Purple crawler
COLOR_CHASER = (255, 90, 40)        # Blazing orange stalker
COLOR_FAST = (240, 30, 80)          # Crimson runner

# Items & Collectibles
COLOR_COIN = (255, 215, 0)
COLOR_COIN_GLOW = (255, 240, 150)
COLOR_HEALTH_CRYSTAL = (50, 230, 100)
COLOR_SPEED_BOOST = (0, 180, 255)
COLOR_SHIELD = (120, 140, 255)
COLOR_MAGNET = (240, 120, 200)

# UI Elements
HUD_BG = (18, 22, 35, 210)
HUD_BORDER = (60, 80, 120)
TEXT_WHITE = (245, 247, 250)
TEXT_GOLD = (255, 215, 0)
HEALTH_RED = (235, 60, 75)
AI_ACCENT = (140, 90, 255)         # Gemma Purple

# Physics Constants
GRAVITY = 0.75
TERMINAL_VELOCITY = 15.0
PLAYER_SPEED = 5.2
PLAYER_ACCEL = 0.55
PLAYER_FRICTION = 0.82
JUMP_FORCE = -14.2
MIN_JUMP_FORCE = -5.5               # Variable height when releasing jump key

# Combat & Stats
PLAYER_MAX_HEALTH = 100
PLAYER_INITIAL_LIVES = 3
INVULNERABILITY_DURATION = 1.5      # Seconds of immunity after damage

# Power-up Durations
SPEED_BOOST_DURATION = 8.0          # Seconds
MAGNET_DURATION = 10.0
MAGNET_RADIUS = 220                 # Pixels

# AI Game Director Settings
GEMMA_DECISION_INTERVAL = 5.0       # Seconds between periodic evaluations
AI_TIMEOUT_SECONDS = 3.0            # Seconds before triggering fallback
MAX_RECENT_EVENTS = 10

# Permitted Actions for Gemma (Strict Whitelist)
ALLOWED_ACTIONS = [
    "do_nothing",
    "spawn_enemy",
    "spawn_coin",
    "spawn_powerup",
    "change_enemy_speed",
    "create_platform",
    "remove_platform",
    "change_weather",
    "increase_difficulty",
    "decrease_difficulty",
    "give_health",
    "activate_event"
]

# AI Safety Thresholds (Clamping & Bounds)
MAX_ENEMIES_TO_SPAWN = 3
MAX_SPEED_MULTIPLIER = 2.0
MIN_SPEED_MULTIPLIER = 0.5
MAX_POWERUPS_TO_SPAWN = 2
MAX_PLATFORM_CHANGES = 2
MAX_HEALTH_GIVE = 40
MIN_DIFFICULTY = 1
MAX_DIFFICULTY = 10
