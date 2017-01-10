#langid Module Required
#Download Here: https://pypi.python.org/packages/ea/4c/0fb7d900d3b0b9c8703be316fbddffecdab23c64e1b46c7a83561d78bd43/langid-1.1.6.tar.gz#md5=10b358148b9d5b7ba4576d89599ea396
#or install using Pip: pip install langid

import langid


def lang_identify (text):
    lang=langid.classify(text)[0]
    if "en" == lang:
        return True
    else:
        return False

print(lang_identify("Text enters here"))
