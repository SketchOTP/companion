#!/usr/bin/env python3
"""Bind generated key studies, not a completed motion or production frame pack."""
import argparse
import hashlib
import json
from pathlib import Path

GAIT = {
    'left': ['left_contact_near_armfix', 'left_down_armfix', 'left_passing_repair2',
             'left_up_near', 'left_contact_far', 'left_down_far', 'left_passing_far', 'left_up_far'],
    'right': ['right_contact_near', 'right_down_near', 'right_passing_near', 'right_up_near',
              'right_contact_far', 'right_down_far', 'right_passing_far_repair', 'right_up_far'],
}
FACING = ['front', 'front_right', 'right_fix', 'back_right', 'back', 'back_left', 'left_fix', 'front_left']


def assemble(raw, include_left_inbetweens=False):
    tracks = []

    def add(name, sequence, ticks=6, completion='once'):
        weights = [ticks] * len(sequence) if isinstance(ticks, int) else ticks
        if len(weights) != len(sequence):
            raise ValueError('timing_length_mismatch')
        tracks.append({'id': name, 'completion': completion, 'quality': 'NOT_APPROVED',
                       'frames': [{'drawing_id': item, 'label': item, 'duration_ticks': weight}
                                  for item, weight in zip(sequence, weights)]})

    for facing in FACING:
        add('construction_' + facing, [facing], 6)
    add('front_breathe_key_study', ['front', 'breathe_peak', 'breathe_exhale', 'front'], [18, 24, 36, 18], 'loop')
    add('front_listen_acknowledge_key_study', ['front', 'listen_hold', 'acknowledge_down', 'front'], [12, 30, 18, 24])
    for side, gait in GAIT.items():
        add(side + '_gait_key_study', gait, 4, 'loop')
        outward = ['front', f'turn_{side}_out_22', 'front_' + side, f'turn_{side}_out_67', side + '_fix']
        returning = [side + '_fix', f'turn_{side}_return_67', 'front_' + side, f'turn_{side}_return_22', 'front']
        start = [side + '_fix', side + '_start_anticipation', side + '_start_liftoff', gait[0]]
        stop = [gait[0], side + '_stop_collect', side + '_stop_settle', side + '_fix']
        add(side + '_outward_turn_key_study', outward)
        add(side + '_return_turn_key_study', returning)
        add(side + '_start_key_study', start)
        add(side + '_stop_key_study', stop)
        # Explicit key-blocking study: no claim this is a finished action.
        add(side + '_complete_action_key_blocking', outward + start[1:] + gait[1:] + gait + stop + returning[1:], 5)
    if include_left_inbetweens:
        sequence = [item for index, key in enumerate(GAIT['left']) for item in (key, f'left_walk_mid_{index}')]
        add('left_inbetween_diagnostic_not_approved', sequence, 2, 'loop')
    used = sorted({frame['drawing_id'] for track in tracks for frame in track['frames']})
    drawings = []
    for name in used:
        source = raw / (name + '.png')
        drawings.append({'id': name, 'file': source.name, 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
    return {'profile': 'BLACK_BACKED_MOTION_REVIEW_V1', 'approval_state': 'candidate',
            'completion_status': 'INCOMPLETE_KEY_STUDIES', 'production_intake': 'NOT_RUN',
            'drawings': drawings, 'tracks': tracks}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--raw', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--include-left-inbetweens', action='store_true')
    args = parser.parse_args()
    result = assemble(args.raw, args.include_left_inbetweens)
    with args.out.open('x') as target:
        target.write(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'drawings': len(result['drawings']), 'studies': len(result['tracks']),
                      'completion_status': result['completion_status']}))
