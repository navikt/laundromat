from nav_pii_anon.regex_engine.fnr import RegexFnr
from nav_pii_anon.regex_engine.credit_card import RegexCreditCard
from enum import Enum


class RegexEngines(Enum):
    FNR = RegexFnr()
    CREDIT_CARD = RegexCreditCard()
