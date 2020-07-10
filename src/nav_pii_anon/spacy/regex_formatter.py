from enum import Enum
from nav_pii_anon.regex_container import RegexEngines


def regex_formatter(entities: list = None):
    """
    Formats desired entities such that they can be fed to SpaCy's entity ruler
    :param entities: a list of strings denoting which entities one wishes to include in the model
    """
    labels = all_possible_labels()
    if not entities:
        regex = [ent.value.regex_pattern for ent in RegexEngines]
        form = []
        for label, reg in zip(labels, regex):
            form += [{"label": label, "pattern": [{"TEXT": {"REGEX": reg}}]}]
        return form
    elif set(entities).issubset(set(labels)):
        regex = [ent.value.regex_pattern for ent in RegexEngines if ent.value.label in entities]
        form = []
        for label, reg in zip(labels, regex):
            form += [{"label": label, "pattern": [{"TEXT": {"REGEX": reg}}]}]
        return form
    # TODO Else if they add entities that do not exist yet


def new_entity(label: str, match: str):
    pass


def all_possible_labels():
    """
    Prints all possible entities
    """
    return [engine.value.label for engine in RegexEngines]
