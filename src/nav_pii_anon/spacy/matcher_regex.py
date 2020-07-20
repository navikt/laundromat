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

            if not overlap(span, doc):
                doc.ents = list(doc.ents) + [span]
                print(doc.ents)

    return doc


def overlap(span, doc):
    """
    Checks if two entities overlap
    :param span: A span of tokens, that the regex wants to match to a label
    :param doc: The text in doc-format
    :return: Boolean: Overlap indicator
    """
    if span is not None:
        for ent in list(doc.ents):
            #print("This is span and ent:", span, ent)
            #print("This is span range and ent rangte", span.start, span.end, ent.start, ent.end + 1)

            if span.start in range(ent.start, ent.end + 1) or span.end in range(ent.start, ent.end + 1):
                overlap_solver(span, doc, ent)
                #print('TRUE!')
                return True
        #print('FALSE!')
        return False    

    else:
        #print('span is None')
        return True


def overlap_solver(span, doc, ent):
    if span.start == ent.start and span.end == ent.end:
        #TODO solve this scenario
        pass
    elif (span.start < ent.end < span.end) or (span.end > ent.start > span.start):
        start = min(span.start, ent.start)
        end = max(span.end, ent.end)
        doc.ents.remove(ent)
        new_span = doc.char_span(start, end, label="OVERLAP")
        doc.ents = list(doc.ents) + [new_span]
        #print('overlap fixed:', new_span)
    else:
        if len(span.text) > len(ent.text):
            doc.ents.remove(ent)
            doc.ents = list(doc.ents) + [span]
            #print('span is longer than ent')
        else:
            pass
