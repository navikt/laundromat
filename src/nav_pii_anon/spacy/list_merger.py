from spacy.tokens import Doc

def merger(doc):
    """
    Assumes that the lists can contain no more than one duplicate of each entity
    """
    list1, list2 = doc.ents, doc._.ents_regex
    merged = []
    for ent_a in list1:
        overlap = False
        for ent_b in list2:
            if ent_a.start == ent_b.start and ent_a.end == ent_b.end:
                print("Complete overlap")
                #Keeps the previous entity and discards the new one
                merged.append(ent_a)
                overlap = True
            elif (ent_a.start < ent_b.end < ent_a.end) or (ent_a.end > ent_b.start > ent_a.start):
                print("Partial or total overlap")
                #Creates a new entity with the label overlap
                start = min(ent_a.start, ent_b.start)
                end = max(ent_a.end, ent_b.end)
                new_ent = doc.char_span(start, end, label=ent_a.label_)
                merged += [new_ent]
                overlap = True
        if not no_overlap:
            print("No overlap")
            merged.append(ent_a)
            merged.append(ent_b)
        print(merged)
    print(merged)
    doc.ents = merged
    return doc