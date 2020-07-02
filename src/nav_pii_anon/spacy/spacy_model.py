

from nav_pii_anon.regex_engine.fnr import RegexFnr
from nav_pii_anon.regex_engine.credit_card import RegexCreditCard
from nav_pii_anon.spacy.regex_formatter import regex_formatter
import spacy
from spacy.pipeline import EntityRuler

class SpacyModel():

      def __init__(self, model = None):
            if not model:
                  self.model = spacy.load("nb_core_news_lg")
            else:
                  self.model=model
            self.ruler = EntityRuler(self.model)
      
      def add_patterns(self, entities:list = None):
            self.ruler.add_patterns(regex_formatter(entities), before = "ner")
            self.model.add_pipe(ruler)

      def predict(self, text:str):
            doc = self.model(text)
            print([(ent.text, ent.label_, ent.start, ent.end) for ent in doc.ents])

