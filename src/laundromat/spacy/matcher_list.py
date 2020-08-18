import pandas as pd
import os
from spacy.pipeline import EntityRuler

class ListMatcher:

    def __init__(self):
        self.default_list = [('land.csv', "LOC"),
                            ('etternavn_ssb.csv', "PER"),
                            ('guttefornavn_ssb.csv', "PER"),
                            ('jentefornavn_ssb.csv', "PER")]

    def csv_list_matcher(self, nlp, path_list = None):
        """
        Reads csv-files for names and surnames and uses EntityRuler to match to a entity and return to be added to
        the model pipeline

        :param nlp: The Spacy model
        :param path_list: a list of tuples with the path of the list and its attendant entity.
        Accepts only single entity type lists. Lists must be a single column with the string "text" in the first cell.
        :return: The ruler containing the new pattern rules to be included in the pipeline
        """
        if path_list is None:
            path_list = self.default_list
        ruler = EntityRuler(nlp)
        for path, label in path_list:
            df = self.get_data(path)
            name_patterns = [{"label": label, "pattern": [{"lower": name.lower()}]} for name in df.iloc[:, 0]]
            ruler.add_patterns(name_patterns)
        return ruler

    def get_data(self, file_name:str):
        """
        Takes the file path of the integrated data and returns the csv-file as a dataframe
        :param file_name:
        :return dataframe:
        """
        location = os.path.dirname(os.path.realpath(__file__))
        my_file = os.path.join(location, 'data', file_name)
        dataframe = pd.read_csv(my_file, sep=';', encoding = 'utf-8')

        return dataframe
    
    def default_list_append(self, item):
        self.default_list.append(item)