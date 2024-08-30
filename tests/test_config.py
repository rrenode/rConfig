import unittest
from rConfig.config import Paths, DevConfig, config, config_property

class TestConfig(unittest.TestCase):
    
    def test_dev_config(self):
        @config
        class TestClass:
            TEST_VAR: int = 10
        
        self.assertEqual(TestClass.TEST_VAR, 10)

    def test_config_loading(self):
        @config
        class TestClass:
            TEST_VAR: int = 10
        
        self.assertEqual(TestClass.TEST_VAR, 10)

    def test_cls_config_property(self):
        @config
        class TestClass:
            OG_VAR: int = 10

            @config_property
            def TEST_VAR(cls):
                return cls.OG_VAR + 5

        self.assertEqual(TestClass.TEST_VAR, 15)

if __name__ == '__main__':
    unittest.main()