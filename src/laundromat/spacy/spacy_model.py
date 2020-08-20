import random
import warnings
from datetime import datetime
from itertools import zip_longest
from pathlib import Path

import networkx as nx
import pandas as pd
import spacy
from laundromat.regex_engine.generic import RegexGeneric
from laundromat.spacy.list_merger import merger
from laundromat.spacy.matcher_list import ListMatcher
from laundromat.spacy.matcher_regex import RegexMatcher
from spacy import displacy
from spacy.gold import GoldParse
from spacy.matcher import Matcher
from spacy.scorer import Scorer
from spacy.tokens import Doc
from spacy.util import compounding, minibatch


class SpacyModel:
    """
    :SpacyModel class: A class for managing a SpaCy nlp model with methods for the following:
    - adding custom RegEx 
    - easy training and display of results
    - various metrics
    """
    
    def __init__(self, model_path=None):
        if not model_path:
            self.model = spacy.load("nb_core_news_lg")
        else:
            self.model = spacy.load(model_path)
            self.model_path = model_path
        self.matcher = Matcher(self.model.vocab)
        Doc.set_extension('ents_regex', force=True, default=True)
        self.patterns_added = False
        self.list_matcher = ListMatcher()

    def add_patterns(self, entities: list = ['FNR', 'DTM', 'TLF', 
    'AMOUNT', 'CREDIT_CARD'], before_ner = False, lookup = False):
        """
        Adds desired patterns to the entity ruler of the SpaCy model.

        :param entities: a list of strings denoting which entities the nlp model should detect.
        """

        self.regex_matcher = RegexMatcher(entities)
        if self.patterns_added:
            self.model = spacy.load(self.model_path)
            self.patterns_added = False
        ruler = self.list_matcher.csv_list_matcher(nlp=self.model)
        if before_ner:
            self.model.add_pipe(self.regex_matcher.match_func, name="regex_matcher", before='ner')
        else:
            self.model.add_pipe(self.regex_matcher.match_func, name="regex_matcher", after='ner')
        if lookup:
            self.model.add_pipe(ruler, after="ner")
        self.model.add_pipe(merger, last = True)
        
    def new_regex(self, pattern: str, context: str, label: str):
        self.regex_matcher.append_regexes(RegexGeneric(pattern, context, label))

    def print_regex_labels(self):
        "Prints regex labels"
        try:
            for regex in self.regex_matcher.regexes:
                print(regex.label)
        except AttributeError:
            print([])

    def add_list(self, new_list):
        """
        :param new_list: new lists must be a tuple of a path and a tag.
        """
        self.list_matcher.default_list_append(new_list)

    def print_matcher_lists(self):
        for ls, tag in self.list_matcher.default_list:
            print("Path: ", ls, "Entity tag: ", tag)

    def predict(self, text: str):
        """
        :param text: a string of text which is to be analysed.
        :return: found entities, their labels, start, and end index.
        """
        doc = self.model(text)
        ents = [[ent.text, ent.label_, ent.start, ent.end] for ent in doc.ents]
        return ents

    def predict_list(self, text_list):
        docs = list(self.model.pipe(text_list))
        ents = []
        for d in docs:
            ents.append([[ent.text, ent.label_, ent.start, ent.end] for ent in d.ents])
        return ents

    def doc(self, text: str):
        """
        Returns the doc, a SpaCy object containing metadata about the text.

        :param text: A text string to be ran through the model
        :return: A text in doc-format
        """
        return self.model(text)

    def doc_list(self, text_list):
        return list(self.model.pipe(text_list))

    def display(self, text: str):
        colors = {"PER": "#FFA3A3",
                  "FNR": "#FDB9A2",
                  "DTM": "#FBCEA0",
                  "TLF": "#D8DEAD",
                  "AMOUNT": "#B5EEB9",
                  "LOC": "#ADDFEE",
                  "CREDIT_CARD": "#C0C7EC",
                  "ORG": "D2AFEA"
                  }

        options = {"ents": ["ORG", "LOC", "PER", "FNR", "AMOUNT", "TLF", "DTM", "CREDIT_CARD"],
                   "colors": colors
                   }
        displacy.render(self.doc(text), style='ent', jupyter=True, options=options)

    def disable_ner(self):
        """
        Disables the NER-model in the pipeline.
        """
        self.disabled = self.model.disable_pipes("ner")

    def enable_ner(self):
        """
        Enables the NER-model in the pipeline.
        """
        self.disabled.restore()

    def pipeline(self):
        """
        Prints current NLP pipeline.
        """
        print(self.model.pipe_names)

    def replace(self, text: str, replacement = "entity", replacement_char = "~"):
        """
        Replaces found entities in the given text with the attendant entity labels,
        e.g. a name is replaced with <PER>. Shuffle replacement is hard coded to use a list
        of girl, boy, county, country, and town names.

        :param text: The text in question as a string.
        :param replacement: The kind of replacement desired. Default is entity.
        :param replacement_char: The character used for character and padding replacement. Default is ~.
        :returns: the modified text as a string
        """

        doc = self.model(text)
        censored_text = text
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
            girls_names = self.list_matcher.get_data('jentefornavn_ssb.csv')['text']
            boys_names = self.list_matcher.get_data('guttefornavn_ssb.csv')['text']
            name_list = girls_names.append(boys_names, ignore_index=True)

            #kom_names = self.list_matcher.get_data('kommuner.csv')['text']
            country_names = self.list_matcher.get_data('land.csv')['text']
            #villages_names = self.list_matcher.get_data('tettsteder.csv')['text']
            #loc_list = kom_names.append(country_names.append(villages_names, ignore_index=True), ignore_index=True)
            loc_list = country_names
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
            current_dtm = str(datetime.now)
            alphanumeric_dtm = [character for character in current_dtm if character.isalnum()]
            alphanumeric_dtm = "".join(alphanumeric_dtm)
            self.model.meta["name"] = "ner_model_"+alphanumeric_dtm
            self.model.to_disk(output_dir)
            print("Saved model to", output_dir)

            # test the saved model
            print("Loading from", output_dir)
            nlp2 = spacy.load(output_dir)
            # Check the classes have loaded back consistently
            assert nlp2.get_pipe("ner").move_names == move_names

    def f1_scorer(self, TEST_DATA):
        """
        Ignores data of the wrong format. If this is a problem, use print_scores instead.
        :return: Scores as a dictionary.
        """
        scorer = Scorer()
        df = pd.DataFrame(TEST_DATA)
        df.columns = ["Text", "True_entities"]
        for txt, ents in zip(df["Text"], df["True_entities"]):
            doc = self.model.make_doc(txt)

            #Gold refers to the correct entity labels
            gold = GoldParse(doc, entities=ents["entities"])
            pred = self.model(txt)
            scorer.score(pred, gold)
        return scorer.scores

    def confusion_matrix(self, TEST_DATA, strict = True):
        """
        Calculates confusion matrix for given data. 
        Only considers whether a token has been labeled and not if it has been labeled correctly.

        :return: Confusion matrix as a dataframe.
        """
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
                    if strict:
                        if (t[0] == m[0]) and (m[1] == t[1]):
                            tp += 1
                            overlap += 1
                    else:
                        if (t[0] <= m[0] <=t[1]) or (t[0] <= m[1] <= t[1]):
                            tp += 1
                            overlap += 1
            fp += len(ents_m) - overlap
            fn += len(ents_t) - overlap
            tn = tn -(len(ents_m)-overlap) -len(ents_t)
        tn += df["total"].sum()
        confusion = pd.DataFrame([[tp, fp], [fn, tn]], index = ["Predicted Positive", "Predicted Negative"], columns=["Is Positive", "Is Negative"])
        return confusion
    
    def print_scores(self, TEST_DATA, strict=True):
        """
        Prints the following scores:
        - Accuracy
        - Balanced accuracy
        - Precision
        - Recall
        - F1 score
        """
        cf = self.confusion_matrix(TEST_DATA, strict)
        true_positive = cf["Is Positive"].iloc[0]
        true_negative = cf["Is Negative"].iloc[1]
        false_positive = cf["Is Negative"].iloc[0]
        false_negative = cf["Is Positive"].iloc[1]
        accuracy = (true_positive+true_negative)/(cf.values.sum() + 1e-100)
        precision = true_positive/(true_positive+false_positive+ 1e-100)
        specificity = true_negative/(true_negative+false_positive+ 1e-100)
        recall = true_positive/(true_positive+false_negative+ 1e-100)
        balanced_accuracy = (recall+specificity)/2
        f_1 = 2*true_positive/(2*true_positive+false_positive+false_negative + 1e-100)

        print("Accuracy is: ", accuracy)
        print("Balanced accuracy is: ", balanced_accuracy)
        print("Precision is: ", precision)
        print("Recall is: ", recall)
        print("F1 score is: ", f_1)
    
    def count(self, text:str):
        try:
            ents = [("PER", 0), ("ORG", 0), ("LOC", 0)]
            ents += [(x.label,0) for x in self.regex_matcher.regexes]
            ents = list(set(ents))
        except AttributeError:
            ents = [("PER", 0), ("ORG", 0), ("LOC", 0)]
        ent_counts = dict(ents)
        try:
            tx = str(text)
        except TypeError:
            return ent_counts
        for ent in self.model(tx).ents:
            try:
                ent_counts[ent.label_] = ent_counts[ent.label_] + 1
            except KeyError:
                ent_counts[ent.label_] = 1
        return ent_counts

    def dependency_graph(self, text: str):
        """
        :param text: The text in question as a string.
        :return: A digraph of the linguistic dependencies in the text. 
        """
        #TODO Seems to struggle with the  <ENTITY> format as <, >, and . end up as their own nodes.
        doc = self.model(text)
        edges = []
        for token in doc:
            for child in token.children:
                edges.append(('{0}'.format(token.lower_),
                            '{0}'.format(child.lower_)))
        return nx.DiGraph(edges)

    def top_n_nodes(self, text:str, n=10):
        """
        :param text: The text in question as a string.
        :param n: Number of nodes desired. Default is 10.
        :return: The top n nodes with highest degree in the dependency graph.
        """
        graph = self.dependency_graph(text)
        sorted_node_degrees = sorted(list(graph.degree), key= lambda x: x[1], reverse=True)
        if(n>len(sorted_node_degrees)):
            n = len(sorted_node_degrees)
        return sorted_node_degrees[:n]

    def similarity(self, text:str, replacement = "entity", replacement_char = "~"):
        """
        :param text: The text in question as a string.
        :param replacement: The kind of replacement desired. Default is entity.
        :param replacement_char: The character used for character and padding replacement. Default is ~.
        :return: The cosine similarity between the unaltered text and the altered text.
        """
        original = self.model(text)
        censored = self.model(self.replace(text, replacement,replacement_char))
        return original.similarity(censored)
