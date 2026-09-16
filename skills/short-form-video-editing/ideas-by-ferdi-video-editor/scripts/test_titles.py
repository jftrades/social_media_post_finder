"""Run with uv run --with pillow==12.3.0 python test_titles.py."""
import tempfile
from pathlib import Path
import unittest
from PIL import Image
import video as v


class Titles(unittest.TestCase):
    def test_styles(self):
        work=Path(tempfile.mkdtemp(prefix='title-test-',dir=v.PROJECTS/'short_form_work'))
        long='Wetten ich kann dein Leben in den nächsten 20sek verändern?!'
        for style in v.STATIC_TITLE_STYLES:
            for text in ('WTF',long):
                job=dict(mode='single',title=text,title_style=style,intake=dict(title_style=style))
                v.title_gate(job);v.title_image(job,work)
                layout=v.read(work/'title-layout.json')
                self.assertEqual(layout['top'],270)
                if style=='max_readable':self.assertEqual(layout['font_size'],76)
                if style=='snapchat':
                    self.assertEqual(Image.open(work/'title.png').getpixel((0,270)),(70,70,70,170))
                # Preserve short/long samples for visual checks without modifying real projects.
                Image.open(work/'title.png').save(work/f'{style}-{len(text)}.png')
        with self.assertRaises(ValueError):
            v.title_gate(dict(mode='single',title='WTF',title_style='removed_style',intake={'title_style':'removed_style'}))
        with self.assertRaises(ValueError):v.title_gate(dict(mode='single',title='WTF',intake={}))
        v.title_gate(dict(mode='single',title='',intake={}))
        v.title_gate(dict(mode='voiceover',title='WTF',title_style='snapchat',intake=dict(title_style='snapchat')))
        print('Title test samples:',work)

    def test_fixed_multiline_presets_and_empty_slots(self):
        work=Path(tempfile.mkdtemp(prefix='multiline-title-test-',dir=v.PROJECTS/'short_form_work'))
        expected={
            'preset_1':[(45,540,316),(87,540,392),(38,749.5,450)],
            'preset_2':[(125,382,420.5),(125,680,524),(36,749.5,624)],
            'preset_3':[(48,540,810),(143,540,900),(143,540,1020)]}
        for style,geometry in expected.items():
            lines=['OBEN','MITTE','UNTEN']
            job=dict(mode='single',title='\n'.join(lines),title_lines=lines,title_style=style,intake={'title_style':style})
            v.title_gate(job);v.title_image(job,work)
            layout=v.read(work/'title-layout.json')
            expected_animation={
                'preset_1':'rise 40px + cubic ease-out + 1.0s alpha fade; 0.12s stagger',
                'preset_2':'top from left and middle from above together; bottom rises after 0.12s; cubic ease-out + 1.0s alpha fade',
                'preset_3':'none'}
            self.assertEqual(layout['animation'],expected_animation[style])
            self.assertEqual(layout['default_duration'],4)
            for line,(size,x,y) in zip(layout['lines'],geometry):
                self.assertTrue(line['rendered'])
                self.assertEqual(line['font_size_px'],size)
                self.assertEqual(line['output_x'],x)
                self.assertEqual(line['output_y'],y)
            if style in {'preset_1','preset_2'}:self.assertEqual(layout['lines'][2]['text'],'*UNTEN')
            if style=='preset_2':self.assertEqual([line['stroke'] for line in layout['lines'][:2]],[3,3])
            Image.open(work/'title.png').save(work/f'{style}.png')
        empty=dict(mode='single',title='OBEN',title_lines=['OBEN','leer','kein Text'],title_style='preset_2',intake={'title_style':'preset_2'})
        v.title_gate(empty);v.title_image(empty,work)
        self.assertEqual([x['rendered'] for x in v.read(work/'title-layout.json')['lines']],[True,False,False])
        v.title_gate(dict(mode='single',title='',title_lines=['nix','','kein text'],title_style='preset_3',intake={'title_style':'preset_3'}))

    def test_multiline_animation_filters(self):
        plan={'duration':10}
        p1=dict(title='A\nB\nC',title_lines=['A','B','C'],title_style='preset_1')
        graph=v.visual_filter(p1,plan)
        self.assertIn("st=0.12:d=1.0",graph)
        self.assertIn("st=0.24:d=1.0",graph)
        self.assertIn("+40*(1-",graph)
        self.assertIn("lt(t,4.0)",graph)
        p2=dict(title='A\nB\nC',title_lines=['A','B','C'],title_style='preset_2',title_duration=6)
        graph=v.visual_filter(p2,plan)
        self.assertEqual(graph.count('st=0:d=1.0'),2)
        self.assertIn("st=0.12:d=1.0",graph)
        self.assertIn("-40*(1-",graph)
        self.assertIn("lt(t,6.0)",graph)
        p3=dict(title='A\nB\nC',title_lines=['A','B','C'],title_style='preset_3')
        self.assertIn('movie=title.png',v.visual_filter(p3,plan))


if __name__=='__main__':unittest.main()
