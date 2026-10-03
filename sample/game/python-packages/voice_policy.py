"""Offline short-utterance scheduler; no service clients or network access."""
import unicodedata
import math


def allow_density(index, density=0.5):
    """Keep a deterministic share of otherwise playable voice opportunities."""
    density = max(0.0, min(1.0, density))
    return math.floor((index + 1) * density) > math.floor(index * density)


def opportunities(text, cps):
    """Times for 4th, then every 16th alphanumeric; punctuation consumes display time."""
    if cps <= 0:
        return []
    count = 0
    out = []
    for position, char in enumerate(unicodedata.normalize('NFC', text), 1):
        if char.isalnum():
            count += 1
            if count >= 4 and (count - 4) % 16 == 0:
                out.append(position / cps)
    return out


class Pulse:
    def __init__(self, text, cps, enabled=True):
        self.times = opportunities(text, cps) if enabled else []
        self.index = 0
        self.count = 0
        self.last = -100.0
        self.stopped = False

    def stop(self):
        self.stopped = True

    def tick(self, elapsed):
        if self.stopped or self.count >= 3:
            return False
        due = None
        while self.index < len(self.times) and self.times[self.index] <= elapsed:
            due = self.times[self.index]
            self.index += 1
        # Never catch up stale audio after menu, a stalled frame, or a fast reveal.
        if due is None or elapsed - due > 0.15 or elapsed - self.last < 1.2:
            return False
        self.last = elapsed
        self.count += 1
        return True


def choose_clip(pool, previous, chooser):
    candidates = [p for p in pool if p != previous]
    return chooser(candidates) if candidates else None
