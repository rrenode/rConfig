from .config import Paths, rError

class Secrets:
    secrets_data = None
    
    @staticmethod
    def load_secrets():
        secrets_path = Paths.rSECRETS_PATH
        config_path = Paths.rCONFIG_PATH
        if secrets_path == config_path:
            err_msg = "SECRETS_PATH and CONFIG_PATH cannot be the same."
            raise rError(ValueError, err_msg)
        
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
            err_msg = f"The secrets file '{secrets_path}' was not found"
            raise rError(FileNotFoundError, err_msg)
        except IOError as err:
            err_msg = f"Could not load secrets file: {err}"
            raise rError(IOError, err_msg)
        except Exception as err:
            err_msg = f"An unhandled exception occured when attempting to load .secrets file: {err}"
            raise rError(Exception, err_msg)
    
    @staticmethod
    def get(var_name : str):
        if Secrets.secrets_data is None:
            Secrets.load_secrets()
        if not var_name in Secrets.secrets_data:
            err_msg = f"Expected secret value was not found in secrets file."
            raise rError(ValueError, err_msg)
        return Secrets.secrets_data.get(var_name)
