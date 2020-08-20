import re
from spacy.tokens import Doc, Span, Token
from laundromat.regex_engine.fnr import RegexFnr
from laundromat.regex_engine.credit_card import RegexCreditCard
from laundromat.regex_engine.tlfnr import RegexTlfNr
from laundromat.regex_engine.amount import RegexAmount
from laundromat.regex_engine.date_time import RegexDateTime
from laundromat.regex_engine.generic import RegexGeneric

class RegexMatcher:
    def __init__(self, regex_list = []):
        default_regexes = [RegexFnr(),
                        RegexCreditCard(),
                        RegexTlfNr(),
                        RegexDateTime(),
                        RegexAmount()
                        ]
        self.regexes = []
        for re in default_regexes:
            if re.label in regex_list:
                self.regexes.append(re)
        
    

    def append_regexes(self, regex):
        self.regexes.append(regex)


    def match_func(self, doc):
        """
        Uses regex to find patterns and label them with the given label.

        :param doc: The text in doc-format
        :return: The text in doc-format with added entities
        """
        spans = []

        for entity in self.regexes:
            for match in re.finditer(entity.regex_pattern, doc.text):
                start, end = match.span()
                span = doc.char_span(start, end, label=entity.label)
                if type(span) is not type(None):
                    if not self.overlap(span, doc):
                        spans.append(span)

        doc._.ents_regex = spans
        return doc

    def overlap(self, span, doc):
        """
        :param span: Span of words
        :param doc: The text in doc-format
        :return: True if overlap
        """
        for entity in doc.ents:
            if (entity.start <= span.start <= entity.end) or (entity.start <=span.end <=entity.end):
                return True
        return False



