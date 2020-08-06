import pandas as pd
import os
from spacy.pipeline import EntityRuler
from laundromat.spacy.data_handler import get_data

def csv_list_matcher(nlp):
    """
    Reads csv-files for names and surnames and uses EntityRuler to match to a entity and return to be added to
    the model pipeline

    :param nlp: The Spacy model
    :return: The ruler containing the new pattern rules to be included in the pipeline
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

    # Names
    for file_path in name_path_list:
        name_df = get_data(file_path)
        names_list.extend(name_df.iloc[:, 0].to_list())
    name_patterns = [{"label": "PER", "pattern": [{"lower": name.lower()}]} for name in names_list]
    ruler.add_patterns(name_patterns)

    # Countries
    for file_path in country_path_list:
        loc_df = get_data(file_path)
        loc_list.extend(loc_df['name'].to_list())
    name_patterns = [{"label": "LOC", "pattern": [{"lower": country.lower()}]} for country in loc_list]
    ruler.add_patterns(name_patterns)

    return ruler
