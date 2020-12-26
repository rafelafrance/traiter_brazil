# The Brazil Flora Traits Project ![Python application](https://github.com/rafelafrance/traiter_brazil/workflows/CI/badge.svg)

## Multiple methods for parsing
1. Rule based parsing. Most machine learning models require a substantial training dataset. I use this method to bootstrap the training data. And, if other methods fail, I can fall back to this.
1. Machine learning models. (In progress)

## Rule-based parsing strategy
1. I label terms using Spacy's phrase and rule-based matchers.
1. Then I match terms using rule-based matchers repeatedly until I have built up a recognizable trait like: color, size, count, etc.
1. Finally, I associate traits with plant parts.

There are, of course, complications and subtleties not outlined above but you should get the gist of what is going on here.

## Install
You will need to have Python 3.8 (or later) installed. You can install the requirements into your python environment like so:
```
git clone https://github.com/rafelafrance/traiter_brazil.git
cd traiter_brazil
optional: virtualenv -p python3.8 venv
optional: source venv/bin/activate
python3 -m pip install --requirement requirements.txt
python3 -m pip install git+https://github.com/rafelafrance/traiter.git@master#egg=traiter
```

## Run
```
./extract.py ... TODO ...
```

## Tests
Having a test suite is absolutely critical. The strategy I use is every new trait gets its own test set. Any time there is a parser error I add the parts that caused the error to the test suite and correct the parser. I.e. I use the standard red/green testing methodology.

You can run the tests like so:
```
cd /my/path/to/brazil_traiter
python -m unittest discover
```
