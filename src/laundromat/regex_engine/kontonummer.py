from laundromat.regex_engine.regex_base import RegexBase
import re

class RegexAccountNumber(RegexBase):
    @property
    def regex_pattern(self):
        """
        TODO Add validation or change pattern as this one overlaps with personnummer
        """
        return r"(?<!\d)(\d{11})|(\d{4}(\.|\s)\d{2}(\.|\s)\d{5}\b)(?!\s*\d)"

    @property
    def context(self):
        return ["Tid og/eller dato"]

    @property
    def label(self):
        return "DTM"

    @property
    def score(self):
        return 1

    def validate(self):
        pass

    def validate_acc(self, acc: str):
        #TODO add a step that puts string in the right format
        # so as to avoid xx.xx.xxxxx for example
        d1 = int(acc[0])
        d2 = int(acc[1])
        d3 = int(acc[2])
        d4 = int(acc[3])
        d5 = int(acc[4])
        d6 = int(acc[5])
        d7 = int(acc[6])
        d8 = int(acc[7])
        d9 = int(acc[8])
        d10 = int(acc[9])

        control_digit = int(acc[10])

        mod_11 = (2*d10+3*d9+4*d8+5*d7+6*d6+7*d5+2*d4+3*d3+4*d2+5*d1)%11
        if mod_11+control_digit ==11:
            return 1.0
        else:
            return 0.0
