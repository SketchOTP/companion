#!/usr/bin/env python3
"""Read-only pixel diagnostics for the black-background retry, not art approval.

The y=880 scan intersects only the front torso in this exact 1254px study set.
It is a reproducible contour observation, not a landmark/contact certificate.
No source pixels are edited. Exit 1 means the requested inhale progression
was not observed. Anatomical leg identity still requires visual inspection.
"""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image


def observe(path):
    with Image.open(path) as im:
        if im.mode != 'RGB' or im.size != (1254, 1254):
            raise ValueError('unexpected_study_image')
        y, center = 880, 627
        def body(x):
            return max(im.getpixel((x, y))) > 32
        if not body(center):
            raise ValueError('torso_center_unobserved')
        left = right = center
        while left > 0 and body(left - 1):
            left -= 1
        while right < im.width - 1 and body(right + 1):
            right += 1
        return {'file': path.name, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                'scan_y': y, 'threshold_channel_max_gt': 32,
                'left': left, 'right': right, 'width': right - left + 1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw', type=Path, required=True)
    args = parser.parse_args()
    names = ['front'] + [f'inhale_{i}' for i in range(1, 5)] + ['breathe_peak']
    rows = [observe(args.raw / (name + '.png')) for name in names]
    widths = [r['width'] for r in rows]
    monotonic = all(a <= b for a, b in zip(widths, widths[1:]))
    result = {'status': 'PASSED' if monotonic else 'FAILED',
              'property': 'requested_inhale_torso_width_progression',
              'requested_progress_fractions': [0, 1/6, 2/6, 3/6, 4/6, 1],
              'observations': rows, 'nondecreasing_width': monotonic,
              'evidence_ceiling': 'E2_REPRODUCED_PIXEL_SCAN_ONLY',
              'anatomy_and_contact_qualification': 'NOT_RUN'}
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if monotonic else 1


if __name__ == '__main__':
    raise SystemExit(main())
