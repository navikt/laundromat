import re
from nav_pii_anon.spacy.regex_formatter import regex_engines


def match_func(doc):
    """
    Uses regex to find patterns and label them with the given label.
    :param doc: The text in doc-format
    :return: doc: The text in doc-format with added entities
    """
    entity_list = regex_engines()
    for entity in entity_list:

        for match in re.finditer(entity.regex_pattern, doc.text):
            start, end = match.span()
            span = doc.char_span(start, end, label=entity.label)

            if not overlap_check(span, doc):
                doc.ents = list(doc.ents) + [span]
            else:
                overlap_resolver(span, doc)

    return doc


def overlap(span, doc):
    """
    Checks if two entities overlap
    :param span: A span of tokens, that the regex wants to match to a label
    :param doc: The text in doc-format
    :return: Boolean: Overlap indicator
    """
    if span is not None:
        for ent in doc.ents:
            if span.start in range(ent.start, ent.end + 1) or span.end in range(ent.start, ent.end + 1):

                if span.start < ent.end or span.end > ent.start:
                    pass

                return True
            else:
                return False
    else:
        print('span is None')
        return True
