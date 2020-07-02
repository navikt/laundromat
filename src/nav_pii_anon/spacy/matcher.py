import spacy
from spacy.tokens import Doc
from spacy import Matcher


class SpacyMatcher():
    def __init__(self, doc, model):
        self.doc = doc
        self.model = model

    def get_list(self):
        """

        :return: returns list of what to match and label
        """
        return NotImplemented()

    def match_list(self):
        """

        :return: match position and label
        """
        matcher = Matcher(model.vocab)
        matcher(self.doc)

        return NotImplemented()