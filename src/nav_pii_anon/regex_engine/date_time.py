from nav_pii_anon.regex_engine.regex_base import RegexBase
import re

class RegexDateTime(RegexBase):
    @property
    def regex_pattern(self):
        """
        Searches for dates and times in a variety of format. Does not currently support the day-month format (e.g. 12. July)
        TODO Currently overlaps with phone numbers. Maybe validation is the best way to get around this.
        TODO Add day and month names for a lookup
        """
        return r"(\b\d{1,2}(\-|\\|\/|\.|\s)?\d{1,2}(\-|\\|\/|\.|\s)?\d{1,4}\b)(\b\d{1,2}(\.|\:)?\d{1,2}\b)"

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
