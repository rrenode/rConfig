import unittest
from rConfig.Rsecrets import Secrets

class TestSecrets(unittest.TestCase):
    
    def test_load_secrets(self):
        # Mock loading secrets for testing
        Secrets.secrets_data = {'TEST_SECRET': 'secret_value'}
        self.assertEqual(Secrets.get('TEST_SECRET'), 'secret_value')
        
    def test_missing_secret(self):
        Secrets.secrets_data = {'TEST_SECRET': 'secret_value'}
        self.assertIsNone(Secrets.get('NON_EXISTENT_SECRET'))

if __name__ == '__main__':
    unittest.main()
