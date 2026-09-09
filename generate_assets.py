"""Regenerate the procedural image and audio assets used by the project.

The assets shipped in assets/ were produced by this script. Running it again
recreates them from scratch, so the repository can be rebuilt on any machine.
"""

import math
import struct
import sys
import wave
from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:  # pragma: no cover
    print("Pillow is required: pip install Pillow")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def make_gradient(path: Path, width: int, height: int, seed: int) -> None:
    """Write a smooth two-tone gradient image."""
    image = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(image)
    for y in range(height):
        ratio = y / max(1, height - 1)
        red = int(40 + 180 * ratio) % 256
        green = int(90 + seed * 7 + 120 * (1 - ratio)) % 256
        blue = int(120 + seed * 3 + 90 * ratio) % 256
        draw.line([(0, y), (width, y)], fill=(red, green, blue))
    image.save(path, "PNG")


def make_tone(path: Path, frequency: float, seconds: float = 1.0,
              rate: int = 44100) -> None:
    """Write a short sine-wave sound effect as a WAV file."""
    frames = bytearray()
    total = int(rate * seconds)
    for index in range(total):
        envelope = 1.0 - index / total
        value = math.sin(2 * math.pi * frequency * index / rate) * envelope
        frames += struct.pack("<h", int(value * 32000))
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(rate)
        handle.writeframes(bytes(frames))


def main() -> int:
    (ASSETS / "images" / "backgrounds").mkdir(parents=True, exist_ok=True)
    (ASSETS / "audio").mkdir(parents=True, exist_ok=True)
    for index in range(4):
        make_gradient(
            ASSETS / "images" / "backgrounds" / f"background_{index:02d}.png",
            1280, 720, index,
        )
    for name, freq in (("correct", 880.0), ("wrong", 220.0), ("finish", 660.0)):
        make_tone(ASSETS / "audio" / f"{name}.wav", freq)
    print("Assets regenerated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
