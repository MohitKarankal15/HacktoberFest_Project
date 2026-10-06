"""
Headless Smoke Test for GEMMA WORLD
Verifies that GameEngine initializes, runs game loop frames, handles physics,
processes AI updates, renders to surfaces, toggles debug panel, and triggers F4 demo
without throwing any runtime exceptions.
"""
import os
# Force software/dummy SDL audio and video for automated CI/smoke testing
os.environ["SDL_VIDEODRIVER"] = "dummy"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from game.game_engine import GameEngine

def run_smoke_test():
    print("Initializing GameEngine in headless mode...")
    engine = GameEngine()
    
    # 1. Start game state
    engine.state = "playing"
    print("Testing 60 frames of gameplay...")
    
    for frame in range(60):
        dt = 1.0 / 60.0
        engine.update(dt)
        engine.draw()

    print("Testing F3 debug overlay toggle...")
    engine.show_debug_panel = True
    engine.draw()

    print("Testing F4 Rogue AI Decision simulation...")
    engine.gemma_brain.trigger_bad_decision_demo()
    
    # Run another 20 frames to process the rogue AI decision through the validator and executor
    for frame in range(20):
        dt = 1.0 / 60.0
        engine.update(dt)
        engine.draw()

    # Verify decision was caught and rejected
    last_status = engine.gemma_brain.last_validation_status
    print(f"Rogue decision validation status: {last_status}")
    assert last_status == "REJECTED", f"Expected REJECTED but got {last_status}"

    print("Stopping background AI thread...")
    engine.gemma_brain.is_running = False
    
    print("SMOKE TEST COMPLETED SUCCESSFULLY! ALL SYSTEMS NOMINAL.")

if __name__ == "__main__":
    run_smoke_test()
