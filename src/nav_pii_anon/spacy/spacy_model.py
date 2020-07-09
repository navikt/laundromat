
from nav_pii_anon.regex_container import RegexEngines
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
		self.model.add_pipe(self.ruler, before = "ner")

	def predict(self, text:str):
		"""
		Prints the found entities, their labels, start, and end index.
		:param text: a string of text which is to be analysed.
		"""
		fnr = RegexEngines.FNR.value
		doc = self.model(text)
		ents = [[ent.text, ent.label_, ent.start, ent.end, "NA"] for ent in doc.ents]
		for ent in ents:
			if ent[1]=="FNR":
				#TODO Since Levenstein distance returns a matrix we cannot have a simple call to the validate pnr function
				if(fnr.validate_pnr(ent[0])==1.0):
					ent[-1] = 1.0              
		print(ents)
	
	def get_doc(self, text:str):
		return self.model(text)
				

