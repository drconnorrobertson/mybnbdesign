"""Regression checks for serialization and contextual linking."""
import ast
import json
from pathlib import Path
import tempfile
import unittest
from check_jsonld import Blocks, check
from crosslink import add_crosslinks

ROOT = Path(__file__).resolve().parents[1]

class JsonLdTests(unittest.TestCase):
    def test_full_site(self):
        self.assertEqual(check(ROOT)['errors'], [])

    def test_gate_detects_bad_block_and_constants(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'nested').mkdir()
            (root / 'nested/page.html').write_text('<script TYPE="application/ld+json">{"x":"bad "quote""}</script><script type="application/ld+json">NaN</script>')
            self.assertEqual(check(root)['invalid_blocks'], 2)

    def test_crosslink_preserves_raw_text_and_links_visible_copy(self):
        raw = '<script type="application/ld+json">{"name":"beach house"}</script><script>const x = "beach house";</script><style>.x {content: "beach house"}</style>'
        linked, count = add_crosslinks(raw + '<p>beach house helps hosts.</p>', '/example.html')
        self.assertTrue(linked.startswith(raw))
        self.assertGreater(count, 0)
        json.loads(Blocks(linked).blocks[0][1])

    def test_generator_roundtrips_special_strings(self):
        # Load definitions without running the legacy generator's file-writing code.
        tree = ast.parse((ROOT / 'scripts/generate_longtail_pages.py').read_text())
        definitions = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef)) or (isinstance(n, ast.Assign) and all(isinstance(t, ast.Name) and t.id in {'TODAY', 'TODAY_LONG', 'BASE_URL'} for t in n.targets))]
        scope = {}
        exec(compile(ast.Module(body=definitions, type_ignores=[]), '<generator definitions>', 'exec'), scope)
        special = 'Quoted "name", backslash \\, café & <a href="/book/">book</a> </script>'
        page = scope['make_page'](special, special, [special], 'Test', [], [(special, special)], 'blog/test/', [])
        blocks = [json.loads(text) for _, text in Blocks(page).blocks]
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0][0]['headline'], special)
        self.assertEqual(blocks[0][1]['mainEntity'][0]['acceptedAnswer']['text'], special)
        self.assertEqual(blocks[1]['itemListElement'][2]['name'], special)

if __name__ == '__main__':
    unittest.main()
