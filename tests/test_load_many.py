import unittest
import tempfile
import shutil
import sys, os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import multiconfig

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.sample_configs = [
            {
                'foo': 'value 1',
                'bar1': 'value 1',
            },
            {
                'foo': 'value 2',
                'bar2': 'value 2',
            },
            {
                'foo': 'value 3',
                'bar3': 'value 3',
            },
            {
                'foo': 'value 4',
                'bar4': 'value 4',
            },
        ]
        self.temp_dirs = []
        for config in self.sample_configs:
            temp_dir = tempfile.mkdtemp()
            self.temp_dirs.append(temp_dir)
            with open(os.path.join(temp_dir, 'sample_config.json'), 'w') as fp:
                json.dump(config, fp)

    def tearDown(self):
        for temp_dir in self.temp_dirs:
            shutil.rmtree(temp_dir)

    def test_loadMany_filenames(self):
        config = multiconfig.getConfig('test_loadMany_filenames')

        config.loadMany(candidate_directories=self.temp_dirs, candidate_filenames=['sample_config.json'])

        self.assertEqual(config.get('foo'), 'value 4')
        self.assertEqual(config.get('bar1'), 'value 1')
        self.assertEqual(config.get('bar2'), 'value 2')
        self.assertEqual(config.get('bar3'), 'value 3')
        self.assertEqual(config.get('bar4'), 'value 4')

    def test_loadMany_fileexts(self):
        config = multiconfig.getConfig('test_loadMany_fileexts')

        config.loadMany(candidate_directories=self.temp_dirs, candidate_filenames=['sample_config'], candidate_extensions=['json'])

        self.assertEqual(config.get('foo'), 'value 4')
        self.assertEqual(config.get('bar1'), 'value 1')
        self.assertEqual(config.get('bar2'), 'value 2')
        self.assertEqual(config.get('bar3'), 'value 3')
        self.assertEqual(config.get('bar4'), 'value 4')

    def test_loadMany_files(self):
        config = multiconfig.getConfig('test_loadMany_files')

        config.loadMany(candidate_files=[os.path.join(d, 'sample_config.json') for d in self.temp_dirs])

        self.assertEqual(config.get('foo'), 'value 4')
        self.assertEqual(config.get('bar1'), 'value 1')
        self.assertEqual(config.get('bar2'), 'value 2')
        self.assertEqual(config.get('bar3'), 'value 3')
        self.assertEqual(config.get('bar4'), 'value 4')

    def test_loadMany_nonefound(self):
        config = multiconfig.getConfig('test_loadMany_fileexts')

        with self.assertRaises(multiconfig.ConfigurationError):
            config.loadMany(candidate_directories=['/foo'], candidate_filenames=['sample_config'], candidate_extensions=['json'])

if __name__ == '__main__':
    unittest.main()