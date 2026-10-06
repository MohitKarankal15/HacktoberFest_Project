"""
Procedural Retro Neo-Arcade Sound Effects for GEMMA WORLD
Synthesizes 8-bit sound effects dynamically in memory without external audio file dependencies.
Fails gracefully if no audio device is connected.
"""
import math
import struct
import pygame

class SoundManager:
    def __init__(self):
        self.enabled = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.enabled = True
            self.sounds = {
                "jump": self._generate_tone_slide(280, 560, 0.12),
                "coin": self._generate_two_tone(980, 1310, 0.08),
                "stomp": self._generate_tone_slide(350, 100, 0.15),
                "hurt": self._generate_tone_slide(420, 140, 0.22),
                "powerup": self._generate_arpeggio([440, 554, 659, 880], 0.06),
                "ai_pulse": self._generate_tone_slide(600, 900, 0.18)
            }
        except Exception:
            self.enabled = False
            self.sounds = {}

    def play(self, sound_name):
        """Plays sound effect if audio subsystem is active."""
        if not self.enabled:
            return
        snd = self.sounds.get(sound_name)
        if snd:
            try:
                snd.play()
            except Exception:
                pass

    def _generate_tone_slide(self, start_freq, end_freq, duration, sample_rate=22050):
        """Generates a frequency slide tone."""
        total_samples = int(sample_rate * duration)
        buf = bytearray()
        for i in range(total_samples):
            t = i / total_samples
            freq = start_freq + (end_freq - start_freq) * t
            val = int(math.sin(2.0 * math.pi * freq * (i / sample_rate)) * 16000 * (1.0 - t))
            packed = struct.pack("<hh", val, val)
            buf.extend(packed)
        return pygame.mixer.Sound(buffer=bytes(buf))

    def _generate_two_tone(self, freq1, freq2, tone_dur, sample_rate=22050):
        """Generates bright coin pickup chime."""
        samples_per_tone = int(sample_rate * tone_dur)
        buf = bytearray()
        for freq in (freq1, freq2):
            for i in range(samples_per_tone):
                t = i / samples_per_tone
                val = int(math.sin(2.0 * math.pi * freq * (i / sample_rate)) * 14000 * (1.0 - (t * 0.5)))
                packed = struct.pack("<hh", val, val)
                buf.extend(packed)
        return pygame.mixer.Sound(buffer=bytes(buf))

    def _generate_arpeggio(self, freqs, step_dur, sample_rate=22050):
        """Generates ascending power-up arpeggio."""
        buf = bytearray()
        samples_per_step = int(sample_rate * step_dur)
        for freq in freqs:
            for i in range(samples_per_step):
                val = int(math.sin(2.0 * math.pi * freq * (i / sample_rate)) * 13000)
                packed = struct.pack("<hh", val, val)
                buf.extend(packed)
        return pygame.mixer.Sound(buffer=bytes(buf))
