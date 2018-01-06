# JsonConfig.py
import json


class JsonConfig():
    def __init__(self, filename):
        self.filename = filename

    def get_file(self):
        with open(self.filename, 'r') as f:
            return json.load(f)

    def display_file(self):
        config = self.get_file()
        print(json.dumps(config, indent=4, sort_keys=True))

    def get(self, key):
        config = self.get_file()
        if key in config:
            return config[key]

    def set(self, key, value):
        config = self.get_file()
        config[key] = value
        with open(self.filename, 'w') as f:
            json.dump(config, f)
