from laundromat.regex_engine.regex_base import RegexBase
import re

class RegexTlfNr(RegexBase):
    @property
    def regex_pattern(self):
        """
        Searches for 8-digit phone numbers and country codes.
        """
        # Det regexuttrykket som retuneres er rimelig robust, men tar bare norske tlfnr
        return r"(?<!\d)((\+|00)47\s*)*(\d{8}|\d{3}\s\d{2}\s\d{3}|\d{2}\s\d{2}\s\d{2}\s\d{2})(\.*)(?!\s*\d)"

    @property
    def context(self):
        return ["Telefonnummer"]

    @property
    def label(self):
        return "TLF"

    @property
    def score(self):
        return 1

    def validate(self):
        pass

    @staticmethod
    def validate_tlf(tlf: str):

        tlf = tlf.replace(' ', '')
        tlf = re.sub(r"(\+|00)47", '', tlf)
        print(tlf)

        if int(tlf) in range(20000000, 80000000) or int(tlf) in range(90000000, 100000000):
            print('gyldig norsk nummer')
            return 1.0
        else:
            print('ugyldig nummer')