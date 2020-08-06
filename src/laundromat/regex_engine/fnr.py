from laundromat.regex_engine.regex_base import RegexBase
import spacy
import re
import numpy as np


def levenstein_distance(pnr):
    """
    Function that checks the Levenstein distance of a string from a pnr
    :param pnr: The inputted pnr
    :return: Levenstein distance of from a PNR
    """
    # TODO: Make this to check for distance to valid PNR, so far it only checks if it is 11 digits

    regex_size = 11
    size_x = len(pnr) + 1
    size_y = regex_size + 1  # size of pnr
    matrix = np.zeros((size_x, size_y))  # Empty matrix

    for x in range(size_x):
        matrix[x, 0] = x
    for y in range(size_y):
        matrix[0, y] = y

    for x in range(1, size_x):
        for y in range(1, size_y):
            if re.match(r"\d", pnr[x - 1]):
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1],
                    matrix[x, y - 1] + 1
                )
            else:
                matrix[x, y] = min(
                    matrix[x - 1, y] + 1,
                    matrix[x - 1, y - 1] + 1,
                    matrix[x, y - 1] + 1
                )

    print('The Levenstein distance from a pnr is {0}'.format(matrix[size_x - 1, size_y - 1]))
    return matrix[size_x - 1, size_y - 1]


class RegexFnr(RegexBase):

    @property
    def regex_pattern(self):
        return r"((?<!\d)(\d{11}\b)|(\b\d{6}\s\d{5}))(\.*)(?!\s*\d)"

    @property
    def context(self):
        return ["fødselnummer"]

    @property
    def label(self):
        return "FNR"

    @property
    def score(self):
        return 1

    @property
    def validate(self):
        pass

    def validate_pnr(self, pnr: str):
        """
        :param pnr:
        :return:
        """

        if len(pnr) == 11 and re.match(r"\d{11}", pnr):
            d1 = int(pnr[0])
            d2 = int(pnr[1])

            m1 = int(pnr[2])
            m2 = int(pnr[3])

            y1 = int(pnr[4])
            y2 = int(pnr[5])

            i1 = int(pnr[6])
            i2 = int(pnr[7])
            i3 = int(pnr[8])

            k1 = int(pnr[9])
            k2 = int(pnr[10])

            k1_mod = (3 * d1 + 7 * d2 + 6 * m1 + m2 + 8 * y1 + 9 * y2 + 4 * i1 + 5 * i2 + 2 * i3) % 11
            new_k1 = 0 if k1_mod == 0 else (11 - k1_mod)

            k2_mod = (5 * d1 + 4 * d2 + 3 * m1 + 2 * m2 + 7 * y1 + 6 * y2 + 5 * i1 + 4 * i2 + 3 * i3 + 2 * k1) % 11
            new_k2 = 0 if k2_mod == 0 else (11 - k2_mod)

            if k1 != new_k1 or k2 != new_k2:
                print('not a valid PNR')
                levenstein_distance(pnr)

            if k1 == new_k1 and k2 == new_k2:
                print('Valid PNR')

                return 1.0
              
        else:
            levenstein_distance(pnr)