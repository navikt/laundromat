from enum import Enum
from nav_pii_anon.regex_container import RegexEngines


def regex_formatter(entities=None):
      labels = all_possible_labels()
      if not entities:  
            regex = [ent.value.regex_pattern for ent in RegexEngines]
            form = []
            for label, reg in zip(labels, regex):
                  form+=[{"label": label, "pattern":[{"TEXT": {"REGEX": reg}}]}]
            return form
      elif set(entities).issubset(set(labels)):
            regex = [ent.value.regex_pattern for ent in RegexEngines if ent.value.label in entities]
            form = []
            for label, reg in zip(labels, regex):
                  form+=[{"label": label, "pattern":[{"TEXT": {"REGEX": reg}}]}]
            return form
      #TODO Else if they add entities that do not exist yet 
            

def new_entity(label:str, match:str):
      pass

def all_possible_labels():
    return [engine.value.label for engine in RegexEngines]