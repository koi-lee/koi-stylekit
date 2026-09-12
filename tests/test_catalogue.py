import json
import struct
import zlib
import hashlib
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from koi import catalogue, render_request, ROOT

class CatalogueTests(unittest.TestCase):
    def test_identity_and_family_links(self):
        styles = catalogue()
        ids = [s['id'] for s in styles]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(len(styles), 308)
        self.assertEqual(len({s['catalogue_number'] for s in styles}), 308)
        by_id = {s['id']: s for s in styles}
        for s in styles:
            self.assertIn(s['family_id'], by_id)
            if s['variant_of']:
                self.assertEqual(s['variant_of'], s['family_id'])
                self.assertFalse(by_id[s['variant_of']]['variant_of'])
            if s.get('image'):
                self.assertTrue((ROOT / 'wireframes' / s['image']).is_file())

    def test_every_supported_export(self):
        for s in catalogue():
            for purpose in s['uses']:
                for policy in ['style', 'subject']:
                    with self.subTest(style=s['id'], purpose=purpose, policy=policy):
                        pack=render_request(dict(style_id=s['id'],subject='绿色的伞',purpose=purpose,color_policy=policy))
                        self.assertEqual(pack['status'], 'ready')
                        self.assertIn('绿色的伞',pack['prompt_zh'])
                        self.assertNotIn('{subject}',pack['prompt_zh'])

    def test_sample_prompt_provenance(self):
        for p in (ROOT / 'wireframes/assets/catalogue').glob('*.json'):
            data=json.loads(p.read_text())
            request=dict(style_id=data['style']['id'], **data['brief'])
            self.assertEqual(render_request(request)['prompt_zh'],data['prompt_zh'])

    def test_all_sample_files_are_complete_and_distinct(self):
        hashes = set()
        for style in catalogue():
            with self.subTest(style=style['id']):
                self.assertTrue(style.get('image'))
                data = (ROOT / 'wireframes' / style['image']).read_bytes()
                self.assertEqual(data[:8], b'\x89PNG\r\n\x1a\n')
                self.assertEqual((style['image_width'], style['image_height']),
                                 struct.unpack('>II', data[16:24]))
                offset = 8
                last_type = None
                while offset < len(data):
                    size = struct.unpack('>I', data[offset:offset + 4])[0]
                    chunk = data[offset + 4:offset + 8 + size]
                    crc = struct.unpack('>I', data[offset + 8 + size:offset + 12 + size])[0]
                    self.assertEqual(zlib.crc32(chunk) & 0xffffffff, crc)
                    last_type = chunk[:4]
                    offset += 12 + size
                self.assertEqual(last_type, b'IEND')
                self.assertEqual(offset, len(data))
                digest = hashlib.sha256(data).hexdigest()
                self.assertNotIn(digest, hashes)
                hashes.add(digest)
