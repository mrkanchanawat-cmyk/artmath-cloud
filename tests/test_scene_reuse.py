"""Synthetic regression cases; no private episode assets are used."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('reuse_renderer', ROOT/'project/current/render_video.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class SourceReuseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        r.configure_root(Path(self.temp.name))

    def shot(self, sid, start, end, **extra):
        return {'id': sid, 'source_in': start, 'source_out': end, **extra}

    def test_overlap_boundary(self):
        for start, fails in [(2,False),(1.9,False),(1.85,False),(1.849,True),(0,True)]:
            with self.subTest(start=start):
                errors = r.validate_source_reuse([self.shot('A',0,2),self.shot('B',start,3)])
                self.assertEqual(bool(errors),fails,errors)

    def test_nonadjacent_contained_and_transform_reuse(self):
        shots = [self.shot('A',0,4), self.shot('B',7,8),
                 self.shot('C',1,2,zoom=2,crop=[0,0,100,100],allow_reuse=True)]
        errors = r.validate_source_reuse(shots)
        self.assertEqual(len(errors),1)
        self.assertIn('SHOT C',errors[0])
        self.assertIn('SHOT A',errors[0])
        self.assertIn('1.000s',errors[0])

    def test_same_path_aliases(self):
        r.SOURCE_MEDIA.parent.mkdir(parents=True,exist_ok=True)
        r.SOURCE_MEDIA.touch()
        alias=r.ROOT/'alias.mp4'
        alias.symlink_to(r.SOURCE_MEDIA)
        for source in ['inputs/video.mp4','inputs/../inputs/video.mp4',str(r.SOURCE_MEDIA),'alias.mp4']:
            with self.subTest(source=source):
                self.assertTrue(r.validate_source_reuse([
                    self.shot('A',0,2),self.shot('B',1,3,source=source)]))

    def test_different_sources_are_independent(self):
        self.assertEqual(r.validate_source_reuse([
            self.shot('A',0,2,source='inputs/one.mp4'),
            self.shot('B',0,2,source='inputs/two.mp4')]),[])

    def test_malformed_input_fails_closed(self):
        for shots in [None,{},[],[None],[{}],
                      [self.shot('A',True,2)],[self.shot('A',0,float('nan'))],
                      [self.shot('A',0,float('inf'))],[self.shot('A',-1,2)],
                      [self.shot('A',2,1)],[self.shot('A','0',2)],
                      [self.shot('A',0,2,source={})],[self.shot('A',0,2,source='')]]:
            with self.subTest(shots=shots):
                self.assertTrue(r.validate_source_reuse(shots))

    def test_direct_render_and_cached_render_cannot_bypass(self):
        doc={'shots':[self.shot('A',0,2),self.shot('B',1,3)]}
        for cached in (False,True):
            with patch.object(r,'render_shot') as shot_renderer, patch.object(r,'run') as run:
                with self.assertRaisesRegex(ValueError,'SCENE_REUSE'):
                    r.render(doc,reuse_shots=cached)
                shot_renderer.assert_not_called()
                run.assert_not_called()


class ReusePipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec=importlib.util.spec_from_file_location('reuse_demo',ROOT/'examples/create_demo.py')
        demo=importlib.util.module_from_spec(spec)
        spec.loader.exec_module(demo)
        cls.temp=tempfile.TemporaryDirectory()
        cls.ep=demo.create_demo(Path(cls.temp.name)/'episode')
        cls.config=json.loads((cls.ep/'project.json').read_text())
        cls.timeline=json.loads((cls.ep/'timeline.json').read_text())

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def cli(self,command,*flags):
        return subprocess.run([sys.executable,str(ROOT/'tools/dm_project.py'),command,
                               str(self.ep),*flags],capture_output=True,text=True)

    def test_force_cannot_bypass_and_outputs_survive(self):
        doc=copy.deepcopy(self.timeline)
        first=doc['shots'][0]
        first.update(start=0,end=1,duration=1,frames=30,source_in=0,source_out=1)
        second={**first,'id':'S02','start':1,'end':2,'source_in':0.5,'source_out':1.5}
        doc['shots']=[first,second]
        (self.ep/'timeline.json').write_text(json.dumps(doc))
        final=self.ep/'outputs'/self.config['output_name']
        final.write_bytes(b'previous output')
        for command,flags in [('validate',()),('render',('--force','--overwrite'))]:
            result=self.cli(command,*flags)
            self.assertEqual(result.returncode,2,result.stdout+result.stderr)
            report=json.loads((self.ep/'outputs/QA_preflight.json').read_text())
            self.assertIn('SCENE_REUSE','\n'.join(report['errors']))
            self.assertEqual(final.read_bytes(),b'previous output')

    def test_real_music_mix_and_approved_audio(self):
        (self.ep/'timeline.json').write_text(json.dumps(self.timeline))
        music=self.ep/'inputs/music.wav'
        subprocess.run(['ffmpeg','-y','-v','error','-f','lavfi','-i',
                        'sine=frequency=220:duration=0.5','-ar','48000',str(music)],check=True)
        for approved in (False,True):
            config={**self.config,'music':'inputs/music.wav'}
            if approved:
                config['approved_audio']=self.config['voice']
            (self.ep/'project.json').write_text(json.dumps(config))
            result=self.cli('render','--overwrite')
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
            info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams',
                '-show_format','-of','json',str(self.ep/'outputs'/self.config['output_name'])]))
            self.assertTrue(any(s['codec_type']=='audio' for s in info['streams']))
            self.assertAlmostEqual(float(info['format']['duration']),2,delta=.05)


if __name__ == '__main__':
    unittest.main()
