import tempfile
import unittest
from fractions import Fraction
from pathlib import Path

from PIL import Image

from review_timing import review_durations, save_review_animation


class ReviewTimingTests(unittest.TestCase):
    def test_tick_timing_not_fixed_frame_delay(self):
        self.assertEqual(review_durations([1, 2, 6, 24]), [40, 90, 250, 1000])

    def test_quarter_speed(self):
        self.assertEqual(review_durations([6] * 16, 4), [1000] * 16)

    def test_no_accumulated_rounding(self):
        for factor in (1, 4):
            durations = review_durations([1, 2, 3] * 100, factor)
            for n in range(1, len(durations) + 1):
                exact = Fraction(sum(([1, 2, 3] * 100)[:n]) * 1000 * factor, 24)
                self.assertLessEqual(abs(sum(durations[:n]) - exact), 5)

    def test_once_does_not_loop_and_source_unchanged(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "once.gif"
            frames = [Image.new("RGBA", (16, 16), color) for color in ("red", "blue")]
            before = [image.tobytes() for image in frames]
            save_review_animation(path, frames, {"completion": "once", "frames": [{"duration_ticks": 6}, {"duration_ticks": 12}]})
            with Image.open(path) as animation:
                self.assertNotIn("loop", animation.info)
                self.assertEqual(animation.info["duration"], 250)
                animation.seek(1)
                self.assertEqual(animation.info["duration"], 500)
            self.assertEqual(before, [image.tobytes() for image in frames])

    def test_loop_explicit(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "loop.gif"
            save_review_animation(path, [Image.new("RGBA", (16, 16), "red")], {"completion": "loop", "frames": [{"duration_ticks": 2}]})
            with Image.open(path) as animation:
                self.assertEqual(animation.info["loop"], 0)

    def test_invalid_timing_fails(self):
        for ticks in ([], [0], [-1], [1.2], [True]):
            with self.assertRaises(ValueError):
                review_durations(ticks)

    def test_explicit_black_review_backdrop(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'black.gif'
            image = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
            image.putpixel((8, 8), (128, 40, 240, 255))
            result = save_review_animation(path, [image], {'completion': 'once', 'frames': [{'duration_ticks': 6}]}, backdrop_rgb=(0, 0, 0))
            self.assertEqual(result['backdrop_rgb'], [0, 0, 0])
            with Image.open(path) as gif:
                self.assertEqual(gif.convert('RGB').getpixel((0, 0)), (0, 0, 0))
            self.assertEqual(image.getpixel((0, 0)), (0, 0, 0, 0))

    def test_invalid_backdrop_fails(self):
        for value in ((0, 0), (0, 0, 256), (True, 0, 0)):
            with self.assertRaises(ValueError):
                save_review_animation(Path('unused'), [], {}, backdrop_rgb=value)


if __name__ == "__main__":
    unittest.main()
