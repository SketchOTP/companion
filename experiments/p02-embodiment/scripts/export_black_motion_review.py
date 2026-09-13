#!/usr/bin/env python3
"""Exact-copy black-backed studies and explicitly non-production playback.

Only review thumbnails/strips/GIFs are resized. Never creates source drawings,
in-betweens, alpha masks, anatomical repairs or transparent intake receipts.
"""
import argparse
import hashlib
import html
import json
from pathlib import Path

from PIL import Image, ImageDraw

from export_author002_failure import copy_exact
from review_timing import save_review_animation


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_name(value):
    if not value or any(c not in 'abcdefghijklmnopqrstuvwxyz0123456789_-' for c in value):
        raise ValueError('invalid_identifier')
    return value


def export(requests, raw, out):
    if requests['profile'] != 'BLACK_BACKED_MOTION_REVIEW_V1':
        raise ValueError('not_black_review_profile')
    if requests['approval_state'] != 'candidate':
        raise ValueError('review_not_approval')
    out.mkdir(parents=True, exist_ok=False)
    observed, images = {}, {}
    for row in requests['drawings']:
        name = safe_name(row['id'])
        if name in observed:
            raise ValueError('duplicate_drawing_identifier')
        source = raw / row['file']
        if Path(row['file']).name != row['file'] or digest(source) != row['sha256']:
            raise ValueError('source_identity_mismatch')
        with Image.open(source) as im:
            if im.format != 'PNG' or im.mode != 'RGB' or im.width != im.height:
                raise ValueError('not_square_opaque_rgb_png')
            w, h = im.size
            perimeter = [im.getpixel((x, y)) for y in (0, h - 1) for x in range(w)]
            perimeter += [im.getpixel((x, y)) for x in (0, w - 1) for y in range(h)]
            channel_max = max(max(pixel) for pixel in perimeter)
            if channel_max > 3:
                raise ValueError('black_review_perimeter_exceeds_3_of_255')
            if im.convert('L').getextrema()[1] < 40:
                raise ValueError('blank_drawing')
            thumb = im.copy()
            thumb.thumbnail((480, 480), Image.Resampling.LANCZOS)
        copy_exact(source, out / 'raw' / (name + '.png'))
        observed[name] = {'sha256': digest(source), 'size': [w, h], 'mode': 'RGB',
                          'perimeter_channel_max': channel_max, 'exact_copy': True}
        images[name] = thumb
    track_results = []
    (out / 'review').mkdir()
    for track in requests['tracks']:
        name = safe_name(track['id'])
        frames = []
        board = Image.new('RGB', (4 * 512, ((len(track['frames']) + 3) // 4) * 550), 'black')
        for index, frame in enumerate(track['frames']):
            drawing = images[frame['drawing_id']]
            tile = Image.new('RGB', (512, 550), 'black')
            tile.paste(drawing, ((512 - drawing.width) // 2, 8))
            label = f"{index:02} {frame['label']} | {frame['duration_ticks']} ticks"
            ImageDraw.Draw(tile).text((8, 506), label, fill='white')
            ImageDraw.Draw(tile).text((8, 527), 'CANDIDATE STUDY - contact/continuity not certified', fill='#bbbbbb')
            frames.append(tile)
            board.paste(tile, (index % 4 * 512, index // 4 * 550))
        board.save(out / 'review' / (name + '-strip.png'))
        timing = {}
        for factor, suffix in ((1, 'normal'), (4, 'quarter')):
            target = out / 'review' / f'{name}-{suffix}.gif'
            timing[suffix] = save_review_animation(target, frames, track, factor, (0, 0, 0))
            with Image.open(target) as gif:
                durations = []
                for i in range(gif.n_frames):
                    gif.seek(i)
                    durations.append(gif.info['duration'])
                if durations != timing[suffix]['review_duration_ms']:
                    raise ValueError('review_timing_readback_mismatch')
        track_results.append({'id': name, 'drawings': len(track['frames']),
                              'timing': timing, 'motion_quality': 'NOT_APPROVED'})
    facing_order = ['front', 'front_right', 'right_fix', 'back_right', 'back', 'back_left', 'left_fix', 'front_left']
    if all(name in images for name in facing_order):
        construction = Image.new('RGB', (2048, 1100), 'black')
        for index, name in enumerate(facing_order):
            construction.paste(images[name], (index % 4 * 512 + 16, index // 4 * 550 + 8))
            ImageDraw.Draw(construction).text((index % 4 * 512 + 16, index // 4 * 550 + 506), name, fill='white')
        construction.save(out / 'review' / 'eight-facing-black-study.png')
    (out / 'requests.json').write_text(json.dumps(requests, indent=2, sort_keys=True) + '\n')
    gallery = ['<!doctype html><meta charset="utf-8"><title>Black motion key studies — incomplete</title>',
               '<style>body{background:#000;color:#eee;font:18px sans-serif;margin:2rem}a{color:#bf9bff}img{max-width:480px}section{margin:3rem 0}</style>',
               '<h1>Black-background motion studies — INCOMPLETE</h1>',
               '<p>Candidate and rejected studies, not finished animation or an approval request. ',
               'Raw source bytes are preserved. No contacts, anatomy or motion-quality pass is implied.</p>']
    for track in track_results:
        name = track['id']
        gallery.append(f'<section><h2>{html.escape(name)}</h2><img src="review/{name}-normal.gif" alt="normal key study"> '
                       f'<img src="review/{name}-quarter.gif" alt="quarter-speed key study"><p>'
                       f'<a href="review/{name}-strip.png">Ordered frame strip</a></p></section>')
    (out / 'index.html').write_text('\n'.join(gallery) + '\n')
    result = {'profile': requests['profile'], 'status': 'CANDIDATE_REVIEW_EXPORT',
              'drawings': observed, 'tracks': track_results,
              'source_pixels_modified': False, 'transparent_intake': 'NOT_RUN',
              'root_contacts': 'NOT_RUN', 'operator_motion_approval': 'NOT_RUN',
              'files': {p.relative_to(out).as_posix(): digest(p)
                        for p in sorted(out.rglob('*')) if p.is_file()}}
    (out / 'result.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--requests', type=Path, required=True)
    parser.add_argument('--raw', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = export(json.loads(args.requests.read_text()), args.raw, args.out)
    print(json.dumps({'status': result['status'], 'drawings': len(result['drawings']),
                      'tracks': len(result['tracks']), 'result_sha256': digest(args.out / 'result.json')}))
