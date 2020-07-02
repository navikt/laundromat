from regex_engine.regex_base import RegexBase


class RegexTlfNr(RegexBase):

    @property
    def regex_pattern(self):
        return r"(\b\d{8}\b)|\b\d{3}\s\d{2}\s\d{3}\b|(\b\d{2}\s\d{2}\s\d{2}\s\d{2}\b)"

    @property
    def context(self):
        return ["Telefonnummer"]

    @property
    def label(self):
        return "[TLF]"

    @property
    def score(self):
        return 1

    def validate(self):
        pass