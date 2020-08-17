
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


