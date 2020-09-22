from data_structures.russian_tweet_data import RussianTweetData

TWEET_DIR = "../data/russian-troll-tweets"


class DatasetReader:
    def __init__(self, document_location):
        self.document_location: str = document_location

    def load_documents(self):
        pass

    def convert_document(self):
        raise NotImplementedError


class RussianTweetReader(DatasetReader):
    def __init__(self, document_location: str = TWEET_DIR):
        super().__init__(document_location)

    def convert_document(self):
        pass
