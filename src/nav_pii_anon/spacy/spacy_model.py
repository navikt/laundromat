
import random
import warnings
from itertools import zip_longest
from pathlib import Path

import numpy as np
import pandas as pd
import plac
import spacy
from nav_pii_anon.spacy.matcher_list import name_list_matcher
from nav_pii_anon.spacy.matcher_regex import match_func
from sklearn.metrics import f1_score
from spacy import displacy
from spacy.gold import GoldParse
from spacy.matcher import Matcher
from spacy.scorer import Scorer
from spacy.util import compounding, minibatch


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
        ruler = name_list_matcher(self.model
                                  )
        self.model.add_pipe(match_func, name="regex_matcher", before='ner')
        self.model.add_pipe(ruler, after="ner")

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

    def train(self, TRAIN_DATA, labels: list =['PER', 'ORG', 'TLF', 'LOC', 'DTM', 'FNR',
                                                'AGE', 'AMOUNT', 'NAV_YTELSER', 'MEDICAL_CONDITIONS'],
              n_iter: int = 30, output_dir=None):

        ner = self.model.get_pipe("ner")
        for lab in labels:
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
        # Save model
        if output_dir is not None:
            output_dir = Path(output_dir)
            if not output_dir.exists():
                output_dir.mkdir()
            self.model.meta["name"] = 'test_model'  # rename model
            self.model.to_disk(output_dir)
            print("Saved model to", output_dir)

            # test the saved model
            print("Loading from", output_dir)
            nlp2 = spacy.load(output_dir)
            # Check the classes have loaded back consistently
            assert nlp2.get_pipe("ner").move_names == move_names


    def f1_scorer(self, TEST_DATA):
        scorer = Scorer()
        df = pd.DataFrame(TEST_DATA)
        df.columns = ["Text", "True_entities"]
        for txt, ents in zip(df["Text"], df["True_entities"]):
            doc = self.model.make_doc(txt)
            gold = GoldParse(doc, entities=ents["entities"])
            pred = self.get_doc(txt)
            scorer.score(pred, gold)
        return scorer.scores



    def test(self, TEST_DATA):
        """
        Tests the model on the given test data. Since identifying sensitive information is more important
        than identifying it correctly, we utilise both our own custom score and a much
        stricter F1 score. For our custom score metric, each correct entity represents 1 point.
        Each token correctly labeled represents 1/n points where n is the number of tokens
        in the entity.
        TODO Case in which one is contained in the other has been simplified
        TODO No functionality for which entity label has been applied
        """
        y_true = []
        y_pred = []
        score = 0
        number_of_ents = 0
        df = pd.DataFrame(TEST_DATA)
        df.columns = ["Text", "True_entities"]
        df["Model_entities"] = df["Text"].apply(lambda x: {"entities": [(ent.start, ent.end, ent.label_) for ent in self.model(x).ents]})
        #print(df.head())
        #print(self.predict("Test text Marius"))
        #Iterate through the prediction and the truth and compare
        #Generate binary list with values based on the truth and predictions
        for model_ent, truth in zip_longest(df["Model_entities"], df["True_entities"]):
            if not truth:
                y_true += [0]
                y_pred += [1]
            elif not model_ent:
                y_true += [1]
                y_pred += [0]
            else:
                #Compares the model prediction with ground truth
                print("model_ent", model_ent)
                if len(model_ent['entities'])==0:
                    y_pred += [0] *len(truth['entities'])
                    y_true += [1] *len(truth['entities'])
                elif len(truth['entities'])==0:
                    y_pred += [1] *len(model_ent['entities'])
                    y_true += [0] *len(model_ent['entities'])
                else:
                    #TODO Make for loop to iterate over all entities in the list.
                    model_start, model_end, model_label = model_ent['entities'][0][0], model_ent['entities'][0][1], model_ent['entities'][0][2]
                    truth_start, truth_end, truth_label = truth['entities'][0][0], truth['entities'][0][1], truth['entities'][0][2]
                    if model_start == truth_start and model_end == truth_end:
                        #Checks if the entities are the same
                        y_true += [1]
                        y_pred += [1]
                        score += 1
                        number_of_ents += 1
                    elif (model_start < truth_end < model_end) or (model_end > truth_start > model_start):
                        #Checks if there is exclusive overlap between the labels
                        y_true += [1]
                        y_pred += [0]
                        score += (model_end-model_start)/(truth_end-truth_start)
                        number_of_ents += 1
                    else:
                        #This covers cases where a label is wholly contained in another
                        if (model_end-model_start)< (truth_end-truth_start):
                            score += 1
                            y_true += [1]
                            y_pred += [0]
                        else:
                            score += 0.5
                            y_true += [1]
                            y_pred += [1]
                        number_of_ents += 1

        return score/number_of_ents, f1_score(y_true, y_pred)
