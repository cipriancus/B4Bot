#the synonyms of word
from nltk.corpus import wordnet as wn

synonyms = []
synset = []

for syn in wn.synsets("small"):
    for l in syn.lemmas():
        synset.append(l.name())
if len(synset) > 5:
    synonyms = synset[2:7]
print(set(synonyms))
