from regex_engine.regex_base import RegexBase


class RegexFnr(RegexBase):

    @property
    def regex_pattern(self):
        return r"(\b\d{11}\b)|(\b\d{6}\s\d{5}\b)"

    @property
    def context(self):
        return ["fødselnummer"]

    @property
    def label(self):
        return "[FNR]"

    @property
    def score(self):
        return 1

    def validate(self):
        pass
