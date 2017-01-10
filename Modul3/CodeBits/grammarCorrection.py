from string import ascii_lowercase, ascii_uppercase

import language_check

tool = language_check.LanguageTool('en-US')


def get_word(text, index_start_word):
    length_word = 1
    while text[index_start_word + length_word] in  ascii_uppercase+ascii_lowercase:
        length_word += 1
    return text[index_start_word: index_start_word+length_word]


def grammarCorrection(text):
    matches = tool.check(text)
    corrected_text = language_check.correct(text, matches)
    word_suggestion = []
    length = 0
    for i in range(len(matches)):
        if matches[i].replacements[0] in corrected_text:
            index_old_word = matches[i].fromx
            word = get_word(text, index_old_word)
            word_suggestion.append((word, matches[i].replacements[0]))

    return corrected_text, word_suggestion

text = "Helli, my nanmme iss Momo.What iis yur name? This are bad. NO idEea.. "
print (grammarCorrection(text))

