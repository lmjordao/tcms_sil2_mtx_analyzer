"""
Usage:
ConfigLoader.getinstance().config_section_map('section')['field']
"""

from configparser import ConfigParser


class ConfigLoader:
    CONFIG_FILENAME = 'config.ini'
    __instance = None

    def __init__(self):
        self.config_parser = ConfigParser()
        self.config_parser.read(ConfigLoader.CONFIG_FILENAME)

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ConfigLoader, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    @staticmethod
    def getinstance():

        if ConfigLoader.__instance is None:
            ConfigLoader()
        return ConfigLoader.__instance

    def config_section_map(self, section):
        dict1 = {}
        options = self.config_parser.options(section)
        for _option in options:
            try:
                dict1[_option] = self.config_parser.get(section, _option)
                if dict1[_option] == -1:
                    print('[!] Skipping ' + _option)
            except:
                print('[!] Exception on ' + _option)
                dict1[_option] = None
        return dict1
