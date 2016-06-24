"""
Wrapper for configuration and properties files
"""
import os
from ConfigParser import SafeConfigParser


class Properties(object):
    """
    Handles configuration and properties
    """
    path = os.path.dirname(os.path.realpath(__file__)) + '/redeye.config'

    def __init__(self, key):
        """
        Initializes properties file path,
        config parser instance and module
        """
        self._config = SafeConfigParser()
        self._key = key

    @classmethod
    def set_config_dir(cls, new_path):
        """
        Defines a new configuration file and
        directory
        """
        cls.path = new_path

    def section(self, name):
        """
        Returns a given section name
        """
        if self._config.read(self.path) and \
                self._config.has_section(self._key):
            return self._config.get(self._key, name)

    def multi_value(self, section):
        """
        Return a multi value section as a list
        """
        _section = self.section(section)

        _section = [element.strip() for element in _section.split(',')]

        return _section
