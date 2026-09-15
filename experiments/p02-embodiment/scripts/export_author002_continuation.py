#!/usr/bin/env python3
"""Preserve continuation studies and diagnostic key playback, never a source pack."""
import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw

from export_author002_failure import copy_exact
from review_timing import save_review_animation


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--requests', type=Path, required=True)
    ap.add_argument('--selection', type=Path, required=True)
    ap.add_argument('--raw', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    request = json.loads(args.requests.read_text())
    selected = json.loads(args.selection.read_text())
    # Approval evidence is immutable, not regenerated from new visual judgments.
    for item in selected['selected']:
        if digest(args.raw / item['file']) != item['sha256']:
            raise ValueError('approved_source_hash_changed:' + item['id'])
    args.out.mkdir(parents=True, exist_ok=False)
    observations = []
    lookup = {row['id']: row for row in selected['selected']}
    for row in request['studies']:
        source = args.raw / row['file']
        destination = args.out / 'raw' / (row['id'] + '.png')
        copy_exact(source, destination)
        with Image.open(source) as im:
            observations.append({'id': row['id'], 'file': row['file'],
                'sha256': digest(source), 'size': list(im.size), 'mode': im.mode,
                'has_alpha': 'A' in im.getbands(), 'exact_copy': True,
                'approval_state': row['approval_state']})
        lookup[row['id']] = row
    # Diagnostic only: coarse keys, not authored in-betweens or normalized motion.
    order = ['right_contact_near', 'right_down_near', 'right_passing_near',
             'right_up_near', 'right_contact_far', 'right_down_far',
             'right_passing_far_repair', 'right_up_far']
    board = Image.new('RGB', (1600, 920), '#eeeeef')
    draw = ImageDraw.Draw(board)
    draw.text((12, 8), 'RIGHT PROFILE KEY STUDY - RAW BACKGROUNDS / NO CONTACT OR SMOOTH-MOTION PASS', fill='black')
    frames = []
    for index, name in enumerate(order):
        row = lookup[name]
        source = args.raw / row['file']
        copy_exact(source, args.out / 'ordered-keys' / (str(index).zfill(2) + '-' + name + '.png'))
        with Image.open(source) as im:
            thumb = im.convert('RGBA')
            thumb.thumbnail((380, 395), Image.Resampling.LANCZOS)
        x, y = index % 4 * 400, index // 4 * 440 + 35
        board.paste(thumb, (x, y), thumb)
        draw.text((x + 8, y + 402), str(index) + ': ' + name, fill='black')
        frame = Image.new('RGBA', (512, 560), '#eeeeef')
        frame.alpha_composite(thumb, ((512 - thumb.width) // 2, 20))
        ImageDraw.Draw(frame).text((12, 525), name + ' | KEY STUDY', fill='black')
        frames.append(frame)
    board.save(args.out / 'right-key-strip.png')
    track = {'completion': 'once', 'frames': [{'duration_ticks': 6} for _ in order]}
    timing = {}
    for factor, label in [(1, 'normal'), (4, 'quarter')]:
        path = args.out / ('right-key-study-' + label + '.gif')
        timing[label] = save_review_animation(path, frames, track, factor)
        with Image.open(path) as im:
            durations = []
            for i in range(im.n_frames):
                im.seek(i)
                durations.append(im.info['duration'])
            if durations != timing[label]['review_duration_ms'] or im.info.get('loop') == 0:
                raise AssertionError('diagnostic_review_timing_mismatch')
    result = {'status': 'BLOCKED_CUTOUT_PROVIDER_HTTP_402',
        'observed_at_utc': datetime.now(timezone.utc).isoformat(),
        'basis_commit': request['basis_commit'], 'generator': request['generator'],
        'approved_source_hashes_rechecked': len(selected['selected']),
        'studies': observations, 'ordered_key_ids': order,
        'cutout_attempts': [{'id': r['id'], 'provider': 'photoroom',
            'http_status': 402, 'exit_code': 1, 'output_created': False}
            for r in request['studies'] if r['id'] != 'alpha_fallback'],
        'cutout_observation_basis': 'six live adapter tool results; no response body or credential retained',
        'fallback': {'id': 'alpha_fallback', 'result': 'FAILED_RGB_NO_ALPHA'},
        'promoted_frames': 0, 'review_timing': timing,
        'review_ceiling': 'raw key study; no cutout, normalization, contact measurement, full action, in-between or motion-quality pass',
        'downstream': {k: 'NOT RUN' for k in ['full_actions', 'v2_intake', 'v2_rust', 'v2_godot', 'world_contacts']},
        'files': {p.relative_to(args.out).as_posix(): digest(p) for p in sorted(args.out.rglob('*')) if p.is_file()}}
    (args.out / 'result.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': result['status'], 'studies': len(observations),
                      'byte_copies': 'PASSED', 'review_duration_readback': 'PASSED',
                      'result_sha256': digest(args.out / 'result.json')}))


if __name__ == '__main__':
    main()
