===================
What Is Laundromat?
===================
Laundromat is a python package for scrubbing personal information from text. 
The current Laundromat is adapted to the Norwegian context, but can easily be modified to fit any language.
----------------------------------

Laundromat uses a mix of matching techniques like Regular expression
and a statistical model to recognize and remove personal information in norwegian text. The package is
built around SpaCy. Current functionality of the package includes:

* Detecting named entities related to personal and sensitive information.
* Censoring texts containing said information.
* Improving the NER model from new data.
* Scoring the model with various metrics.

Supported entities:

* <PER> - Person
* <DTM> - Date-time
* <TLF> - Telephone number
* <FNR> - Norwegian Personal Number
* <AMOUNT> - Amounts like percentages
* <LOC>  - Location, i.e. countries, cities, and addresses.
* <CREDIT_CARD> - Credit card number


Current Performance of an untrained 
-------------------


+-------+----------+-------+
| Enteties         | Score |
+------------------+-------+
| PER              |   0   |
+------------------+-------+
| TLF              |   0   |
+------------------+-------+
| DTM              |   0   |
+------------------+-------+
| AMOUNT           |   0   |
+------------------+-------+
| LOC              |   0   |
+------------------+-------+
| CREDIT_CARD      |   0   |
+------------------+-------+


Requirements
------------

spacy >= 2.3.0
