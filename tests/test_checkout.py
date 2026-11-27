import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from tools.validate_solution import ROOT


@unittest.skipUnless(shutil.which("git"), "requires Git checkout filters")
class CheckoutPolicy(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        self.git("init", "--quiet")
        for name in (".gitignore", ".gitattributes"):
            shutil.copyfile(ROOT / name, self.repo / name)

    def git(self, *args, **kwargs):
        return subprocess.run(["git", "-c", "core.autocrlf=true", *args], cwd=self.repo,
                              capture_output=True, check=True, **kwargs)

    def test_private_packet_is_not_staged_by_git_add(self):
        guide = (ROOT / "review/README.md").read_text()
        filename = re.search(r"--init proposed > ([\w./-]+)", guide)[1]
        packet = self.repo / filename
        packet.parent.mkdir(parents=True, exist_ok=True)
        packet.write_text("{}")
        example = "review/examples/proposed.json"
        (self.repo / example).parent.mkdir(parents=True)
        (self.repo / example).write_text("{}")
        self.git("add", ".")
        staged = self.git("ls-files").stdout.decode().splitlines()
        self.assertNotIn(filename, staged)
        self.assertIn(example, staged)

    def test_windows_checkout_preserves_renderer_inputs(self):
        files = ("reference-architectures/sap-order-acknowledgments.md", "COMPONENTS.md",
                 "tools/diagrams/platforms.txt", "tools/diagrams/render.mjs",
                 "tools/diagrams/package-lock.json", "assets/platforms/studio.svg",
                 "assets/platforms/products.json", "assets/flows/manifest.json",
                 "assets/flows/write-reconciliation.png")
        for name in files:
            dest = self.repo / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)
        (self.repo / "control.txt").write_bytes(b"one\ntwo\n")
        self.git("add", ".")
        self.git("checkout-index", "--all", "--prefix=clean/")
        checkout = self.repo / "clean"
        self.assertEqual((checkout / "control.txt").read_bytes(), b"one\r\ntwo\r\n")
        for name in files:
            with self.subTest(name=name):
                self.assertEqual((checkout / name).read_bytes(), (ROOT / name).read_bytes())
