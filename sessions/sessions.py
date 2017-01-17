import logging
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search
from session_handler_config_helper import SessionHandlerConfigHelper


class SessionHandler(object):
    def __init__(self):
        config_helper = SessionHandlerConfigHelper("sessions_config.json")
        logging.basicConfig(
            filename=str(config_helper.get_logging_path() + "SessionHandler" + str(datetime.now().date()) + ".log")
        )
        self.logger = logging.getLogger("SessionHandler")
        self.logger.info("Initialized configuration from file")

        self.client = Elasticsearch(hosts=config_helper.get_hosts())
        self.logger.info("Using ElasticSearch hosts: {}",config_helper.get_hosts())

        self.active_sessions_index = config_helper.get_active_sessions_index()
        self.logger.info("Using active sessions index: {}", self.active_sessions_index)

        self.past_sessions_index = config_helper.get_past_sessions_index()
        self.logger.info("Using past sessions index: {}", self.past_sessions_index)

        self.past_type = config_helper.get_past_sessions_type()
        self.logger.info("ElasticSearch type used: {}", self.past_type)

        self.search_threshold = config_helper.get_search_threshold()
        self.logger.info("ElasticSearch search score threshold: {}", self.search_threshold)

    def add(self, session_id, question, answer, feeling):
        doc = dict()
        doc["input"] = question
        doc["output"] = answer
        doc["feeling"] = feeling
        doc["timestamp"] = datetime.now()
        res = self.client.index(index=self.active_sessions_index, doc_type=session_id, body=doc)
        if res['created'] is True:
            return True
        else:
            self.logger.error("Server returned false for session {}, message {}", str(session_id), str(doc))
            return False

    def get_old_session(self, session_id):
        server_response = self.client.get(self.past_sessions_index, session_id)
        return server_response["doc"]

    def check_repeat_question(self, session_id, question):
        search_query = Search().using(self.client) \
            .index(self.active_sessions_index) \
            .doc_type(session_id) \
            .query('match', input=question)

        most_certain_hit = search_query.execute()[0]
        if most_certain_hit.meta.score > self.search_threshold:
            return True
        return False

    def delete_session(self, session_id):
        self.client.delete_by_query(
            index=self.active_sessions_index,
            doc_type=session_id,
            body={
                "query": {
                    "match_all": {}
                }
            }
        )


handler = SessionHandler()
