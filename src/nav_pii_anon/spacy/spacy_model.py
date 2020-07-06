

from nav_pii_anon.regex_engine.fnr import RegexFnr
from nav_pii_anon.regex_engine.credit_card import RegexCreditCard
from nav_pii_anon.spacy.regex_formatter import regex_formatter
import spacy
from spacy.pipeline import EntityRuler

class SpacyModel():

      def __init__(self, model = None):
            """
            SpacyModel class: A class for managing a SpaCy nlp model with methods for adding custom RegEx and for easy printing
            :param model: an nlp model
            """
            if not model:
                  self.model = spacy.load("nb_core_news_lg")
            else:
                  self.model=model
            self.ruler = EntityRuler(self.model)
      
      def add_patterns(self, entities:list = None):
            """
            Adds desired patterns to the entity ruler of the SpaCy model
            :param entities: a list of strings denoting which entities the nlp model should detect.
            """
            self.ruler.add_patterns(regex_formatter(entities))
            self.model.add_pipe(ruler, before = "ner")

      def predict(self, text:str):
            """
            Prints the found entities, their labels, start, and end index.
            :param text: a string of text which is to be analysed.
            """
            doc = self.model(text)
            print([(ent.text, ent.label_, ent.start, ent.end) for ent in doc.ents])

