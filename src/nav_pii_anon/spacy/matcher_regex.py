import re
from nav_pii_anon.spacy.regex_formatter import regex_engines
from spacy.tokens import Doc, Span, Token

def match_func(doc):
    """
    Uses regex to find patterns and label them with the given label.

    :param doc: The text in doc-format
    :return: The text in doc-format with added entities
    """
    entity_list = regex_engines()
    spans = []
    for entity in entity_list:
        for match in re.finditer(entity.regex_pattern, doc.text):
            start, end = match.span()
            span = doc.char_span(start, end, label=entity.label)
            spans.append(span)
            if not overlap(span, doc):
                doc.ents = list(doc.ents) + [span]
    if spans is not None:
        for span in spans:
            span.merge()
    return doc

def overlap(span, doc):
    if span is not None:
        for entity in doc.ents:
            if (entity.start <= span.start <= entity.end) or (entity.start <=span.end <=entity.end):
                return True
    else:
        return True