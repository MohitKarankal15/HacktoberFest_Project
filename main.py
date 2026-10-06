"""
GEMMA WORLD: AI ADAPTIVE PLATFORMER
Main Launch Entry Point
"""
import sys
from game.game_engine import GameEngine

def main():
    engine = GameEngine()
    engine.run()

if __name__ == "__main__":
    main()
