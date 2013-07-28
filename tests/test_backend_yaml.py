import unittest
import tempfile
import shutil
import sys, os
import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import multiconfig

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.sample_config={
            "strVar": "Hello world",
            "intVar": 42,
            "floatVar": 3.14,
            "listVar": ["foo", "bar"],
            "dictVar": {
                "strVar": "Goodbye World",
                "intVar": 24,
                "floatVar": 4.13,
                "listVar": ["baz", "asdf"],
            }
        }
        self.sample_config_2={
            "floatVar": 1.23,
            "dictVar": {
                "strVar": "foobar"
            }
        }
        self.temp_dir=tempfile.mkdtemp()
        with open(os.path.join(self.temp_dir, "sample_config.yml"), "w") as fp:
            yaml.dump(self.sample_config, fp)
        with open(os.path.join(self.temp_dir, "sample_config_2.yaml"), "w") as fp:
            yaml.dump(self.sample_config_2, fp)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_loadOne(self):
        config=multiconfig.getConfig("test_loadOne")

        config.load(os.path.join(self.temp_dir, "sample_config.yml"))

        self.assertEqual(config.get("strVar"), self.sample_config["strVar"])
        self.assertEqual(config.get("intVar"), self.sample_config["intVar"])
        self.assertEqual(config.get("floatVar"), self.sample_config["floatVar"])
        self.assertEqual(config.get("listVar"), self.sample_config["listVar"])
        self.assertEqual(len(config.get("listVar")), len(self.sample_config["listVar"]))

        self.assertEqual(config.get("dictVar/strVar"), self.sample_config["dictVar"]["strVar"])
        self.assertEqual(config.get("dictVar/intVar"), self.sample_config["dictVar"]["intVar"])
        self.assertEqual(config.get("dictVar/floatVar"), self.sample_config["dictVar"]["floatVar"])
        self.assertEqual(config.get("dictVar/listVar"), self.sample_config["dictVar"]["listVar"])
        self.assertEqual(len(config.get("dictVar/listVar")), len(self.sample_config["dictVar"]["listVar"]))

    def test_loadTwo(self):
        config=multiconfig.getConfig("test_loadTwo")

        config.load(os.path.join(self.temp_dir, "sample_config.yml"))
        config.load(os.path.join(self.temp_dir, "sample_config_2.yaml"))

        self.assertEqual(config.get("strVar"), self.sample_config["strVar"])
        self.assertEqual(config.get("intVar"), self.sample_config["intVar"])
        self.assertEqual(config.get("floatVar"), self.sample_config_2["floatVar"])
        self.assertEqual(config.get("listVar"), self.sample_config["listVar"])
        self.assertEqual(len(config.get("listVar")), len(self.sample_config["listVar"]))

        self.assertEqual(config.get("dictVar/strVar"), self.sample_config_2["dictVar"]["strVar"])
        self.assertEqual(config.get("dictVar/intVar"), self.sample_config["dictVar"]["intVar"])
        self.assertEqual(config.get("dictVar/floatVar"), self.sample_config["dictVar"]["floatVar"])
        self.assertEqual(config.get("dictVar/listVar"), self.sample_config["dictVar"]["listVar"])
        self.assertEqual(len(config.get("dictVar/listVar")), len(self.sample_config["dictVar"]["listVar"]))

if __name__ == '__main__':
    unittest.main()