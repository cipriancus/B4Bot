#necesita instalare textblob [ex: pip install -U textblob]
from textblob import TextBlob
from textblob import Word

def correction(text):
    return (TextBlob(text).correct())

def suggestions(word):
    return (Word(word).spellcheck())

print(correction("I hav a good answwar"))
print(suggestions("havver"))