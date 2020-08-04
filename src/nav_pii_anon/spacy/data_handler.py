import os
import pandas as pd


def get_data(file_name:str):
    """
    Takes the file path of the integrated data and returns the csv-file as a dataframe
    :param file_name:
    :return dataframe:
    """
    location = os.path.dirname(os.path.realpath(__file__))
    my_file = os.path.join(location, 'data', file_name)
    dataframe = pd.read_csv(my_file, sep=';')

    return dataframe