import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

from PIL import Image

import remove_background_provider as provider


class ProviderTests(unittest.TestCase):
    def invoke(self, root, response):
        source = root / "source.png"
        Image.new("RGB", (16, 16), "white").save(source)
        credentials = root / "credentials.env"
        credentials.write_text("UNRELATED=not_read\nPHOTOROOM_API_KEY=fixture-secret\n")
        args = ["cutout", "--source", str(source), "--out", str(root / "out.png"),
                "--credentials-file", str(credentials), "--provider", "photoroom"]
        before = source.read_bytes()
        stream = io.StringIO()
        with patch("sys.argv", args), patch.object(provider.urllib.request, "urlopen", side_effect=response), contextlib.redirect_stdout(stream):
            result = provider.main()
        self.assertEqual(source.read_bytes(), before)
        self.assertNotIn("fixture-secret", stream.getvalue())
        return result, stream.getvalue()

    @staticmethod
    def response(size=(16,16), mode="RGBA", transparent=True):
        image = Image.new(mode, size, "purple")
        if transparent and mode == "RGBA":
            image.putpixel((0,0), (0,0,0,0))
        data = io.BytesIO(); image.save(data, format="PNG")
        raw = data.getvalue()
        def call(request, timeout):
            stream = io.BytesIO(raw); stream.status = 200
            return stream
        return call, raw

    def test_exact_response_bytes_and_original_preserved(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            response, raw = self.response()
            result, output = self.invoke(root, response)
            self.assertEqual(result, 0)
            self.assertEqual((root / "out.png").read_bytes(), raw)
            evidence = json.loads(output)
            self.assertTrue(evidence["dimensions_preserved"])
            self.assertNotIn("geometry_unchanged", evidence)

    def test_provider_http_failure_no_output_no_secret(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            result, output = self.invoke(root, urllib.error.HTTPError("https://example.invalid",402,"blocked",{},None))
            self.assertEqual(result, 1)
            self.assertEqual(json.loads(output)["http_status"], 402)
            self.assertFalse((root / "out.png").exists())

    def test_wrong_dimensions_or_mode_or_opaque_fail(self):
        for kwargs in ({"size": (8,8)}, {"mode": "RGB"}, {"transparent": False}):
            with self.subTest(kwargs=kwargs), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                response, _ = self.response(**kwargs)
                with self.assertRaisesRegex(SystemExit, "provider_output_contract_failed"):
                    self.invoke(root, response)
                self.assertFalse((root / "out.png").exists())


if __name__ == "__main__":
    unittest.main()
