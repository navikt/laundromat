
import random
import warnings
from itertools import zip_longest
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd
import plac
import spacy
from nav_pii_anon.spacy.data_handler import get_data
from nav_pii_anon.spacy.matcher_list import csv_list_matcher
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
        SpacyModel class: A class for managing a SpaCy nlp model with methods for adding custom RegEx and for
        easy printing

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
        ruler = csv_list_matcher(self.model)
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

    def doc(self, text: str):
        """
        A method to return the doc, thus all its meta info.

        :param text: A text string to be ran through the model
        :return: A text in doc-format
        """
        return self.model(text)

    def display_predictions(self, text: str):
        colors = {"PER": "linear-gradient(10deg, #FF3333, #FF9933)",
                  "FNR": "linear-gradient(90deg, #AD0CA3, #AD0C3A)",
                  "TLF": "linear-gradient(10deg, #6BFF33, #F1B141)",
                  "AMOUNT": "linear-gradient(10deg, #aa9cfc, #fc9ce7)",
                  "LOC": "linear-gradient(10deg, #33FFF6, #33B2FF)",
                  "CREDIT_CARD": "linear-gradient(10deg, #9CF9B3, #F6F99C)",
                  "DTM": "linear-gradient(10deg, #0A7E2F, #0EAD0C)",
                  }

        options = {"ents": ["LOC", "PER", "FNR", "AMOUNT", "MEDICAL_CONDITIONS", "TLF", "DTM", "CREDIT_CARD"],
                   "colors": colors
                   }
        displacy.render(self.doc(text), style='ent', jupyter=True, options=options)

    def disable_ner(self):
        """
        Disables the NER-model in the pipeline

        """
        self.disabled = self.model.disable_pipes("ner")

    def enable_ner(self):
        """
        Enables the NER-model in the pipeline

        """
        self.disabled.restore()

    def pipeline(self):
        print(self.model.pipe_names)

    def replace(self, text: str, replacement = "entity", replacement_char = "~"):
        """
        Replaces found entities in the given text with the attendant entity labels,
        e.g. a name is replaced with <PER>.

        returns: the modified text as a string
        """

        doc = self.model(text)
        censored_text = text  # Redundant variable?
        ents = [[ent.text, ent.label_, ent.start, ent.end, "NA"] for ent in doc.ents]

        if replacement=="entity":
            for ent in ents:
                censored_text = censored_text.replace(ent[0], "<" + ent[1] + ">")
        elif replacement=="character":
            for ent in ents:
                censored_text = censored_text.replace(ent[0], replacement_char)
        elif replacement=="pad":
            for ent in ents:
                censored_text = censored_text.replace(ent[0], replacement_char*len(ent[0]))
        elif replacement=="shuffle":
            girls_names = get_data('jentefornavn_ssb.csv')['fornavn']
            boys_names = get_data('guttefornavn_ssb.csv')['fornavn']
            name_list = girls_names.append(boys_names, ignore_index=True)

            kom_names = get_data('kommuner.csv')['name']
            counrties_names = get_data('land.csv')['name']
            villages_names = get_data('tettsteder.csv')['name']
            loc_list = kom_names.append(counrties_names.append(villages_names, ignore_index=True), ignore_index=True)

            for ent in ents:
                if ent[1] == 'PER':
                    censored_text = censored_text.replace(ent[0], name_list[np.random.randint(0, len(name_list))])
                if ent[1] == 'LOC':
                    censored_text = censored_text.replace(ent[0], loc_list[np.random.randint(0, len(loc_list))])
                else:
                    censored_text = censored_text.replace(ent[0], "<" + ent[1] + ">")
        else:
            raise ValueError("replacement must be either entity, character, pad, or shuffle")
        return censored_text

    def train(self, TRAIN_DATA, labels: list, n_iter: int = 30, output_dir=None):

        """
        Takes the training data and trains the wanted entities. Also saves the model if a output path is given

        :param TRAIN_DATA: training data
        :param labels: texts with labels
        :param n_iter: number
        :param output_dir: Where the model should be saved
        """

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

            #Gold refers to the correct entity labels
            gold = GoldParse(doc, entities=ents["entities"])
            pred = self.model(txt)
            scorer.score(pred, gold)
        return scorer.scores #, scorer.textcat_score, scorer.textcats_per_cat

    def confusion_matrix(self, TEST_DATA):
        tp, fn, fp, tn = 0, 0, 0, 0
        df = pd.DataFrame(TEST_DATA)
        df.columns = ["Text", "True_entities"]
        df["Model_entities"] = df["Text"].apply(lambda x: {"entities": [(ent.start_char, ent.end_char, ent.label_) for ent in self.model(x).ents]})
        df["total"] = df["Text"].apply(lambda x: len(self.model(x)))
        for model, truth in zip_longest(df["Model_entities"], df["True_entities"]):
            ents_m = model["entities"]
            ents_t = truth["entities"]
            overlap = 0
            for m in model["entities"]:
                for t in truth["entities"]:
                    if (t[0] == m[0]) and (m[1] == t[1]):
                        tp += 1
                        overlap += 1
            fp += len(ents_m) - overlap
            fn += len(ents_t) - overlap
            tn = tn -(len(ents_m)-overlap) -len(ents_t)
        tn += df["total"].sum()
        return [[tp, tn], [fp, fn]]
            
    def accuracy(self, test):
        """
        A very lenient accuracy measure. If there is any overlap between the predicted entity label and the 
        true entity label then it is considered a true positive. The labels still have to be the same.
        """
        positive, negative = 0, 0
        df = pd.DataFrame(test)
        df.columns = ["Text", "True_entities"]
        df["Model_entities"] = df["Text"].apply(lambda x: {"entities": [(ent.start_char, ent.end_char, ent.label_) for ent in self.model(x).ents]})
        for model, truth in zip_longest(df["Model_entities"], df["True_entities"]):
            for ents_m in model["entities"]:
                for ents_t in truth["entities"]:
                    if (ents_t[0] <= ents_m[0] <= ents_t[1]) or (ents_t[0] <= ents_m[1] <= ents_t[1]):
                        positive += 1
                negative += len  
        negative = total - positive
        return positive, negative

    def test(self, TEST_DATA):
        """
        Tests the model on the given test data. Since identifying sensitive information is more important
        than identifying it correctly, we utilise both our own custom score and a much
        stricter F1 score. For our custom score metric, each correct entity represents 1 point.
        Each token correctly labeled represents 1/n points where n is the number of tokens
        in the entity.

        TODO Case in which one is contained in the other has been simplified

        TODO No functionality for which entity label has been applied

        :returns: a custom score, and the F_1 score
        """
        y_true = []
        y_pred = []
        score = 0
        number_of_ents = 0
        df = pd.DataFrame(TEST_DATA)
        df.columns = ["Text", "True_entities"]
        df["Model_entities"] = df["Text"].apply(lambda x: {"entities": [(ent.start_char, ent.end_char, ent.label_) for ent in self.model(x).ents]})
        #print(df.head())
        #print(self.predict("Test text Marius"))
        #Iterate through the prediction and the truth and compare
        #Generate binary list with values based on the truth and predictions
        for model_ent, truth in zip_longest(df["Model_entities"], df["True_entities"]):
            #If and elif cover if one column is shorter than the other
            if not truth:
                y_true += [0]
                y_pred += [1]
            elif not model_ent:
                y_true += [1]
                y_pred += [0]
            else:
                #Compares the model prediction with ground truth
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
    
    def dependency_graph(self, text: str):
        #TODO Seems to struggle with the  <ENTITY> format as <, >, and . end up as their own nodes.
        doc = self.model(text)
        edges = []
        for token in doc:
            for child in token.children:
                edges.append(('{0}'.format(token.lower_),
                            '{0}'.format(child.lower_)))
        return nx.DiGraph(edges)

    def top_n_nodes(self, text:str, n=10):
        graph = self.dependency_graph(text)
        sorted_node_degrees = sorted(list(graph.degree), key= lambda x: x[1], reverse=True)
        if(n>len(sorted_node_degrees)):
            n = len(sorted_node_degrees)
        return sorted_node_degrees[:n]

    def similarity(self, text:str, replacement = "entity", replacement_char = "~"):
        original = self.model(text)
        censored = self.model(self.replace(text, replacement,replacement_char))
        return original.similarity(censored)



