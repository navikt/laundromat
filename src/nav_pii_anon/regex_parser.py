from enum import Enum

from nav_pii_anon.regex_engine.fnr import RegexFnr
from nav_pii_anon.regex_engine.credit_card import RegexCreditCard


class RegexEngines(Enum):
    FNR = RegexFnr()
    CREDIT_CARD = RegexCreditCard()


def all_possible_labels():
    return [engine.value.label for engine in RegexEngines]


def find_all_hits(text: str, labels: list = None) -> list:
    hits = []

    selected_labels = []
    if labels:
        selected_labels.extend(labels)
    else:
        selected_labels.extend(all_possible_labels())

    engines = [engine.value for engine in RegexEngines if engine.value.label in selected_labels]

    for engine in engines:
        hits.extend(engine.find_all(text))

    return hits


def replace_hits(text: str, labels: list = None) -> str:
    hits = find_all_hits(text, labels)

    for hit in hits:
        text = text.replace(hit.get('hit'), f"[{hit.get('label')}]", 1)

    return text

