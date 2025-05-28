import os
import configparser
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_path = Path(__file__).parent / 'settings.ini'
        self._load_config()

    def _load_config(self):
        # Read from INI file
        self.config.read(self.config_path)
        
        # Override with environment variables if they exist
        for section in self.config.sections():
            for key in self.config[section]:
                env_var = f"{section.upper()}_{key.upper()}"
                if env_var in os.environ:
                    self.config[section][key] = os.environ[env_var]

    def get(self, section, key, default=None):
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default

    def getint(self, section, key, default=None):
        try:
            return self.config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default

    def getboolean(self, section, key, default=None):
        try:
            return self.config.getboolean(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return default

# Singleton configuration instance
config = Config()