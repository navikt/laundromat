from laundromat.regex_engine.regex_base import RegexBase
import datetime



class RegexGeneric(RegexBase):

    def __init__(self, pattern = None, context = None, label = None):
        if not pattern:
            raise ValueError("Your RegEx must have a value")
        if not context:
            raise ValueError("Your RegEx must have a context")
        if not label:
            raise ValueError("Your RegEx must have a label")
        
        self.__regex_pattern = pattern
        self.__context = context
        self.__label = label

    
    @property
    def regex_pattern(self):
        return self.__regex_pattern
            

    @property
    def context(self):
        return self.__context

    @property
    def label(self):
        return self.__label

    @property
    def score(self):
        return 1

    def validate(self):
        pass