import logging
from conversation.statement import Statement
from conversation.response import Response

class Trainer(object):
    """
    Base class for all other trainer classes.
    """

    def __init__(self, storage, **kwargs):
        self.storage = storage
        self.logger = logging.getLogger(__name__)

    def train(self, *args, **kwargs):
        """
        This class must be overridden by a class the inherits from 'Trainer'.
        """
        raise self.TrainerInitializationException()

    def get_or_create(self, statement_text):
        """
        Return a statement if it exists.
        Create and return the statement if it does not exist.
        """
        statement = self.storage.find(statement_text)

        if not statement:
            statement = Statement(statement_text)

        return statement

    class TrainerInitializationException(Exception):
        """
        Exception raised when a base class has not overridden
        the required methods on the Trainer base class.
        """

        def __init__(self, value=None):
            default = (
                'A training class must specified before calling train(). ' +
                'See http://chatterbot.readthedocs.io/en/stable/training.html'
            )
            self.value = value or default

        def __str__(self):
            return repr(self.value)

    def _generate_export_data(self):
        result = []

        for statement in self.storage.filter():
            for response in statement.in_response_to:
                result.append([response.text, statement.text])

        return result

    def export_for_training(self, file_path='./export.json'):
        """
        Create a file from the database that can be used to
        train other chat bots.
        """
        from jsondb.db import Database
        database = Database(file_path)
        export = {'export': self._generate_export_data()}
        database.data(dictionary=export)


class ListTrainer(Trainer):
    """
    Allows a chat bot to be trained using a list of strings
    where the list represents a conversation.
    """

    def train(self, conversation):
        """
        Train the chat bot based on the provided list of
        statements that represents a single conversation.
        """
        statement_history = []

        for text in conversation:
            statement = self.get_or_create(text)

            if statement_history:
                statement.add_response(
                    Response(statement_history[-1].text)
                )

            statement_history.append(statement)
            self.storage.update(statement, force=True)


class ChatterBotCorpusTrainer(Trainer):
    """
    Allows the chat bot to be trained using data from the
    ChatterBot dialog corpus.
    """

    def __init__(self, storage, **kwargs):
        super(ChatterBotCorpusTrainer, self).__init__(storage, **kwargs)
        from corpus.corpus import Corpus

        self.corpus = Corpus()

    def train(self, *corpora):
        trainer = ListTrainer(self.storage)

        # Allow a list of coupora to be passed instead of arguments
        if len(corpora) == 1:
            if isinstance(corpora[0], list):
                corpora = corpora[0]

        for corpus in corpora:
            corpus_data = self.corpus.load_corpus(corpus)
            for data in corpus_data:
                for pair in data:
                    trainer.train(pair)


class UbuntuCorpusTrainer(Trainer):
    """
    Allow chatbots to be trained with the data from
    the Ubuntu Dialog Corpus.
    """

    def __init__(self, storage, **kwargs):
        super(UbuntuCorpusTrainer, self).__init__(storage, **kwargs)
        import os

        self.data_download_url = kwargs.get(
            'ubuntu_corpus_data_download_url',
            'http://cs.mcgill.ca/~jpineau/datasets/ubuntu-corpus-1.0/ubuntu_dialogs.tgz'
        )

        self.data_directory = kwargs.get(
            'ubuntu_corpus_data_directory',
            './data/'
        )

        # Create the data directory if it does not already exist
        if not os.path.exists(self.data_directory):
            os.makedirs(self.data_directory)

    def download(self, url, show_status=True):
        """
        Download a file from the given url.
        Show a progress indicator for the download status.
        Based on: http://stackoverflow.com/a/15645088/1547223
        """
        import os
        import sys
        import requests

        file_name = url.split('/')[-1]
        file_path = os.path.join(self.data_directory, file_name)

        # Do not download the data if it already exists
        if os.path.exists(file_path):
            self.logger.info('File is already downloaded')
            return file_path

        with open(file_path, 'wb') as open_file:
            print('Downloading %s' % file_name)
            response = requests.get(url, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:
                # No content length header
                open_file.write(response.content)
            else:
                download = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    download += len(data)
                    open_file.write(data)
                    if show_status:
                        done = int(50 * download / total_length)
                        sys.stdout.write('\r[%s%s]' % ('=' * done, ' ' * (50 - done)))
                        sys.stdout.flush()

        return file_path

    def extract(self, file_path):
        """
        Extract a tar file at the specified file path.
        """
        import os
        import tarfile

        dir_name = os.path.split(file_path)[-1].split('.')[0]

        extracted_file_directory = os.path.join(
            self.data_directory,
            dir_name
        )

        # Do not extract if the extracted directory already exists
        if os.path.isdir(extracted_file_directory):
            return False

        self.logger.info('Starting file extraction')

        def track_progress(members):
            for member in members:
                # this will be the current file being extracted
                yield member
                print('Extracting {}'.format(member.path))

        with tarfile.open(file_path) as tar:
            tar.extractall(path=self.data_directory, members=track_progress(tar))

        self.logger.info('File extraction complete')

        return True

    def train(self):
        import glob
        import csv
        import os

        # Download and extract the Ubuntu dialog corpus
        corpus_download_path = self.download(self.data_download_url)

        self.extract(corpus_download_path)

        extracted_corpus_path = os.path.join(
            self.data_directory,
            os.path.split(corpus_download_path)[-1].split('.')[0],
            '**', '*.tsv'
        )

        for file in glob.iglob(extracted_corpus_path):
            self.logger.info('Training from: {}'.format(file))

            with open(file, 'r') as tsv:
                reader = csv.reader(tsv, delimiter='\t')

                statement_history = []

                for row in reader:
                    if len(row) > 0:
                        text = row[3]
                        statement = self.get_or_create(text)
                        print(text, len(row))

                        statement.add_extra_data('datetime', row[0])
                        statement.add_extra_data('speaker', row[1])

                        if row[2].strip():
                            statement.add_extra_data('addressing_speaker', row[2])

                        if statement_history:
                            statement.add_response(
                                Response(statement_history[-1].text)
                            )

                        statement_history.append(statement)
                        self.storage.update(statement, force=True)
