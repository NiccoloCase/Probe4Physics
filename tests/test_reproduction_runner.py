from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/reproduce_notebooks.py'


class ReproductionSafetyTests(unittest.TestCase):
    def test_source_output_directory_is_rejected_without_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'repo'
            root.mkdir()
            destination = root / 'results' / 'new-run'
            result = subprocess.run([sys.executable, str(SCRIPT), '--repo-root', str(root),
                                     '--output-dir', str(destination)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('outputs must be below output/', result.stderr)
            self.assertFalse(destination.exists())

    def test_existing_output_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / 'existing'
            destination.mkdir()
            marker = destination / 'evidence.txt'
            marker.write_text('preserve me')
            result = subprocess.run([sys.executable, str(SCRIPT), '--output-dir', str(destination)],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('already exists', result.stderr)
            self.assertEqual(marker.read_text(), 'preserve me')


if __name__ == '__main__':
    unittest.main()
