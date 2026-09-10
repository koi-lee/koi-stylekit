"""Cross-runtime parity: requires Node.js, fails rather than silently skipping."""
import json
import subprocess
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from koi import ROOT, catalogue, render_request

class StaticParityTests(unittest.TestCase):
    def test_all_recipes_and_boundaries(self):
        requests = []
        for style in catalogue():
            for purpose in style['uses']:
                for policy in ('ask','style','subject'):
                    for aspect in (None,'1:1','3:4','16:9'):
                        requests.append(dict(style_id=style['id'],subject='  绿色的书 RED red 猫blue 蓝色 🐟 {subject} $&  ',purpose=purpose,color_policy=policy,aspect=aspect,caption=' 标题 '))
        for subject in ('',' '*3,None,123,'🐟'*1200,'🐟'*1201,'\ufeff','\x1c猫\x1f','red猫 猫red red_blue red-blue','RED red Blue blue','Kblack ıred ſilver'):
            requests.append(dict(style_id='duotone-print',subject=subject))
        requests.extend([[],{},dict(style_id='no',subject='猫'),dict(style_id='minimal-line',subject='猫'),dict(style_id='duotone-print',subject='猫',extra=1)])
        for field, value in [('caption','🐟'*81),('caption',42),('aspect','2:3'),('purpose','no'),('color_policy','no')]:
            requests.append(dict(style_id='duotone-print',subject='猫',**{field:value}))
        expected=[]
        for data in requests:
            try: expected.append(render_request(data))
            except ValueError as e: expected.append({'error':str(e)})
        script="""
import fs from 'node:fs';
import {renderRequest} from './wireframes/renderer.mjs';
const styles=JSON.parse(fs.readFileSync('wireframes/styles.json'));
const rules=JSON.parse(fs.readFileSync('wireframes/render-rules.json'));
const inputs=JSON.parse(fs.readFileSync(0,'utf8'));
console.log(JSON.stringify(inputs.map(d=>{try{return renderRequest(d,styles,rules)}catch(e){return {error:e.message}}})));
"""
        result=subprocess.run(['node','--input-type=module','-e',script],cwd=ROOT,input=json.dumps(requests),text=True,capture_output=True,check=True)
        actual=json.loads(result.stdout)
        self.assertEqual(len(expected),len(actual))
        for i,(a,b) in enumerate(zip(actual,expected)):
            self.assertEqual(a,b,repr(requests[i]))
        print(f'Browser/Python parity: {len(requests)} requests')
