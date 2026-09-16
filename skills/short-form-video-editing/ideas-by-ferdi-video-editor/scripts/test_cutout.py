"""Opt-in and actual layer-order checks; no RVM model needed."""
from pathlib import Path
import tempfile
import unittest
from PIL import Image, ImageDraw
import video as v


class CutoutTests(unittest.TestCase):
    def test_gate(self):
        job=dict(mode='single',title='Test',intake=dict(cutout='ja'),title_behind_person=True)
        v.cutout_gate(job)
        v.cutout_gate({**job,'mode':'multi'})
        for change in ({'title':''},{'mode':'voiceover'},{'intake':{}},{'title_behind_person':False}):
            with self.assertRaises(ValueError):v.cutout_gate({**job,**change})
        v.cutout_gate({**job,'intake':dict(cutout='nein'),'title_behind_person':False})
        v.cutout_gate(dict(mode='voiceover',title='Test'))

    def test_layers(self):
        work=Path(tempfile.mkdtemp(prefix='cutout-test-',dir=v.PROJECTS/'short_form_work'))
        (work/'fonts').mkdir()
        import shutil
        shutil.copy2(v.TOOLS/'fonts/AlteHaasGroteskBold.ttf',work/'fonts/AlteHaasGroteskBold.ttf')
        job=dict(title='TEST',title_style='max_readable',captions=True,caption_y=350,title_behind_person=True)
        v.captions(job,[dict(word='TOP',start=0,end=2)],work)
        img=Image.new('RGBA',(1080,1920));ImageDraw.Draw(img).rectangle((90,270,990,420),fill='white');img.save(work/'title.png')
        v.ff(['-f','lavfi','-i','color=blue:s=1080x1920:r=30:d=2',
              '-vf','drawbox=x=400:y=100:w=300:h=500:color=red:t=fill','-c:v','ffv1',work/'base.mkv'])
        v.ff(['-f','lavfi','-i','color=black:s=1080x1920:r=30:d=2',
              '-vf',"drawbox=x=400:y=100:w=300:h=500:color=white:t=fill:enable='lt(t,1)',format=gray",'-c:v','ffv1',work/'cutout-alpha.mkv'])
        v.ff(['-i','base.mkv','-vf',v.visual_filter(job,dict(duration=2)),'-c:v','ffv1','result.mkv'],work)
        frames=[]
        for t in (.5,1.5):
            path=work/f'{t}.png';v.ff(['-ss',t,'-i','result.mkv','-frames:v','1',path],work)
            frames.append(Image.open(path).convert('RGB'))
        self.assertGreater(frames[0].getpixel((420,300))[0],240)
        self.assertLess(frames[0].getpixel((420,300))[1],10)  # Person above title.
        self.assertGreater(min(frames[0].getpixel((200,300))),240)  # Visible title outside person.
        self.assertGreater(min(frames[1].getpixel((420,300))),240)  # Zero mask: title stays above B-roll.
        self.assertTrue(any(min(frames[0].getpixel((x,y)))>230 for x in range(490,590) for y in range(330,370)))
        print('Layer QA artifacts:',work)


if __name__=='__main__':unittest.main()
