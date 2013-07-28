import unittest
import sys, os

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

    def test_getConfig(self):
        config1=multiconfig.getConfig("alsjfalksej")
        config2=multiconfig.getConfig("alsjfalksej")
        self.assertIs(config1, config2)
        config3=multiconfig.getConfig("qwerty")
        self.assertIsNot(config1, config3)
        self.assertIsNot(config2, config3)

    def test_getKeys(self):
        config=multiconfig.getConfig("test_getKeys")
        config.configuration=self.sample_config

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

    def test_getMissingKey_NoDefault(self):
        config=multiconfig.getConfig("test_getMissingKey_NoDefault")
        config.configuration=self.sample_config

        self.assertIsNone(config.get("ThisKeyDoesntExist"))

    def test_getMissingKey_Default(self):
        config=multiconfig.getConfig("test_getMissingKey_Default")
        config.configuration=self.sample_config

        self.assertIs(config.get("ThisKeyDoesntExist", default=0), 0)

    def test_getMissingKey_Exception(self):
        config=multiconfig.getConfig("test_getMissingKey_Exception")
        config.configuration=self.sample_config

        with self.assertRaises(KeyError):
            config.get("ThisKeyDoesntExist", do_except=True)

    def test_merge(self):
        config=multiconfig.getConfig("test_merge")
        merged=config._merged(self.sample_config, self.sample_config_2)

        self.assertEqual(merged["strVar"], self.sample_config["strVar"])
        self.assertEqual(merged["intVar"], self.sample_config["intVar"])
        self.assertEqual(merged["floatVar"], self.sample_config_2["floatVar"])
        self.assertEqual(merged["listVar"], self.sample_config["listVar"])
        self.assertEqual(len(merged["listVar"]), len(self.sample_config["listVar"]))

        self.assertEqual(merged["dictVar"]["strVar"], self.sample_config_2["dictVar"]["strVar"])
        self.assertEqual(merged["dictVar"]["intVar"], self.sample_config["dictVar"]["intVar"])
        self.assertEqual(merged["dictVar"]["floatVar"], self.sample_config["dictVar"]["floatVar"])
        self.assertEqual(merged["dictVar"]["listVar"], self.sample_config["dictVar"]["listVar"])
        self.assertEqual(len(merged["dictVar"]["listVar"]), len(self.sample_config["dictVar"]["listVar"]))

if __name__ == '__main__':
    unittest.main()