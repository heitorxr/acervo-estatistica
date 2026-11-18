"""Regression checks for canonical document links in printable project sheets."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://heitorxr.github.io/acervo-estatistica/'


class AnchorParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            href = dict(attrs).get('href')
            if href:
                self.links.append(href)


class PrintableLinksTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='acervo-links-', dir=os.environ.get('TMPDIR'))
        cls.output = Path(cls.temp.name)
        (cls.output / 'tools').mkdir()
        for name in ['index.template.html', 'projetos.json', 'tools/build_site.py']:
            shutil.copy2(ROOT / name, cls.output / name)
        subprocess.run([sys.executable, str(cls.output / 'tools/build_site.py')], check=True, capture_output=True)
        cls.projects = json.loads((ROOT / 'projetos.json').read_text(encoding='utf-8'))

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_teaching_archive_is_reachable_from_the_portfolio(self):
        parser = AnchorParser()
        parser.feed((self.output / 'index.html').read_text(encoding='utf-8'))
        self.assertIn('https://heitorxr.github.io/acervo-didatico/', parser.links)

    def test_each_original_document_is_linked_only_once(self):
        for project in self.projects:
            if not project.get('workUrl'):
                continue
            with self.subTest(project=project['id']):
                parser = AnchorParser()
                parser.feed((self.output / '_build' / ('ficha-' + project['id'] + '.html')).read_text(encoding='utf-8'))
                target = urljoin(BASE, project['workUrl'])
                self.assertEqual(sum(urljoin(BASE, link) == target for link in parser.links), 1)


if __name__ == '__main__':
    unittest.main()
