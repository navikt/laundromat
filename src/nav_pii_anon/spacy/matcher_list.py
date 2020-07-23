import pandas as pd
import os
from spacy.pipeline import EntityRuler


def csv_list_matcher(nlp):
    """
    Reads csv-files for names and surnames and uses EntityRuler to match to a entity and return to be added to
    the model pipeline
    :param nlp:
    :return: ruler:
    """
    names_list = []
    loc_list = []
    name_path_list = ['etternavn_ssb.csv',
                      'guttefornavn_ssb.csv',
                      'jentefornavn_ssb.csv']
    country_path_list = ['land.csv',
                         'kommuner.csv',
                         'tettsteder.csv']

    ruler = EntityRuler(nlp)
    location = os.path.dirname(os.path.realpath(__file__))

    # Names
    for file_path in name_path_list:
        my_file = os.path.join(location, 'data', file_path)
        name_df = pd.read_csv(my_file, sep=';')
        names_list.extend(name_df.iloc[:, 0].to_list())
    name_patterns = [{"label": "PER", "pattern": [{"lower": name.lower()}]} for name in names_list]
    ruler.add_patterns(name_patterns)

    # Countries
    for file_path in country_path_list:
        loc_file = os.path.join(location, 'data', file_path)
        loc_df = pd.read_csv(loc_file, sep=';')
        loc_list.extend(loc_df['name'].to_list())
    name_patterns = [{"label": "LOC", "pattern": [{"lower": country.lower()}]} for country in loc_list]
    ruler.add_patterns(name_patterns)

    return ruler
