import pandas as pd
import os
from spacy.pipeline import EntityRuler


def name_list_matcher(nlp):
    """
    Reads csv-files for names and surnames and uses EntityRuler to match to a entity and return to be added to
    the model pipeline
    :param nlp:
    :return: ruler:
    """

    file_list = ['etternavn_ssb.csv',
                 'guttefornavn_ssb.csv',
                 'jentefornavn_ssb.csv']
    names_list = []

    location = os.path.dirname(os.path.realpath(__file__))
    for file_path in file_list:
        my_file = os.path.join(location, 'data', file_path)
        name_df = pd.read_csv(my_file, sep=';')
        names_list.extend(name_df.iloc[:, 0].to_list())

    ruler = EntityRuler(nlp)
    patterns = [{"label": "PER", "pattern": [{"lower": name.lower()}]} for name in names_list]
    print(patterns)
    ruler.add_patterns(patterns)

    return ruler
