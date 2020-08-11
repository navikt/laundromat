import re

from abc import ABC, abstractmethod
from spacy.tokens import Doc


class RegexBase(ABC):
    """
    Abstract class that RegEx classes inherit from.
    """
    @property
    @abstractmethod
    def regex_pattern(self):
        """
        :return: Returns the regex pattern of the class
        """
        return NotImplementedError()

    @property
    @abstractmethod
    def label(self):
        """
        :return: Return label to substitute with
        """
        return NotImplementedError()

    @property
    @abstractmethod
    def score(self):
        return NotImplementedError()

    @property
    @abstractmethod
    def context(self):
        """
        :return: List of pattern groups
        """
        return NotImplementedError()

    @abstractmethod
    def validate(self):
        return NotImplementedError()

    def sub_all(self, text: str):
        return re.sub(self.regex_pattern, f'[{self.label}]', text)

    def find_all(self, text: str):
        hits = []
        for hit in re.finditer(self.regex_pattern, text):
            hits.append({
                'start': hit.start(),
                'end': hit.end(),
                'hit': hit.group(),
                'label': self.label
                         })

        return hits

    def spacy_pipe_func(self, doc: Doc) -> Doc:
        """
        :param doc: Spacy doc
        :return: Spacy doc
        """
        pass
