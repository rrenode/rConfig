# rConfig

rConfig is a tiny Python library for handling config and secrets, along with some dot env. 

The library currently only handles getting static configs. Future plans involve handling saving configs, a mix of dynamic as well as static config value handling, and eventually multiple config files.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install rConfig.

```bash
pip install rconfig[default]@git+https://github.com/rrenode/rConfig
```

## Usage

### YAML
```yaml
FooConfig:
  NAME: Rob
  SOME_DICT:
    A: Look at me!
    1: 12345
    "nested": [1,2,3,"abc"]
```

### Secrets
```
MY_SECRET=Be very, very sneaky
NOT_SO_SECRET=All secrets are considered strings
```

### DotEnv
```python
DEBUG=True
```

### Python
```python
from rconfig import config, dev_config, config_property, Secrets

# Using dev_config
@dev_config
class EnvVars:
    DEBUG : bool = False

# return True (since it's defined in the .env file above)
EnvVars.DEBUG

# Setting a config with the decorator
@config
class FooConfig:
    VAR_NAME : str = "Some default value here"
    NAME: str = "Rob"
    SOME_DICT : dict = None
    
    # Setting a config_property
    @config_property
    def FOOBAR(cls):
        return cls.NAME + " is cool"

# returns 'Some default value here'
FooConfig.VAR_NAME

# returns 'Rob is cool'
FooConfig.FOOBAR

# Using Secrets
#   returns 'Be very, very sneaky'
Secrets.get("MY_SECRET")

```

## Library Config

The library allows you to configure a few things using the DotEnv file.

### The `.env` file

In the dot env file you can set the paths for the config file and for the secrets file as such:
```python
# The path can be either relative to the project or absolute.
# File extension doesn't matter much, library will read it as a YAML file.
# By default the library looks for config.yml relative to the entry point.
rCONFIG_PATH=path/config.yml

# .secrets is by convention only, realistically you can use any file name with any extension.
# However, the library will only attempt to read it as a text file with key-value pairs.
rSECRETS_PATH=path/.secrets
```

You can also set a debug output mode which if set to true will output more context as to what the library is doing. Setting this to true will enable outputs showing every config var as it is set and what it is set to.
```python
# Capitalization does not matter
rDEBUG=true
```

If you want to disable messages when default values are being used (including when no config file is being used), then you can set the `rSilent` flag to true. For now, this **ONLY** disables these messages.
```python
rSilent=true
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)