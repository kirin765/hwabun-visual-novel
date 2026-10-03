"""Content identity and timing behavior, independent of Ren'Py's renderer."""
import json,re,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'sample/game/python-packages'))
from voice_policy import Pulse,opportunities,choose_clip,allow_density

class Content(unittest.TestCase):
    def test_every_original_block_in_order(self):
        original=(ROOT/'1화대본.md').read_text().split('## S01 ',1)[1].split('## 제작 확인 메모',1)[0]
        expected=[]
        for paragraph in re.split(r'\n\s*\n',original):
            match=re.match(r'^(미란 속말|미란|세란|옥녀|단주|현마|라디오|운전수): (.*)$',paragraph,re.S)
            if match:expected.append(match.groups())
        aliases={'inner':'미란 속말','miran':'미란','seran':'세란','oknyeo':'옥녀','danju':'단주','hyunma':'현마','radio':'라디오','driver':'운전수'}
        actual=[]
        for line in (ROOT/'sample/game/story.rpy').read_text().splitlines():
            m=re.match(r'\s+(inner|miran|seran|oknyeo|danju|hyunma|radio|driver) (".*") id sample_\d+',line)
            if m:actual.append((aliases[m[1]],json.loads(m[2])))
        self.assertEqual(expected,actual)
        self.assertEqual(len(actual),415)
        self.assertTrue(actual[-1][1].endswith('그래도 이제는 내 손으로 문을 열 차례였다.'))
    def test_only_expected_assets(self):
        game=ROOT/'sample/game'
        self.assertEqual(len(list((game/'images').glob('*.png'))),23)
        self.assertEqual(len(list((game/'audio').rglob('*.ogg'))),69)
        manifest=json.loads((game/'audio/voices.json').read_text())
        self.assertTrue(manifest['speakers']['miran']['approved'])
        self.assertEqual(len(manifest['speakers']['miran']['clips']),8)
        self.assertTrue(all(x['approved'] and len(x['clips'])==8 for x in manifest['speakers'].values()))
        for clip in manifest['speakers']['miran']['clips']:
            self.assertTrue((game/clip).is_file())
        for p in re.findall(r'"((?:audio|images|fonts)/[^"\n]+\.(?:ogg|png|otf))"','\n'.join(p.read_text() for p in game.glob('*.rpy'))):
            self.assertTrue((game/p).is_file(),p)

class Timing(unittest.TestCase):
    def test_half_the_playable_voice_opportunities(self):
        old = [i for i in range(100) if allow_density(i, 1.0)]
        reduced = [i for i in range(100) if allow_density(i, 0.5)]
        self.assertEqual(len(reduced), len(old) // 2)
        self.assertEqual(reduced, list(range(1,100,2)))
        self.assertFalse(any(allow_density(i, 0.0) for i in range(100)))
    def test_counts_only_valid_chars_but_waits_for_display(self):
        self.assertEqual(opportunities('아, 나. 다 라!',10),[.9])
        self.assertEqual(opportunities('가'*40,10),[.4,2.,3.6])
    def test_minimum_interval_and_maximum_three(self):
        for cps in (5,20,28,60,120):
            p=Pulse('가'*600,cps)
            events=[t/100 for t in range(12001) if p.tick(t/100)]
            self.assertEqual(len(events),3)
            self.assertTrue(all(b-a >= 1.2-1e-8 for a,b in zip(events,events[1:])))
            self.assertAlmostEqual(events[0],4/cps,delta=.011)
    def test_thought_muted_and_instant_text(self):
        for p in [Pulse('가'*300,28,False),Pulse('가'*300,0)]:
            self.assertFalse(any(p.tick(i/100) for i in range(3000)))
    def test_cancel_never_restarts_or_catches_up(self):
        p=Pulse('가'*300,20);p.stop()
        self.assertFalse(any(p.tick(i/100) for i in range(3000)))
        p=Pulse('가'*300,20)
        self.assertFalse(p.tick(8.5))
        self.assertFalse(p.tick(8.51))
    def test_no_immediate_repetition(self):
        pool=['a','b','c'];previous=None
        for _ in range(20):
            clip=choose_clip(pool,previous,lambda x:x[0])
            self.assertNotEqual(clip,previous);previous=clip
        self.assertIsNone(choose_clip(['a'],'a',lambda x:x[0]))

if __name__=='__main__':unittest.main(verbosity=2)
