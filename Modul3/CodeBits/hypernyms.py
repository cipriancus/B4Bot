#the synonyms of word
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer


def synonyms(word):
    hipernims=[]
    synset=[]
    for syn in  wn.synsets(word):
        synset.append(syn)
        hipernims.append(syn.hypernyms())
    return hipernims,synset


def lemmas(word):
    wordnet_lemmatizer = WordNetLemmatizer()
    return wordnet_lemmatizer.lemmatize(word)

print(synonyms('dog'))
print(lemmas('cats'))
