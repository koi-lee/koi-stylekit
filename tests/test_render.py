import json
import subprocess
import sys
import threading
import unittest
import urllib.request
import urllib.error
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from koi import render_request, ROOT
from serve import make_server

class RenderTests(unittest.TestCase):
    def test_choice_blocks_export(self):
        r=render_request(dict(style_id='duotone-print',subject='绿色的书'))
        self.assertEqual(r['status'],'needs_color_choice')
        self.assertIsNone(r['prompt_zh'])

    def test_subject_color_removes_fixed_palette(self):
        for style in ['duotone-print','minimal-line']:
            r=render_request(dict(style_id=style,subject='绿色的书',color_policy='subject'))
            self.assertTrue(r['palette_variant'])
            self.assertIn('绿色的书',r['prompt_zh'])
            self.assertNotIn('只给一个关键物体',r['prompt_zh'])
            self.assertNotIn('仅使用珊瑚红',r['prompt_zh'])

    def test_title_separate_and_subject_literal(self):
        r=render_request(dict(style_id='ink-accent',subject='猫 {subject} $(echo x)',caption='春日故事',aspect='3:4'))
        self.assertEqual(r['brief']['caption'],'春日故事')
        self.assertNotIn('春日故事',r['prompt_zh'])
        self.assertIn('猫 {subject} $(echo x)',r['prompt_zh'])
        self.assertIn('3:4',r['prompt_zh'])

    def test_invalid_inputs(self):
        for extra in [dict(subject=' '),dict(aspect='9:9'),dict(purpose='bad'),dict(caption='x'*81),dict(color_policy='bad')]:
            with self.assertRaises(ValueError):
                render_request(dict(dict(style_id='ink-accent',subject='猫'),**extra))

    def test_cli_http_exact_equality(self):
        server=make_server(0)
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            for policy in ['ask','style','subject']:
                data=dict(style_id='duotone-print',subject='绿色的书',caption='书香',aspect='3:4',purpose='cover',color_policy=policy)
                url=f'http://127.0.0.1:{server.server_port}/api/render'
                req=urllib.request.Request(url,data=json.dumps(data).encode(),headers={'Content-Type':'application/json'})
                with urllib.request.urlopen(req) as response: api=json.load(response)
                cli=subprocess.run([sys.executable,str(ROOT/'scripts/koi.py'),'render','--style',data['style_id'],'--subject',data['subject'],'--caption','书香','--aspect','3:4','--purpose','cover','--color-policy',policy],capture_output=True,text=True)
                self.assertEqual(cli.returncode,2 if policy=='ask' else 0)
                self.assertEqual(api,json.loads(cli.stdout))
            req=urllib.request.Request(url,data=b'{}',headers={'Content-Type':'application/json','Origin':'https://example.com'})
            with self.assertRaises(urllib.error.HTTPError) as caught:urllib.request.urlopen(req)
            self.assertEqual(caught.exception.code,403)
            caught.exception.close()
        finally:
            server.shutdown();server.server_close();thread.join()

if __name__=='__main__':unittest.main()
