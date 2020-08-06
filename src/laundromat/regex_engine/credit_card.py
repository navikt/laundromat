from laundromat.regex_engine.regex_base import RegexBase


class RegexCreditCard(RegexBase):

    @property
    def regex_pattern(self):
        return r"\b((4\d{3})|(5[0-5]\d{2})|(6\d{3})|(1\d{3})|(3\d{3}))[- ]?(\d{3,4})[- ]?(\d{3,4})[- ]?(\d{3,5})\b"

    @property
    def context(self):
        return [
            "credit",
            "card",
            "visa",
            "mastercard",
            "cc ",
            "amex",
            "discover",
            "jcb",
            "diners",
            "maestro",
            "instapayment"
        ]

    @property
    def label(self):
        return "CREDIT_CARD"

    @property
    def score(self):
        return 1

    def validate(self):
        pass
