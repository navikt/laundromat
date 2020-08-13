===================
What Is Laundromat?
===================
Laundromat is a python package for scrubbing personal information from text. 
The current Laundromat is adapted to the Norwegian context, but can easily be modified to fit any language.

Laundromat uses regular expressions coupled with a machine learning model to 
recognize and remove personal information in norwegian text. The package is
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


Current F1 scores with a model tuned on 500 hand labled texts:
-------------------


+--------+---------+-------+
| Entities         | Score |
+------------------+-------+
| Overall          |   87  |
+------------------+-------+
| PER              |   92  |
+------------------+-------+
| TLF              |   71  |
+------------------+-------+
| DTM              |   86  |
+------------------+-------+
| AMOUNT           |   83  |
+------------------+-------+
| LOC              |   89  |
+------------------+-------+
| ORG              |   67  |
+------------------+-------+


Current F1 scores using an untrained SpaCy model:
-------------------


+------------------+-------+
| Entities         | Score |
+------------------+-------+
| Overall          |   40  |
+------------------+-------+
| PER              |   63  |
+------------------+-------+
| TLF              |   51  |
+------------------+-------+
| DTM              |   38  |
+------------------+-------+
| AMOUNT           |   06  |
+------------------+-------+
| LOC              |   58  |
+------------------+-------+
| ORG              |   09  |
+------------------+-------+




Requirements
------------

spacy >= 2.3.0
