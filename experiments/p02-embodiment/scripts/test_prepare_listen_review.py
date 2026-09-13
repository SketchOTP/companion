import json
import tempfile
import unittest
from pathlib import Path
from prepare_listen_review import prepare

class ListenReviewTests(unittest.TestCase):
    def rejected(self, sequence, rejected, reason):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "selection.json"
            path.write_text(json.dumps({"sequence": sequence, "rejected": rejected}))
            with self.assertRaisesRegex(ValueError, reason):
                prepare(root, path)

    def frame(self, name="front", ticks=2):
        return {"drawing_id": name, "duration_ticks": ticks, "label": name}

    def test_missing_rest_endpoint(self):
        self.rejected([self.frame("other"), self.frame()], {}, "rest_endpoints_required")

    def test_zero_duration(self):
        self.rejected([self.frame(ticks=0), self.frame()], {}, "invalid_duration")

    def test_boolean_duration(self):
        self.rejected([self.frame(ticks=True), self.frame()], {}, "invalid_duration")

    def test_rejected_frame(self):
        self.rejected([self.frame(), self.frame("bad"), self.frame()], {"bad": "artifact"}, "rejected_drawing_selected")

    def test_unsafe_path(self):
        self.rejected([self.frame(), self.frame("../bad"), self.frame()], {}, "unsafe_drawing_id")

    def test_missing_source_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "selection.json"
            path.write_text(json.dumps({"sequence": [self.frame(), self.frame()], "rejected": {}}))
            with self.assertRaises(KeyError):
                prepare(root, path)
