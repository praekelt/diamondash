import yaml
import json
from os import path
from glob import glob

from diamondash import utils


class ConfigError(Exception):
    """Raised when there is an error parsing a configuration"""


class ConfigMetaClass(type):
    def __new__(mcs, name, bases, dict):
        cls = type.__new__(mcs, name, bases, dict)
        cls.REGISTRY[cls.KEY] = cls

        defaults = {}
        for base in bases:
            if base is not object:
                defaults.update(base.DEFAULTS)

        defaults.update(cls.DEFAULTS)
        cls.DEFAULTS = defaults

        return cls


class Config(object):
    __metaclass__ = ConfigMetaClass

    # Override with a string representing the key used to lookup configuration
    # and defaults relevant for the config type
    KEY = 'base'

    DEFAULTS = {}

    REGISTRY = {}

    def __init__(self, items=None):
        self._items = items or {}

    def __contains__(self, key):
        return key in self._items

    def __getitem__(self, key):
        return self._items[key]

    def __setitem__(self, key, value):
        self._items[key] = value

    @classmethod
    def parse(cls, config_dict):
        return config_dict

    @classmethod
    def from_dict(cls, config_dict):
        config_dict = utils.update_dict(cls.DEFAULTS, config_dict)

        if 'defaults' in config_dict:
            config_dict.update(config_dict['defaults'].get(cls.KEY, {}))

        return cls(cls.parse(config_dict))

    @classmethod
    def from_args(cls, **kwargs):
        return cls.from_dict(kwargs)

    @staticmethod
    def merge_defaults(old, new):
        defaults = {}

        for type_key in (set(old.keys()) | set(new.keys())):
            defaults[type_key] = utils.update_dict(
                old.get(type_key, {}),
                new.get(type_key, {}))

        return defaults

    @classmethod
    def from_file(cls, filename, defaults=None):
        config_dict = yaml.safe_load(open(filename))

        if defaults is not None:
            config_dict['defaults'] = cls.merge_defaults(
                config_dict.get('defaults', {}),
                defaults)

        return cls.from_dict(config_dict)

    @classmethod
    def configs_from_dir(cls, dirname, defaults=None):
        return [
            cls.from_file(filepath, defaults)
            for filepath in glob(path.join(dirname, "*.yml"))]

    def to_dict(self):
        data = {}

        for key, value in self._items.items():
            if isinstance(value, Config):
                data[key] = value.to_dict()
            else:
                data[key] = value

        return data

    def to_json(self):
        return json.dumps(self.to_dict())