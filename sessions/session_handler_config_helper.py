from config_helper import ConfigHelper
import os


class SessionHandlerConfigHelper(ConfigHelper):
    def get_hosts(self):
        return self.get_value('elasticsearch_hosts')

    def get_active_sessions_index(self):
        return self.get_value('active_sessions')

    def get_past_sessions_index(self):
        return self.get_value('past_sessions')

    def get_past_sessions_type(self):
        return self.get_value('past_ES_type')

    def get_search_threshold(self):
        return self.get_value('search_threshold')

    def get_logging_path(self):
        path = self.get_value('logging_path')
        if not os.path.exists(path):
            os.mkdir(self.get_value('logging_path'))
        return path
