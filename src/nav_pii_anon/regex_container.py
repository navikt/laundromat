from nav_pii_anon.regex_engine.fnr import RegexFnr
from nav_pii_anon.regex_engine.credit_card import RegexCreditCard
from nav_pii_anon.regex_engine.tlfnr import RegexTlfNr
from nav_pii_anon.regex_engine.date_time import RegexDateTime
from enum import Enum


class RegexEngines(Enum):
    FNR = RegexFnr()
    CREDIT_CARD = RegexCreditCard()
    TLF = RegexTlfNr()
    DTM = RegexDateTime()
