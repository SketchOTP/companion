#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path
from compile_black_review import compose, load_bundle, sha, validate

class ReviewCompilationTests(unittest.TestCase):
    def fixture(self, root):
        (root / "raw").mkdir()
        p=root / "raw/a.png"
        p.write_bytes(b"hash-validation-fixture-not-art")
        req={"drawings":[{"id":"a","file":"a.png","sha256":sha(p)}],
             "tracks":[{"id":"t","completion":"once","frames":[{"drawing_id":"a","label":"a","duration_ticks":2}]}]}
        (root / "requests.json").write_text(json.dumps(req))
        return req

    def test_preserves_bytes_and_ticks(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);source=root/"source";source.mkdir();self.fixture(source)
            out=root/"out";(out/"raw").mkdir(parents=True)
            assets, tracks=load_bundle(source,"x",out)
            self.assertEqual((source/"raw/a.png").read_bytes(),(out/"raw/x_a.png").read_bytes())
            self.assertEqual(tracks[0]["frames"][0]["ticks"],2)
            self.assertEqual(assets["x_a"]["sha256"],sha(source/"raw/a.png"))

    def test_tampered_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root);(root/"raw/a.png").write_bytes(b"tamper")
            with self.assertRaisesRegex(ValueError,"source_hash_mismatch"):load_bundle(root,"x",root)

    def test_missing_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);self.fixture(root);(root/"raw/a.png").unlink()
            with self.assertRaises(FileNotFoundError):load_bundle(root,"x",root)

    def test_unsafe_source_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);r=self.fixture(root);r["drawings"][0]["file"]="../a.png"
            (root/"requests.json").write_text(json.dumps(r))
            with self.assertRaisesRegex(ValueError,"unsafe_source_path"):load_bundle(root,"x",root)

    def test_composition_preserves_order_and_holds(self):
        p={"title":"Walk","frames":[{"asset":"a","ticks":2,"label":"contact"},{"asset":"b","ticks":4,"label":"passing"}]}
        t=compose("full","Full",[p,p])
        self.assertEqual([f["asset"] for f in t["frames"]],["a","b","a","b"])
        self.assertEqual(sum(f["ticks"] for f in t["frames"]),12)
        self.assertEqual(t["completion"],"once")

if __name__=="__main__":unittest.main()
