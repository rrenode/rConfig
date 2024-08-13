import unittest
from rConfig.config import Paths, DevConfig, config

class TestConfig(unittest.TestCase):
    
    def test_dev_config(self):
        @config
        class TestClass:
            TEST_VAR: int = 10
        
        self.assertEqual(TestClass.TEST_VAR, 10)

    def test_config_loading(self):
        # Assuming you have a method to mock config loading
        @config
        class TestClass:
            TEST_VAR: int = 10
        
        # Example test to ensure a config value is loaded correctly
        self.assertEqual(TestClass.TEST_VAR, 10)

if __name__ == '__main__':
    unittest.main()