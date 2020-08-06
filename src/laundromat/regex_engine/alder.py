from laundromat.regex_engine.regex_base import RegexBase
import re

class RegexAccountNumber(RegexBase):
    @property
    def regex_pattern(self):
        """
        """
        return r"(\b(?<!(\d{1,11}))(\d{2,3})(?!\d{1,11})(?!\s\d{1,4})(?!\.\d{1,4})(?!\-\d{1,4})(?!\%)(?!\sprosent)\b)"

    @property
    def context(self):
        return ["Alder"]

    @property
    def label(self):
        return "AGE"

    @property
    def score(self):
        return 1

    def validate(self):
        pass

    def validate_age(self, age: str):
        if(int(age)<0 or int(age)>110):
            return 0.0
        else:
            return 0.5
