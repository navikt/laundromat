from laundromat.regex_engine.regex_base import RegexBase
import datetime



class RegexDateTime(RegexBase):

    @property
    def regex_pattern(self):
        """
        Searches for dates and times in a variety of format. Does not currently support the day-month format
        (e.g. 12. July)
        TODO Currently overlaps with phone numbers. Maybe validation is the best way to get around this.
        TODO Add day and month names for a lookup
        """
        return r"(?<!\d)((\d{1,2}(\-|\\|\/|\.|\s)?(0|1)?(\d)(\-|\\|\/|\.|\s)?(19|20)?\d{2}))(\.*)(?!\s*\d)"

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

    @staticmethod
    def validate_dmt(dmt: str):
        """
        Checks a list of different datetime formats an does a checksum
        :param dmt:
        :return:
        """
        check_pass = False
        date_format = ['%d.%m.%y', '%d.%m.%Y',
                       '%d-%m-%y', '%d-%m-%Y',
                       '%d%m%y', '%d%m%Y',
                       '%d %m %y', '%d %m %Y']

        for form in date_format:
            try:
                datetime.datetime.strptime(dmt, form)
                check_pass = True
            except ValueError:
                pass

        if check_pass:
            return 1.0
        else:
            return 0
