import copy
import tempfile
import unittest
from pathlib import Path

from PIL import Image

from export_black_motion_review import digest, export


class BlackReviewTests(unittest.TestCase):
    def make_source(self, root):
        image = Image.new('RGB', (32, 32), 'black')
        image.paste((180, 40, 220), (8, 8, 24, 24))  # synthetic calibration only
        image.save(root / 'test.png')
        return {'profile': 'BLACK_BACKED_MOTION_REVIEW_V1', 'approval_state': 'candidate',
                'drawings': [{'id': 'test', 'file': 'test.png', 'sha256': digest(root / 'test.png')}],
                'tracks': [{'id': 'test', 'completion': 'once', 'frames': [
                    {'drawing_id': 'test', 'label': 'synthetic', 'duration_ticks': 6}]}]}

    def test_exact_copy_and_review(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            request = self.make_source(root)
            before = (root / 'test.png').read_bytes()
            result = export(request, root, root / 'out')
            self.assertEqual(before, (root / 'out/raw/test.png').read_bytes())
            self.assertFalse(result['source_pixels_modified'])
            self.assertEqual(result['root_contacts'], 'NOT_RUN')

    def test_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            valid = self.make_source(root)
            for index, mutation in enumerate(('hash', 'timing', 'identifier', 'approval', 'drawing')):
                value = copy.deepcopy(valid)
                if mutation == 'hash': value['drawings'][0]['sha256'] = '0' * 64
                if mutation == 'timing': value['tracks'][0]['frames'][0]['duration_ticks'] = 0
                if mutation == 'identifier': value['drawings'][0]['id'] = '../escape'
                if mutation == 'approval': value['approval_state'] = 'operator_approved'
                if mutation == 'drawing': value['tracks'][0]['frames'][0]['drawing_id'] = 'missing'
                with self.subTest(mutation=mutation), self.assertRaises((ValueError, KeyError)):
                    export(value, root, root / f'bad-{index}')


if __name__ == '__main__':
    unittest.main()
