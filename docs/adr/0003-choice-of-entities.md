# 3. Choice of entities for the Named Entity Recognizer

Date: 08-07-2020

## Status

Accepted

## Context
The choice of entities, i.e. what categories of information we want to anonymise and the specificity of these categories, will greatly impact the performance of our model. Additionally, time constraints mean that there is an upper limit to how many entities can be included. As such, we concluded that those entities which fulfill at least two of the following three categories should be included:
 * It is either directly identifying or a close proxy (e.g. names, phone numbers, etc.)
 * It is a so-called “special categories” of information (e.g. medical information)
 * It is present in the data in non-trivial quantities 

## Decision
We have chosen the following NER entities:
 * ORG (Organisation)
 * LOC (Location)
 * PER (Person)
 * FNR (Personal number)
 * MONEY
 * DATE_TIME (Dates, time of day, name of day, and name of month)
 * MEDICAL_CONDITIONS
 

Entities that will be left purely to RegEx are:
 * NAV_YTELSE and NAV_OFFICE
 * AGE
 * TLF (Telephone number)
 * BACC (Bank account number)

We believe this list strikes the right balance between performance (fewer entities are better) and coverage.

## Consequences

Since data will be labeled with these entities, changing this list will require substantial resources and possible relabeling of data. Increasing granularity especially will be difficult to achieve if desired. These will most likely be the entities used going forward.

