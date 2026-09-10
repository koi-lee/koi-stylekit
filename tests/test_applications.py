"""Ensure application demos use real assets and the shared recipes."""
import json
import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from koi import ROOT, render_request

class ApplicationTests(unittest.TestCase):
    def test_all_nine_application_samples_match_renderer(self):
        directory=ROOT/'wireframes/cases/style-applications'
        for style in ['paper-lightbox','popup-book','bubble-mosaic']:
            for topic in ['people','product','knowledge']:
                with self.subTest(style=style,topic=topic):
                    stem=directory/(style+'-'+topic)
                    pack=json.loads(stem.with_suffix('.json').read_text())
                    self.assertEqual(pack['prompt_zh'],render_request(dict(style_id=style,**pack['brief']))['prompt_zh'])
                    self.assertTrue(stem.with_suffix('.png').read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
                    self.assertIn(stem.name+'.png',(directory/'index.html').read_text())
