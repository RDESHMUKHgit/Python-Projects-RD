"""
Sound effects module for Neon Pong.
Uses Windows winsound in background daemon threads for non-blocking 8-bit audio.
Gracefully falls back to silence if winsound is unavailable.
"""

import threading

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

# Global lock to avoid overlapping sound thread explosions
_sound_lock = threading.Lock()

def _beep(freq: int, duration_ms: int):
    if not HAS_WINSOUND:
        return
    try:
        winsound.Beep(int(freq), int(duration_ms))
    except Exception:
        pass

def play_async(freq: int, duration_ms: int):
    """Play a single tone asynchronously."""
    t = threading.Thread(target=_beep, args=(freq, duration_ms), daemon=True)
    t.start()

def sound_paddle_hit(rally: int = 0):
    """Rising pitch based on current rally streak."""
    # Base 650Hz, rises up to 1350Hz as rally intensifies
    freq = min(620 + rally * 35, 1400)
    play_async(freq, 35)

def sound_wall_hit():
    """Low solid thud on wall bounce."""
    play_async(340, 25)

def sound_score():
    """Exciting ascending fanfare when a player scores."""
    def fanfare():
        notes = [(440, 45), (554, 45), (659, 45), (880, 80)]
        for f, d in notes:
            _beep(f, d)
    threading.Thread(target=fanfare, daemon=True).start()

def sound_win():
    """Triumphant victory melody when a player wins the match."""
    def victory():
        melody = [
            (523, 90), (659, 90), (784, 90), (1046, 160),
            (880, 80), (1046, 260)
        ]
        for f, d in melody:
            _beep(f, d)
    threading.Thread(target=victory, daemon=True).start()

def sound_countdown(is_go: bool = False):
    """Beep during serve countdown."""
    if is_go:
        play_async(880, 70)
    else:
        play_async(440, 45)
