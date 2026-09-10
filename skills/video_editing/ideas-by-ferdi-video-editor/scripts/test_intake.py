"""Intake and voice-over timing invariants; no user media required."""
import copy
import unittest
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

    def test_retiming(self):
        self.assertEqual(v.visual_timing(dict(start=12,end=17,speed=2),18,True),2.5)
        for visual in (dict(start=12,end=16,speed=2),dict(start=0,end=5,speed=2),dict(start=12,end=19.5,speed=3)):
            with self.assertRaises(ValueError):v.visual_timing(visual,18,True)

    def test_voiceover_without_cutout(self):
        job=self.job();job.update(mode='voiceover',strict_visual_timing=True)
        job['intake'].update(visual_timing='ja',retiming='keine')
        v.gate(job)
        with self.assertRaises(ValueError):v.gate({**job,'title_behind_person':True})
        job.update(zoom_enabled=True,visuals=[dict(start=0,end=2.5),dict(start=0,end=2.5)],
                   zooms=[dict(source=0,start=1,end=1.5,reset=4,reason='point')])
        job['intake']['zooms']='ja';v.gate(job)
        events=v.zoom_timeline(job,[dict(source=0,start=0,end=5)])
        self.assertEqual(events[0]['reset'],2.5)


if __name__=='__main__':unittest.main()
