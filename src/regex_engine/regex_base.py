from abc import ABC, abstractmethod
import re


class RegexBase(ABC):

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

    def find_all(self, text: str):

        for hit in re.finditer(self.regex_pattern, text):
            print(hit.span())

    @abstractmethod
    def validate(self):
        return NotImplementedError()

    def sub_all(self, text: str):
        return re.sub(self.regex_pattern, f'[{self.label}]', text)
