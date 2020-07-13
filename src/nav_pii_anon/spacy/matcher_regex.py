import re
from nav_pii_anon.spacy.regex_formatter import regex_formatter


def match_func(doc):
    expression_list = regex_formatter()
    for expression in expression_list:
        for match in re.finditer(expression['pattern'][0]['TEXT']['REGEX'], doc.text):
            start, end = match.span()
            span = doc.char_span(start, end, label=expression['label'])
            doc.ents = list(doc.ents) + [span]

    return doc
