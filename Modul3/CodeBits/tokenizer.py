import re


def sentenceTokenizer(text):
    sentenceList = re.findall("[\w\s]*[.!?]", text)
    returnList = list()
    for sentence in sentenceList:
        if len(sentence) != 0:
            returnList.append(sentence.strip())
    return returnList
