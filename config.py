import json
from platform.settings import Settings

class Config:
    def __init__(self, settings = Settings(), map = None):
        if map is None:
            with open(settings.CONFIG_FILE, 'r') as f:
                self.params = json.load(f)
        else:
            self.params = map
        self.settings = settings

    def serialize(self):
        with open(self.settings.CONFIG_FILE, 'w') as f:
            json.dump(self.params, f, indent=4, sort_keys=True)

    instance = None
