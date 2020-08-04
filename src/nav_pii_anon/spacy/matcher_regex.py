import re
from nav_pii_anon.spacy.regex_formatter import regex_engines


def match_func(doc):
    """
    Uses regex to find patterns and label them with the given label.

    :param doc: The text in doc-format
    :return: The text in doc-format with added entities
    """
    entity_list = regex_engines()
    for entity in entity_list:
        for match in re.finditer(entity.regex_pattern, doc.text):
            start, end = match.span()
            span = doc.char_span(start, end, label=entity.label)
            if not overlap(span, doc):
                doc.ents = list(doc.ents) + [span]
    return doc

def overlap(span, doc):
    for entity in doc.ents:
        if (entity.start <= span.start <= entity.end) or (entity.start <=span.end <=entity.end):
            return True