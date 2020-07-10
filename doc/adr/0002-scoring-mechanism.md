# 3. Scoring mechanism

Date: 07-07-2020

## Status

Accepted

## Context
A confidence score is very useful when evaluating the output of any model. It enables the user to put varying degrees of faith in the model predictions and allows for certain performance metrics. Sadly the SpaCy NER model’s architecture is such that it does not output confidence scores. There are ways around this, but they are unsatisfying and produce very low quality confidence scores. Therefore another method of gaining these confidence scores is required.

## Decision
We have chosen to create a model that will take as input the SpaCy NER model’s predicted entities, and output a confidence score. The architecture of this model has not been decided yet, but we will explore simple GLMs first before trying neural models.

## Consequences
Creating this model will require time and resources. It will slow down the speed of the spacy pipeline, and there is a risk that achieving sufficient levels of accuracy is not possible within the scope of the project. However, gaining a confidence score will result in better grounds for evaluating the SpaCy model and ultimately more responsible use of our solution.

