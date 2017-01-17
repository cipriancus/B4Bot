
def levenshtein_distance(statement, other_statement):

    import sys

    try:
        from Levenshtein.StringMatcher import StringMatcher as SequenceMatcher
    except ImportError:
        from difflib import SequenceMatcher

    PYTHON = sys.version_info[0]

    if not statement.text or not statement.text:
        return 0


    statement_text = str(statement.text.lower())
    other_statement_text = str(other_statement.text.lower())

    similarity = SequenceMatcher(
        None,
        statement_text,
        other_statement_text
    )

    percent = int(round(100 * similarity.ratio())) / 100.0

    return percent

def sentiment_comparison(statement, other_statement):
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sentiment_analyzer = SentimentIntensityAnalyzer()
    statement_polarity = sentiment_analyzer.polarity_scores(statement.text.lower())
    statement2_polarity = sentiment_analyzer.polarity_scores(other_statement.text.lower())

    statement_greatest_polarity = 'neu'
    statement_greatest_score = -1
    for polarity in sorted(statement_polarity):
        if statement_polarity[polarity] > statement_greatest_score:
            statement_greatest_polarity = polarity
            statement_greatest_score = statement_polarity[polarity]

    statement2_greatest_polarity = 'neu'
    statement2_greatest_score = -1
    for polarity in sorted(statement2_polarity):
        if statement2_polarity[polarity] > statement2_greatest_score:
            statement2_greatest_polarity = polarity
            statement2_greatest_score = statement2_polarity[polarity]

    # Check if the polarity if of a different type
    if statement_greatest_polarity != statement2_greatest_polarity:
        return 0

    values = [statement_greatest_score, statement2_greatest_score]
    difference = max(values) - min(values)

    return 1.0 - difference