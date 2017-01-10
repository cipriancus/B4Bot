import grammar_check

tool = grammar_check.LanguageTool('en-GB')

def grammarCorrection(text):
    return (tool.correct(text))

print(grammarCorrection("This are bad."))