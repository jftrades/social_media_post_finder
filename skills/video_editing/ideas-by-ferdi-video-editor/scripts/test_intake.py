"""Intake and voice-over timing invariants; no user media required."""
import copy
import unittest
from pathlib import Path
from unittest.mock import patch
import video as v


class Intake(unittest.TestCase):
    def job(self):
        return dict(project='test',mode='single',sources=['test.mp4'],
                    intake={**{k:'ja' for k in ('format','cleanup','clips','captions','music','title','broll','capture','audio_normalization')},'zooms':'nein'},
                    intake_confirmed=True,intake_completed_levels=[1,2,3],
                    audio_normalize=True,zoom_enabled=False,title='',capture='graded',broll_mode='none')

    def test_waits_for_every_level(self):
        job=self.job();v.gate(job)
        for levels in ([],[1],[1,2],[2,1,3]):
            with self.assertRaises(ValueError):v.gate({**job,'intake_completed_levels':levels})
        for key in job['intake']:
            missing=copy.deepcopy(job);del missing['intake'][key]
            with self.assertRaises(ValueError):v.gate(missing)

    def test_audio_title_and_exceptions(self):
        job=self.job();job['audio_normalize']=False
        with self.assertRaises(ValueError):v.gate(job)
        job['intake']['audio_normalization']='nein';v.gate(job)
        job.update(title='Test',title_style='snapchat',title_behind_person=False)
        job['intake'].update(title_style='snapchat',cutout='nein')
        with self.assertRaises(ValueError):v.gate(job)
        job['title_duration']=3;v.gate(job)
        with self.assertRaises(ValueError):v.gate({**job,'segment_overrides':[{'source':0,'captions':False}]})
        self.assertEqual(v.video_filter('graded'),v.video_filter('phone'))
        custom=v.video_filter('camera',normalize_mix=.4,look_mix=.4)
        self.assertIn("A*0.6+B*0.4",custom)

    def test_retiming(self):
        self.assertEqual(v.visual_timing(dict(start=12,end=17,speed=2),18),2.5)
        for visual in (dict(start=-1,end=2,speed=1),dict(start=5,end=4,speed=1),dict(start=12,end=19.5,speed=3),dict(start=0,end=5,speed=.5)):
            with self.assertRaises(ValueError):v.visual_timing(visual,18)

    def test_voiceover_without_cutout(self):
        job=self.job();job.update(mode='voiceover',sources=['voice.wav'],
                                  visual_cut_policy='one_second_montage_over_5s',voiceover_broll_policy='none',
                                  voiceover_inserts=[])
        job['intake'].update(original_audio='nein',visual_timing='one_second_montage_over_5s',
                             retiming='keine',broll_fallback='none')
        v.gate(job)
        with self.assertRaises(ValueError):v.gate({**job,'sources':['a.wav','b.wav']})
        with self.assertRaises(ValueError):v.gate({**job,'title_behind_person':True})
        job.update(zoom_enabled=True,visuals=[dict(start=0,end=2.5),dict(start=0,end=2.5)],
                   zooms=[dict(source=0,start=1,end=1.5,reset=4,reason='point')])
        job['intake']['zooms']='ja';v.gate(job)
        events=v.zoom_timeline(job,[dict(source=0,start=0,end=5)])
        self.assertEqual(events[0]['reset'],2.5)

    @patch.object(v,'media',side_effect=lambda path:Path(path))
    @patch.object(v,'duration',return_value=8)
    def test_long_voiceover_visuals_are_multiple_one_second_snippets(self,_duration,_media):
        base=dict(voiceover_inserts=[],visuals=[
            dict(path='long.mp4',start=0,end=1,speed=1),
            dict(path='long.mp4',start=3,end=4,speed=1)])
        v.voiceover_visual_gate(base)
        with self.assertRaises(ValueError):
            v.voiceover_visual_gate({**base,'visuals':base['visuals'][:1]})
        bad=copy.deepcopy(base);bad['visuals'][0]['end']=.8
        with self.assertRaises(ValueError):v.voiceover_visual_gate(bad)
        insert=dict(path='live.mp4',start=1,end=5,speed=1,original_audio=True)
        v.voiceover_visual_gate(dict(voiceover_inserts=[dict(path='live.mp4',start=1,end=5,reason='spoken line')],visuals=[insert,*base['visuals']]))


if __name__=='__main__':unittest.main()
