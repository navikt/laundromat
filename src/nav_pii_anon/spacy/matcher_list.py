import pandas as pd
from spacy.pipeline import EntityRuler


def name_list_matcher(nlp):
    """
    Reads csv-files for names and surnames and uses EntityRuler to match to a entity and return to be added to
    the model pipeline
    :param nlp:
    :return: ruler:
    """

    file_list = ['guttefornavn_ssb.csv', 'jentefornavn_ssb.csv', 'etternavn_ssb.csv']
    names_list = []

    for file_path in file_list:
        df = pd.read_csv(file_path, sep=';')
        names_list.extend(df.iloc[:, 0].to_list())

    patterns = [{"label": "PER", "pattern": name} for name in names_list]
    ruler = EntityRuler(nlp)
    ruler.add_patterns(patterns)

    return ruler
