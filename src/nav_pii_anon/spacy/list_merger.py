from spacy.tokens import Doc

def merger(doc):
    """
    Assumes that the lists can contain no more than one duplicate of each entity
    """
    list_ner, list_regex = doc.ents, doc._.ents_regex

    #Remove overlap from regex list
    correct_regex = list_regex
    for ent_a in list_regex:
        for ent_b in list_regex:
            if (ent_a.start < ent_b.end < ent_a.end) or (ent_a.end > ent_b.start > ent_a.start):
                if(len(ent_a.text)>len(ent_b.text)) and ent_b in correct_regex:
                    correct_regex.remove(ent_b)
                elif(len(ent_a.text)<len(ent_b.text)) and ent_a in correct_regex:
                    correct_regex.remove(ent_a)

    merged = []
    for ent_ner in list_ner:
        overlap = False
        for ent_regex in correct_regex:
            if ent_ner.start == ent_regex.start and ent_ner.end == ent_regex.end:
                #Keeps the previous entity and discards the new one
                if (ent_ner not in merged) and (ent_regex not in merged):
                    merged.append(ent_ner)
                overlap = True
            elif (ent_ner.start < ent_regex.end < ent_ner.end) or (ent_ner.end > ent_regex.start > ent_ner.start):
                #Creates a new entity with the label overlap
                start = min(ent_ner.start_char, ent_regex.start_char)
                end = max(ent_ner.end_char, ent_regex.end_char)
                new_ent = doc.char_span(start, end, label=ent_ner.label_)
                merged += [new_ent]
                overlap = True
        if not overlap:
            merged.append(ent_ner)
    for ent_regex in correct_regex:
        overlap = False
        for ent_ner in list_ner:
            if ent_ner.start == ent_regex.start and ent_ner.end == ent_regex.end:
                overlap = True
            elif (ent_ner.start < ent_regex.end < ent_ner.end) or (ent_ner.end > ent_regex.start > ent_ner.start):
                overlap = True
        if not overlap:
            merged.append(ent_regex)
    doc.ents = merged
    return doc