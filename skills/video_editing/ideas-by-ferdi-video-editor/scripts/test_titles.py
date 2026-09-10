"""Run with uv run --with pillow==12.3.0 python test_titles.py."""
import tempfile
from pathlib import Path
import unittest
from PIL import Image
import video as v


class Titles(unittest.TestCase):
    def test_styles(self):
        work=Path(tempfile.mkdtemp(prefix='title-test-',dir=v.PROJECTS/'work'))
        long='Wetten ich kann dein Leben in den nächsten 20sek verändern?!'
        sizes={}
        for style in v.TITLE_STYLES:
            for text in ('WTF',long):
                job=dict(mode='single',title=text,title_style=style,intake=dict(title_style=style))
                v.title_gate(job);v.title_image(job,work)
                layout=v.read(work/'title-layout.json')
                sizes[style,text]=layout['font_size']
                self.assertEqual(layout['top'],270)
                if style=='max_readable':self.assertEqual(layout['font_size'],76)
                if style=='blurred_key_quali':
                    self.assertLessEqual(layout['ink_height'],220)
                    self.assertAlmostEqual(layout['blur_radius'],layout['font_size']*.025)
                if style=='snapchat':
                    self.assertEqual(Image.open(work/'title.png').getpixel((0,270)),(70,70,70,170))
                # Preserve short/long samples for visual checks without modifying real projects.
                Image.open(work/'title.png').save(work/f'{style}-{len(text)}.png')
        self.assertGreater(sizes['blurred_key_quali','WTF'],sizes['blurred_key_quali',long])
        with self.assertRaises(ValueError):v.title_gate(dict(mode='single',title='WTF',intake={}))
        v.title_gate(dict(mode='single',title='',intake={}))
        v.title_gate(dict(mode='voiceover',title='WTF',title_style='snapchat',intake=dict(title_style='snapchat')))
        print('Title test samples:',work)


if __name__=='__main__':unittest.main()
