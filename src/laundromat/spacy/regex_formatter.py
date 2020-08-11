from laundromat.regex_engine.fnr import RegexFnr
from laundromat.regex_engine.credit_card import RegexCreditCard
from laundromat.regex_engine.tlfnr import RegexTlfNr
from laundromat.regex_engine.amount import RegexAmount
from laundromat.regex_engine.date_time import RegexDateTime

# TODO Keeping for now, consider removing later

def regex_formatter(entities: list = None):
    """
    Formats desired entities such that they can be fed to SpaCy.

    :param entities: A list of strings denoting which entities one wishes to include in the model.
    """
    labels = all_possible_labels()

    if not entities:
        regex = [ent.regex_pattern for ent in regex_engines()]
        form = []
        for label, reg in zip(labels, regex):
            form += [{"label": label, "pattern": [{"TEXT": {"REGEX": reg}}]}]
        return form
    elif set(entities).issubset(set(labels)):
        regex = [ent.regex_pattern for ent in regex_engines() if ent.label in entities]
        form = []
        for label, reg in zip(labels, regex):
            form += [{"label": label, "pattern": [{"TEXT": {"REGEX": reg}}]}]
        return form
    # TODO Else if they add entities that do not exist yet.


def new_entity(label: str, match: str):
    #TODO Functionality for directly adding classes.
    pass


def all_possible_labels():
    """
    Prints all possible entities
    """
    return [engine.label for engine in regex_engines()]


def regex_engines():
    """
    Calls the different regex classes, and adds them in an ordered way.
    """
    regex_function = [
        RegexFnr(),
        RegexCreditCard(),
        RegexTlfNr(),
        RegexDateTime(),
        RegexAmount()
    ]
    return regex_function
