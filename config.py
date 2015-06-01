import json
from platform.settings import Settings

class Config:
    def __init__(self, settings = Settings(), map = None):
        if map is None:
            with open(settings.CONFIG_FILE, 'r') as f:
                self.params = json.load(f)
        else:
            self.params = map

    def serialize(self):
        with open(Settings().CONFIG_FILE, 'w') as f:
            json.dump(self.params, f, indent=4, sort_keys=True)

    def commandparams(self, p) -> {}:
        # for param, value in self.params['commandparams'].items():
        #     if path.find(param) != -1:
        #         return value
        return {}

    instance = None