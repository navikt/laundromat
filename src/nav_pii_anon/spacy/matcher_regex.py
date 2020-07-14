import re
from nav_pii_anon.spacy.regex_formatter import regex_formatter


def match_func(doc):
    expression_list = regex_formatter()
    ents_list = []
    for expression in expression_list:
        print(expression['label'])
        for match in re.finditer(expression['pattern'][0]['TEXT']['REGEX'], doc.text):
            start, end = match.span()
            span = doc.char_span(start, end, label=expression['label'])
            try:
                doc.ents = list(doc.ents) + [span]
            except ValueError:
                # Here there should be a function to solve overlaps of entities
                print('Overlapping ents')

    return doc
