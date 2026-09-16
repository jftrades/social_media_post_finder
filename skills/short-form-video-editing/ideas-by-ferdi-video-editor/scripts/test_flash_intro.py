"""Frame-accurate FlashShutterIntro integration test; no user media required."""
import tempfile
from pathlib import Path
import unittest
import video as v


class FlashShutterIntro(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources=v.PROJECTS/'short_form_unfinished_projects'/'flash-intro-test'
        cls.sources.mkdir(parents=True,exist_ok=True)
        colors=('red','orange','yellow','green','blue','purple','white')
        for index,color in enumerate(colors):
            target=cls.sources/f'{index}.mp4'
            v.ff(['-f','lavfi','-i',f'color=c={color}:s=270x480:r=30:d=2',
                  '-an','-c:v','libx264','-pix_fmt','yuv420p',target])

    def test_frame_timing_audio_and_duration(self):
        work=Path(tempfile.mkdtemp(prefix='flash-intro-test-',dir=v.PROJECTS/'short_form_work'))
        v.ff(['-f','lavfi','-i','color=c=black:s=1080x1920:r=30:d=5',
              '-f','lavfi','-i','sine=frequency=220:sample_rate=48000:duration=5',
              '-map','0:v','-map','1:a','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
              '-c:a','pcm_s16le','base.mkv'],work)
        paths=[f'project_videos/short_form_unfinished_projects/flash-intro-test/{i}.mp4' for i in range(7)]
        job={'project':'flash-intro-test','mode':'voiceover','capture':'phone',
             'intake':{'flash_shutter_intro':'ja'},'flash_shutter_intro_enabled':True,
             'flash_shutter_intro_clips':paths,'visuals':[{'path':p,'capture':'phone'} for p in paths]}
        result=v.add_flash_shutter_intro(job,work,'base.mkv',5)
        self.assertEqual(result,'flash-base.mkv')
        self.assertAlmostEqual(v.duration(work/result),5,places=1)
        self.assertAlmostEqual(v.duration(work/'flash-shutter-sfx.wav'),5,places=1)
        report=v.read(work/'flash-shutter-report.json')
        self.assertEqual(report['frame_counts'],list(v.FLASH_SHUTTER_FRAME_COUNTS))
        self.assertEqual(len(report['clips']),7)
        self.assertTrue(all(abs(c-s-.2)<1e-9 for c,s in zip(report['cut_times'],report['shutter_times'])))


if __name__=='__main__':unittest.main()
