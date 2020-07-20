from nav_pii_anon.spacy.matcher_regex import match_func
import spacy
from spacy.matcher import Matcher
from spacy import displacy
import plac
import random
import warnings
import spacy
from spacy.util import minibatch, compounding


class SpacyModel:

    def __init__(self, model=None):
        """
        SpacyModel class: A class for managing a SpaCy nlp model with methods for adding custom RegEx and for easy printing
        :param model: an nlp model
        """
        if not model:
            self.model = spacy.load("nb_core_news_lg")
        else:
            self.model = model
        self.matcher = Matcher(self.model.vocab)

    def add_patterns(self, entities: list = None):
        """
        Adds desired patterns to the entity ruler of the SpaCy model
        :param entities: a list of strings denoting which entities the nlp model should detect.
        """
        self.model.add_pipe(match_func, before='ner')

    def predict(self, text: str):
        """
        Prints the found entities, their labels, start, and end index.
        :param text: a string of text which is to be analysed.
        """
        doc = self.model(text)
        ents = [[ent.text, ent.label_, ent.start, ent.end, "NA"] for ent in doc.ents]

        print(ents)

    def get_doc(self, text: str):
        return self.model(text)

    def display_predictions(self, text: str):
        displacy.render(self.get_doc(text), style='ent', jupyter=True)

    def disable_ner(self):
        self.disabled = self.model.disable_pipes("ner")

    def enable_ner(self):
        self.disabled.restore()

    def replace(self, text: str):
        doc = self.model(text)
        censored_text = text
        ents = [[ent.text, ent.label_, ent.start, ent.end, "NA"] for ent in doc.ents]
        for ent in ents:
            censored_text = censored_text.replace(ent[0], "<" + ent[1] + ">")
        return censored_text

def train(self, TRAIN_DATA, labels: list = ['ORG', 'LOC', 'DTM', 'PER',
                                            'TLF', 'TITLE', 'MEDICAL_CONDITIONS'],
          n_iter: int = 30):
        ner = self.model.get_pipe("ner")
        for lab in labels:
            print(type(lab))
            ner.add_label(lab)
        optimizer = self.model.resume_training()
        move_names = list(ner.move_names)
        pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
        other_pipes = [pipe for pipe in self.model.pipe_names if pipe not in pipe_exceptions]
        with (self.model.disable_pipes(*other_pipes)), warnings.catch_warnings():
            warnings.filterwarnings("once", category=UserWarning, module='spacy')
            sizes = compounding(1.0, 4.0, 1.001)
            # batch up the examples using spaCy's minibatch
            for itn in range(n_iter):
                random.shuffle(TRAIN_DATA)
                batches = minibatch(TRAIN_DATA, size=sizes)
                losses = {}
                for batch in batches:
                    texts, annotations = zip(*batch)
                    self.model.update(texts, annotations, sgd=optimizer, drop=0.35, losses=losses)
                print("Losses", losses)
