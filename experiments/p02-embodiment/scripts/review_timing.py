"""Review derivatives use source tick timing; never imply new source drawings."""
from fractions import Fraction
from pathlib import Path

from PIL import Image


def review_durations(ticks: list[int], slow_factor: int = 1) -> list[int]:
    """Cumulative nearest-centisecond quantization for GIF's 10 ms timebase.

    Boundary error is at most 5 ms, rather than accumulating rounding per frame.
    The 24 Hz source is authoritative; this is only a review-format conversion.
    """
    if not ticks or slow_factor not in (1, 4):
        raise ValueError("invalid_review_timing")
    elapsed = Fraction(0)
    previous = 0
    durations = []
    for tick in ticks:
        if type(tick) is not int or tick < 1:
            raise ValueError("duration_ticks_must_be_positive_integer")
        elapsed += Fraction(tick * slow_factor * 100, 24)
        boundary = (elapsed.numerator * 2 + elapsed.denominator) // (2 * elapsed.denominator)
        durations.append((boundary - previous) * 10)
        previous = boundary
    return durations


def save_review_animation(path: Path, images: list[Image.Image], track: dict, slow_factor: int = 1,
                          backdrop_rgb: tuple[int, int, int] = (238, 238, 242)) -> dict:
    if len(backdrop_rgb) != 3 or any(type(c) is not int or not 0 <= c <= 255 for c in backdrop_rgb):
        raise ValueError("invalid_review_backdrop")
    if len(images) != len(track["frames"]):
        raise ValueError("review_frame_count_mismatch")
    completion = track["completion"]
    if completion not in ("once", "loop"):
        raise ValueError("unknown_completion")
    ticks = [frame["duration_ticks"] for frame in track["frames"]]
    durations = review_durations(ticks, slow_factor)
    options = {"loop": 0} if completion == "loop" else {}
    # Compositing onto a declared neutral review backdrop avoids GIF's binary
    # transparency destroying antialiased sprite edges. Source PNGs are untouched.
    frames = []
    for image in images:
        backdrop = Image.new("RGBA", image.size, (*backdrop_rgb, 255))
        backdrop.alpha_composite(image.convert("RGBA"))
        frames.append(backdrop.convert("RGB"))
    frames[0].save(path, format="GIF", save_all=True, append_images=frames[1:],
                   duration=durations, disposal=2, optimize=False, **options)
    return {"source_ticks": ticks, "source_fps": 24, "slow_factor": slow_factor,
            "review_duration_ms": durations, "completion": completion,
            "source_pixels_mutated": False, "gif_boundary_error_ms_max": 5,
            "backdrop_rgb": list(backdrop_rgb)}
