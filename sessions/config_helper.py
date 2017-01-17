import json


class ConfigHelper(object):
    def __init__(self, config_file):
        self.config_dict = json.load(open(config_file, 'r'))

    def get_value(self, field):
        return self.config_dict[field]
