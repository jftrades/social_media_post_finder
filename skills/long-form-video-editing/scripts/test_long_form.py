import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = Path(__file__).with_name("long_form.py")
SPEC = importlib.util.spec_from_file_location("long_form", MODULE_PATH)
lf = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(lf)


class LongFormContractTests(unittest.TestCase):
    def job(self):
        return {
            "project": "demo",
            "intake": {
                "level1": {"confirmed": True},
                "level2": {"confirmed": True},
                "level3": {"confirmed": True},
            },
            "segments": [{"source": "clip.mp4", "start": 0, "end": 2}],
            "output": {"width": 1920, "height": 1080, "fps": 30},
        }

    def test_valid_contract(self):
        lf.validate(self.job())

    def test_requires_each_level(self):
        job = self.job()
        job["intake"]["level2"]["confirmed"] = False
        with self.assertRaisesRegex(ValueError, "level2"):
            lf.validate(job)

    def test_atempo_supports_fast_segments(self):
        self.assertEqual(lf.atempo(5), "atempo=2,atempo=2,atempo=1.25")

    def test_rejects_invalid_segment(self):
        job = self.job()
        job["segments"][0]["end"] = 0
        with self.assertRaises(ValueError):
            lf.validate(job)


if __name__ == "__main__":
    unittest.main()
