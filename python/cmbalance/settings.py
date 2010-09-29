import ConfigParser

class SettingsSection(object):
    def __init__(self, config, section):
        self.config = config
        self.section = section
        self.items = {}
        self._load_values(self.config.items(section))

    def _load_values(self, values):
        for k, v in values:
            self.items[k] = v

    def __getattr__(self, attr):
        return self.items[attr]

    def __repr__(self):
        return "<SettingsSection (name: %s)>" % (self.section)

class Settings(object):
    def __init__(self, fn):
        self.config = ConfigParser.RawConfigParser()
        self.config.read(fn)

    def __getattr__(self, attr):
        return SettingsSection(self.config, attr)
