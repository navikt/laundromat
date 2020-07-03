from nav_pii_anon.regex_engine.regex_base import RegexBase
import spacy
import re
import numpy as np


class RegexFnr(RegexBase):

    @property
    def regex_pattern(self):
        return r"(\b\d{11}\b)|(\b\d{6}\s\d{5}\b)"

    @property
    def context(self):
        return ["fødselnummer"]

    @property
    def label(self):
        return "FNR"

    @property
    def score(self):
        return 1

    def levenstein_distance(self, pnr):
        """
        :param pnr: Takes
        :return: Levenstein distance of from a pnr without spaces
        """

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
                if re.match(r'\d', pnr[x - 1]):
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

        return matrix[size_x - 1, size_y - 1]

        def validate(self):
            pass

    ## TODO: implement with our format

    # def validate(date: str, person_nr: str) -> None:
    #     d1 = int(date[0])
    #     d2 = int(date[1])
    #
    #     m1 = int(date[2])
    #     m2 = int(date[3])
    #
    #     y1 = int(date[4])
    #     y2 = int(date[5])
    #
    #     i1 = int(person_nr[0])
    #     i2 = int(person_nr[1])
    #     i3 = int(person_nr[2])
    #
    #     k1 = int(person_nr[3])
    #     k2 = int(person_nr[4])
    #
    #     k1_mod = (3 * d1 + 7 * d2 + 6 * m1 + m2 + 8 * y1 + 9 * y2 + 4 * i1 + 5 * i2 + 2 * i3) % 11
    #     new_k1 = 0 if k1_mod == 0 else (11 - k1_mod)
    #
    #     if k1 != new_k1:
    #         raise ValueError
    #
    #     k2_mod = (5 * d1 + 4 * d2 + 3 * m1 + 2 * m2 + 7 * y1 + 6 * y2 + 5 * i1 + 4 * i2 + 3 * i3 + 2 * k1) % 11
    #     new_k2 = 0 if k2_mod == 0 else (11 - k2_mod)
    #
    #     if k2 != new_k2:
    #         raise ValueError