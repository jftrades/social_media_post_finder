"""Local integration test: uv run --with pillow python .../test_zooms.py."""
import copy
import math
from pathlib import Path
import tempfile
import unittest
import wave
from array import array
from PIL import Image, ImageChops, ImageStat
import video as v


class ZoomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cache=v.PROJECTS/'work';cache.mkdir(exist_ok=True)
        cls.work=Path(tempfile.mkdtemp(prefix='zoom-test-',dir=cache))
        v.ff(['-f','lavfi','-i','testsrc2=size=1080x1920:rate=30','-frames:v','1',cls.work/'source.png'])
        v.ff(['-loop','1','-i',cls.work/'source.png','-f','lavfi','-i','sine=frequency=440:sample_rate=48000',
              '-t','4.5','-c:v','libx264','-pix_fmt','yuv420p','-c:a','aac',cls.work/'source.mp4'])
        cls.job=dict(project='zoom-test',mode='single',sources=[str(cls.work/'source.mp4')],
                     intake={k:'ja' for k in ('cleanup','clips','captions','music','title','broll','capture','zooms')},
                     intake_confirmed=True,cleanup=True,captions=True,title='Pointe prüfen!',capture='phone',
                     broll_mode='none',broll=[],zoom_enabled=True,
                     music='agent_tooling/background_music/Phrygian_Drift_2026-09-04T124142.mp3',
                     zooms=[dict(source=0,start=.8,end=1.4,reset=2.0,out_duration=.2,reason='first point'),
                            dict(source=0,start=2.4,end=2.8,reset=4.0,reason='second point')])
        cls.job['title_style']='max_readable'
        cls.job.update(intake_completed_levels=[1,2,3],audio_normalize=True,title_duration=3)
        cls.job['intake'].update(format='single',audio_normalization='ja')
        cls.job['intake']['title_style']='max_readable'
        cls.job['intake']['cutout']='nein'
        cls.job['title_behind_person']=False
        cls.words=[dict(word='Test',start=a,end=b) for a,b in [(0.1,.8),(1.4,2),(2.2,2.4),(2.8,3.3),(4,4.3)]]
        for i in (0,1):
            folder=cls.work/'transcripts'/str(i);folder.mkdir(parents=True)
            v.save(folder/'speech.json',dict(segments=[dict(words=cls.words)]))

    def test_gates(self):
        v.gate(self.job)
        for change in ({'zoom_enabled':False},{'mode':'voiceover'},
                       {'intake':{k:x for k,x in self.job['intake'].items() if k!='zooms'}}):
            with self.assertRaises(ValueError):v.gate({**self.job,**change})
        vo={**self.job,'mode':'voiceover','zoom_enabled':False,'zooms':[]}
        vo.update(strict_visual_timing=True,intake={**self.job['intake'],'zooms':'nein','visual_timing':'ja','retiming':'keine'})
        v.gate(vo)

    def test_plan_and_render(self):
        job=copy.deepcopy(self.job)
        v.plan(job,self.work);p=v.read(self.work/'plan.json')
        self.assertEqual(len(p['zooms']),2)
        self.assertLess(p['zooms'][1]['reset'],4)
        self.assertTrue(any(s['start']<=.8 and s['end']>=1.4 for s in p['segments']))
        yes_duration=p['duration']
        p['reviewed']=True;v.save(self.work/'plan.json',p)
        v.render(job,self.work)
        self.assertLessEqual(v.read(self.work/'render-check.json')['true_peak_dbfs'],-1)
        def frame(at,name):
            path=self.work/(name+'.png')
            v.ff(['-ss',at,'-i',self.work/'zoom-base.mkv','-frames:v','1',path])
            return Image.open(path).convert('RGB')
        before=frame(.2,'before');hold=frame(1.6,'hold');reset=frame(2.25,'reset')
        delta=lambda a,b:sum(ImageStat.Stat(ImageChops.difference(a,b)).mean)
        self.assertGreater(delta(before,hold),10)
        self.assertLess(delta(before,reset),3)
        with wave.open(str(self.work/'zoom-sfx.wav'),'rb') as wav:
            samples=array('h',wav.readframes(wav.getnframes()));rate=wav.getframerate()*wav.getnchannels()
        rms=lambda a,b:math.sqrt(sum(x*x for x in samples[int(a*rate):int(b*rate)])/max(1,int((b-a)*rate)))
        self.assertEqual(rms(0,.5),0)
        self.assertGreater(rms(.8,1.2),1)
        self.assertEqual(rms(1.5,1.8),0)
        no={**job,'zoom_enabled':False,'zooms':[],'intake':{**job['intake'],'zooms':'nein'}}
        no['audio_normalize']=False
        no['intake']['audio_normalization']='nein'
        v.plan(no,self.work);off=v.read(self.work/'plan.json')
        self.assertEqual(off['zooms'],[])
        self.assertLess(off['duration'],yes_duration)
        off['reviewed']=True;v.save(self.work/'plan.json',off)
        v.render(no,self.work)
        self.assertFalse(v.read(self.work/'render-check.json')['speech_measurement']['enabled'])

    def test_multi_and_conflicts(self):
        job=copy.deepcopy(self.job);job['mode']='multi';job['sources']*=2
        job['zooms']=[dict(source=0,start=.8,end=1.4,reset=99,reason='cut reset'),
                      dict(source=1,start=.8,end=1.4,reset=2,reason='second angle')]
        v.plan(job,self.work);p=v.read(self.work/'plan.json')
        self.assertEqual(len(p['zooms']),2)
        self.assertLess(p['zooms'][0]['reset'],p['zooms'][1]['start'])
        job['zooms'].append(dict(source=0,start=1.5,end=1.8,reset=2,reason='overlap'))
        with self.assertRaises(ValueError):v.plan(job,self.work)
        job=copy.deepcopy(self.job);job['drops']=[dict(source=0,start=.9,end=1.2)]
        with self.assertRaises(ValueError):v.plan(job,self.work)

    @classmethod
    def tearDownClass(cls):
        print('Test artifacts:',cls.work)


if __name__=='__main__':unittest.main()
