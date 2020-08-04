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
    """
    Checks if two entities overlap

    :param span: A span of tokens, that the regex wants to match to a label
    :param doc: The text in doc-format
    :return: A boolean overlap indicator
    """
    if span is not None:
        for ent in list(doc.ents):
            if span.start in range(ent.start, ent.end + 1) or span.end in range(ent.start, ent.end + 1):
                overlap_solver(span, doc, ent)
                return True
        return False    
    else:
        return True


def overlap_solver(span, doc, ent):
    """
    The actual overlap solver. If the new entity covers more than the old one, it replaces the old one. If it is a
    partial overlap, it extends both into a new one labeled <OVERLAP>

    :param span: A span of tokens, that the regex wants to match to a label
    :param doc: The text in doc-format
    :param ent: The type of entity
    """
    if span.start == ent.start and span.end == ent.end:
        #Keeps the previous entity and discards the new one
        pass
    elif (span.start < ent.end < span.end) or (span.end > ent.start > span.start):
        #Creates a new entity with the label overlap
        start = min(span.start, ent.start)
        end = max(span.end, ent.end)
        doc.ents = list(doc.ents).remove(ent)
        new_span = doc.char_span(start, end, label="OVERLAP")
        doc.ents = list(doc.ents) + [new_span]
    else:
        if len(span.text) > len(ent.text):
            #Discards the old entity and replaces it with the new one
            doc.ents = list(doc.ents).remove(ent)
            doc.ents = list(doc.ents) + [span]
        else:
            pass
