from senti_classifier import senti_classifier

def analize(sentence):
     return senti_classifier.polarity_scores(sentence)
