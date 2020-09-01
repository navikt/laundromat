# 1. Creating our own python package based on SpaCy and RegEx

Date: 30-06-2020

## Status

Accepted

## Context

At the beginning of the project Presidio seemed like a promising framework to for anonymizing text. Part of our desire to use it was that Presidio is supported by Microsoft, meaning that significantly more resources than are available to us might be used to develop and maintain it. Additionally, Presidio supports image anonymization which might be a useful feature for NAV down the line. 

Our initial idea was to modify Presidio to support Norwegian, and to include our own custom Named Entities. After some experimentation, we discovered the following:
 * Presidio’s documentation is sparse and lacks detail.
 * Presidio adds only limited functionality to SpaCy for text.
 * Much of Presidio is hard coded to use English, and so adapting it for Norwegian was difficult.

## Decision

We will not be using the Presidio framework. Instead we will make our own python package implementing Spacy and RegEx.

## Consequences

Much of the logic in Presidio has to be replicated. We have to implement our own custom SpaCy model and our own RegEx as a Python package, perhaps with an API. Resources must be spent maintaining the package.

