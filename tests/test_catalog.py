import collections
import hashlib
import json
import re
import unittest
from urllib.parse import unquote, urlsplit

from tools.validate_solution import GROUPS, ROOT, RULES


ENTRIES = {p.relative_to(ROOT).as_posix():p for group in GROUPS for p in (ROOT / group).glob("*.md")}
LINK = r"\[[^\]\n]*\]\(([^\s)]+)\)"


class CatalogIntegrity(unittest.TestCase):
    def test_published_counts_match_entries_by_class(self):
        catalog = (ROOT / "CATALOG.md").read_text()
        readme = (ROOT / "README.md").read_text()
        self.assertIn(f"**{len(ENTRIES)} entries**", readme)
        self.assertIn(f"**{len(ENTRIES)} separate pattern files**", catalog)
        sections = (("Microsoft reference architectures", "microsoft-reference-architectures"),
                    ("Microsoft solution ideas", "microsoft-solution-ideas"),
                    ("Fabric integration options", "fabric-integration-options"),
                    ("Orchestration and handoff options", "orchestration-and-handoff-options"),
                    ("Synthesized technical patterns", "synthesized-technical-patterns"))
        for heading, anchor in sections:
            section = catalog.split(f"\n## {heading}\n", 1)[1].split("\n## ", 1)[0]
            count = sum(link in ENTRIES for row in section.splitlines() if row.startswith("|")
                        for link in re.findall(LINK, row))
            for guide in (readme, catalog):
                self.assertRegex(guide, re.escape(f"#{anchor}) | {count} |"))

    def test_catalog_component_and_credit_coverage(self):
        tables = []
        for file, section in (("CATALOG.md", None), ("COMPONENTS.md", "component-matrix"),
                              ("COPILOT-CREDITS.md", "credit-profile")):
            text = (ROOT / file).read_text()
            if section:
                text = text.split(f"<!-- {section}:start -->")[1].split(f"<!-- {section}:end -->")[0]
            rows, counts = {}, collections.Counter()
            for line in text.splitlines():
                if line.startswith("|"):
                    for link in re.findall(LINK, line):
                        if link.split("/")[0] in GROUPS and not urlsplit(link).fragment:
                            counts[link] += 1
                            rows[link] = [c.strip() for c in line.strip("|").split("|")]
            self.assertEqual(counts, collections.Counter(ENTRIES.keys()), file)
            tables.append(rows)
        for key, path in ENTRIES.items():
            matrix, credits, text = tables[1][key], tables[2][key], path.read_text()
            self.assertEqual((len(matrix), len(credits)), (11, 4), key)
            self.assertEqual(matrix[1], credits[1], key)
            self.assertIn(f"**copilot credits drivers ({credits[2].lower()}):", text.lower(), key)
            self.assertEqual(text.count("```mermaid"), 2, key)
            for token in ("## Architecture", "**Review decision:**", "## Technical flow", "autonumber",
                          "## Copilot Studio components"):
                self.assertIn(token, text, key)

    def test_review_rules_link_to_guidance(self):
        for _, _, ref in RULES.values():
            self.assertTrue((ROOT / ref).is_file(), ref)

    def test_rendered_images(self):
        manifest = json.loads((ROOT / "assets/flows/manifest.json").read_text())
        self.assertEqual(set(manifest), {p.stem for p in ENTRIES.values()})
        for p in ENTRIES.values():
            image = ROOT / f"assets/flows/{p.stem}.png"
            self.assertEqual(hashlib.sha256(image.read_bytes()).hexdigest(), manifest[p.stem]["png"], p)
            self.assertIn(f"](../assets/flows/{p.stem}.png)", p.read_text(), p)

    def test_document_links(self):
        # Check maintained documents, never third-party tool dependencies.
        docs = [*ROOT.glob("*.md"), *ENTRIES.values(), *(ROOT / "review").glob("*.md"),
                *(ROOT / "assets/platforms").glob("*.md"), *(ROOT / "tools/diagrams").glob("*.md")]
        texts = {p:p.read_text() for p in docs}
        anchors = {p:{"".join(c for c in h.lower() if c.isalnum() or c in " _-").replace(" ", "-")
                      for h in re.findall(r"^#{1,6} (.*)$", t, re.M)} for p,t in texts.items()}
        for p, text in texts.items():
            for link in re.findall(LINK, text):
                u = urlsplit(link)
                if u.scheme or u.netloc:
                    continue
                dest = (p.parent / unquote(u.path)).resolve() if u.path else p
                self.assertTrue(dest.exists(), f"{p.name}: {link}")
                if u.fragment and dest in anchors:
                    self.assertIn(unquote(u.fragment), anchors[dest], f"{p.name}: {link}")
