from __future__ import annotations

import contextlib
import io
import unittest

import run
from experiments.registry import list_experiments


class ReleaseCLITests(unittest.TestCase):
    def test_help_lists_every_public_command(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            run.main(['help'])
        text = output.getvalue()
        for command in run.COMMANDS:
            self.assertIn(command, text)
        self.assertNotIn('ssv2', text.lower())
        self.assertNotIn('backfill.', text)

    def test_only_paper_datasets_are_exposed(self):
        self.assertFalse(any('ssv2' in name for name in run.COMMANDS | run.ALIASES))
        self.assertFalse(any('ssv2' in spec.name for spec in list_experiments()))
        self.assertFalse(any(name.startswith('backfill.') for name in run.COMMANDS))
        with self.assertRaises(SystemExit):
            run.main(['init.ssv2'])


if __name__ == '__main__':
    unittest.main()
