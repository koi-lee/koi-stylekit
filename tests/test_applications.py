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

    def test_paper_kit_prompts_and_downloads_match_saved_inputs(self):
        """Prevent displayed prompts drifting from downloadable generation inputs."""
        from html.parser import HTMLParser
        class CaseParser(HTMLParser):
            def __init__(self):
                super().__init__(); self.prompts=[]; self.downloads=[]; self.images=[]; self.in_text=False
            def handle_starttag(self,tag,attrs):
                attrs=dict(attrs)
                if tag=='textarea': self.in_text=True; self.prompts.append('')
                if tag=='a' and 'download' in attrs: self.downloads.append(attrs['href'])
                if tag=='img': self.images.append(attrs['src'])
            def handle_endtag(self,tag):
                if tag=='textarea': self.in_text=False
            def handle_data(self,data):
                if self.in_text: self.prompts[-1]+=data
        directory=ROOT/'wireframes/cases/style-applications'
        page=CaseParser(); page.feed((directory/'paper-kit.html').read_text())
        self.assertEqual(len(page.prompts),4)
        self.assertEqual(len(page.downloads),4)
        self.assertEqual(len(page.images),4)
        for prompt,download,image in zip(page.prompts,page.downloads,page.images):
            with self.subTest(download=download):
                pack=json.loads((directory/download).read_text())
                self.assertEqual(prompt,pack['prompt_zh'])
                self.assertEqual(prompt,render_request(dict(style_id=pack['style']['id'],**pack['brief']))['prompt_zh'])
                self.assertTrue((directory/image).read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
