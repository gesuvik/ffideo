#!/usr/bin/env python3
"""Regression tests for FFideo's zero-dependency site checker."""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class SiteCheckerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="ffideo-site-test-", dir=os.environ.get("TMPDIR"))
        self.site = Path(self.temp_dir.name) / "site"
        shutil.copytree(ROOT, self.site, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def run_check(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python3", "scripts/check_site.py", *args],
            cwd=self.site,
            text=True,
            capture_output=True,
            timeout=30,
        )

    def replace(self, relative_path: str, old: str, new: str) -> None:
        path = self.site / relative_path
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding="utf-8")

    def test_baseline_passes(self) -> None:
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unknown_placeholder_fails(self) -> None:
        self.replace("success.html", "Purchase complete", "Purchase __UNKNOWN_VALUE__ complete")
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Placeholders must be limited", result.stdout)

    def test_missing_local_link_fails(self) -> None:
        self.replace("success.html", 'href="install.html"', 'href="missing-install.html"')
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing local target", result.stdout)

    def test_placeholder_checkout_requires_static_disabled_state(self) -> None:
        self.replace("index.html", ' aria-disabled="true"', "")
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must be statically aria-disabled", result.stdout)

    def test_placeholder_checkout_is_removed_from_tab_order(self) -> None:
        self.replace("index.html", ' tabindex="-1"', "")
        result = self.run_check()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("must use tabindex=-1", result.stdout)

    def test_live_checkout_url_passes(self) -> None:
        self.replace("assets/config.js", "__CHECKOUT_URL__", "https://example.lemonsqueezy.com/buy/example")
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_external_check_rejects_private_https_url(self) -> None:
        self.replace(
            "assets/config.js",
            '  checkoutUrl: "__CHECKOUT_URL__"',
            '  checkoutUrl: "__CHECKOUT_URL__",\n  brokenUrl: "https://127.0.0.1:1/unreachable"',
        )
        result = self.run_check("--check-external")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unsafe external URL", result.stdout)


if __name__ == "__main__":
    unittest.main()
