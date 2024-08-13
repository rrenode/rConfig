from .config import Paths

class Secrets:
    secrets_data = None
    
    @staticmethod
    def load_secrets():
        secrets_path = Paths.SECRETS_PATH
        config_path = Paths.CONFIG_PATH
        if secrets_path == config_path:
            raise ValueError("SECRETS_PATH and CONFIG_PATH cannot be the same.")
        
        try:
            with open(secrets_path, 'r') as file:
                Secrets.secrets_data = {}
                for line in file:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    key, value = line.split('=', 1)
                    Secrets.secrets_data[key.strip()] = value.strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"The secrets file '{secrets_path}' was not found")
        except Exception as e:
            raise ValueError(f"Error loading secrets file: {e}")
    
    @staticmethod
    def get(var_name):
        if Secrets.secrets_data is None:
            Secrets.load_secrets()
        return Secrets.secrets_data.get(var_name)
