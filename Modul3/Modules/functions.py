import re
from string import ascii_lowercase, ascii_uppercase
from threading import Thread, RLock

import langid
from nltk.corpus import wordnet as wn


def parse_sentence(_parser, _lemmatizer, _text, _language_tool):
    # function that gives the input and returns the final json product
    try:
        # threads = []
        final_output = []

        if lang_identify(_text):
            token_sentences = tokenize_sentence(_text)
            print("Tokenized sentences...\n")

            for sentence in token_sentences:

                spell_checked = grammar_correction(_text=sentence, _language_tool=_language_tool)
                print("Spell checked the sentence...\n")
                result = _parser.raw_parse(sentence=spell_checked[0], verbose=True)
                for element in result:
                    parsed_sentence = get_sentence_layout(element, spell_checked[1], _lemmatizer)
                    final_output.append({sentence: {"words": parsed_sentence, "punctuation": str(sentence[-1]),
                                                    "spell_check": spell_checked[0]}})

            # sent_thread = Thread(target=ref_sentence, args=(_parser, sentence, final_output))
            #     sent_thread.start()
            #
            #     threads.append(sent_thread)
            #
            # if len(threads):
            #     for thread in threads:
            #         if thread:
            #             thread.join()

            return final_output

        else:
            return "The language was not recognized as english! Please try again!\n"

    except Exception as exception:
        print("Exception occurred in 'functions.parse_sentence()' >> " + str(exception))


def ref_sentence(_parser, _sentence, _final_output):
    lock = RLock()
    result = _parser.raw_parse(sentence=_sentence, verbose=True)

    for element in result:
        parsed_sentence = get_sentence_layout(element)
        try:

            lock.acquire()
            _final_output.append({_sentence: {"words": parsed_sentence, "punctuation": str(_sentence[-1])}})
            lock.release()

        except Exception as exception:
            print("Exception occurred in 'functions.ref_sentence()' >> " + str(exception))


def get_sentence_layout(tree, _suggestions, _lemmatizer):
    try:

        parts_of_speech = dict()
        relations = dict()
        all_of_it = dict()

        threads = []

        for triple in tree.triples():
            parsed_triple = Thread(target=get_parsed_triple, args=(triple, parts_of_speech, relations))
            parsed_triple.start()

            threads.append(parsed_triple)

        if len(threads):
            for thread in threads:
                if thread:
                    thread.join()

        for key in parts_of_speech:
            # synonyms_and_hypernyms = get_synonyms_and_hypernims(key)
            # print(synonyms_and_hypernyms)

            all_of_it.setdefault(key, {"part-of-speech": parts_of_speech.get(key),
                                       "dependencies": relations.get(key),
                                       "synonyms": get_synonyms(key),
                                       # "hypernyms": synonyms_and_hypernyms[1],
                                       "lemma": get_lemma(word=key,
                                                          _word_lemmatizer=_lemmatizer),
                                       "suggestion": _suggestions.get(key)})

        return all_of_it

    except Exception as exception:
        print("Exception occurred in 'functions.get_sentence_layout()' >> " + str(exception))


def get_synonyms(word):
    try:

        synonyms = []

        for syn in wn.synsets("small"):
            for lem in syn.lemmas():
                if lem.name() not in synonyms:
                    synonyms.append(lem.name())

        return synonyms

    except Exception as exception:
        print("Exception occurred in 'functions.get_synonyms_and_hypernims()' >> " + str(exception))


def get_lemma(_word_lemmatizer, word):
    try:
        return _word_lemmatizer.lemmatize(word)

    except Exception as exception:
        print("Error occurred in 'functions.get_lemma' >> " + str(exception))


def lang_identify(text):
    try:

        lang = langid.classify(text)[0]
        if "en" == lang:
            return True
        else:
            return False

    except Exception as exception:
        print("Exception occurred in 'functions.get_synonyms()' >> " + str(exception))


def get_parsed_triple(triple, _parts_of_speech, _relations):
    try:

        lock = RLock()

        for element in triple:
            if isinstance(element, type(triple)):
                lock.acquire()
                try:
                    if element[0] not in _parts_of_speech.keys():

                        _parts_of_speech.setdefault(element[0], element[1])
                        lock.release()

                    else:
                        _parts_of_speech.update({element[0]: element[1]})
                        lock.release()

                except Exception as exception:
                    print("Exception occurred at 'functions' > " + str(exception))
                    lock.release()

        lock.acquire()
        try:
            if triple[0][0] not in _relations.keys():
                relation = ({"relation": triple[1], "with_word": triple[2][0]})
                _relations.setdefault(triple[0][0], [relation])

            else:
                get_value = _relations.get(triple[0][0])
                relation = ({"relation": triple[1], "with_word": triple[2][0]})
                get_value.append(relation)
                _relations.update({triple[0][0]: get_value})
                lock.release()

        except Exception as exception:
            print("Exception occurred > " + str(exception))
            lock.release()

        lock.acquire()

    except Exception as exception:
        print("Exception occurred in 'functions.get_synonyms()' >> " + str(exception))


def tokenize_sentence(sentence):
    try:

        sentence = sentence.strip()
        sentence_list = re.findall("[\w\s*,:'`;]+\.?\??!?", sentence)
        return_list = list()

        for sentence in sentence_list:
            if len(sentence) != 0:
                return_list.append(sentence.strip())
        return return_list

    except Exception as exception:
        print("Exception occurred in 'functions.tokenize_sentence()' >> " + str(exception))


def get_word(text, index_start_word):
    length_word = 1
    while text[index_start_word + length_word] in ascii_uppercase + ascii_lowercase:
        length_word += 1
    return text[index_start_word: index_start_word + length_word]


def grammar_correction(_text, _language_tool):
    matches = _language_tool.LanguageTool("en-US").check(_text)
    corrected_text = _language_tool.correct(_text, matches)

    word_suggestion = dict()

    for index in range(len(matches)):
        if matches[index].replacements[0] in corrected_text:
            index_old_word = matches[index].fromx
            word = get_word(_text, index_old_word)
            if len(word_suggestion):
                word_suggestion.update({word: matches[index].replacements[0]})
            else:
                word_suggestion.setdefault(word, matches[index].replacements[0])

    return corrected_text, word_suggestion
