from enum import Enum
from nav_pii_anon.regex_container import RegexEngines

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
