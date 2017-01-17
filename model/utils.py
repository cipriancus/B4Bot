def clean_whitespace(text):
    import re

    # liniile noi vor fi spatii
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

    text = text.strip()

    # Stergem spatiile multiple
    text = re.sub(' +', ' ', text)

    return text


def clean(text):
    import unicodedata

    text = clean_whitespace(text)
    # stergem cod html, daca este

    import html
    text = html.unescape(text)

    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')

    return str(text)


def import_module(dotted_path):
    """
    importa modulul specificat
    """
    import importlib

    module_parts = dotted_path.split('.')
    module_path = '.'.join(module_parts[:-1])
    module = importlib.import_module(module_path)

    return getattr(module, module_parts[-1])


def initialize_class(data, **kwargs):
    if isinstance(data, dict):
        import_path = data.pop('import_path')
        data.update(kwargs)
        Class = import_module(import_path)

        return Class(**data)
    else:
        Class = import_module(data)

        return Class(**kwargs)


def validate_adapter_class(validate_class, adapter_class):
    """
    Verifica daca cele 2 clase date au o relatie de rudenie
    """
    from adapters.adapters import Adapter
    import B4Bot

    if isinstance(validate_class, dict):
        origional_data = validate_class.copy()
        validate_class = validate_class.get('import_path')

        if not validate_class:
            raise B4Bot.InvalidAdapterException(
                'Dictionarul {} trebuie sa aiba o valoare valida pentru  "import_path"'.format(
                    str(origional_data)
                )
            )

    if not issubclass(import_module(validate_class), Adapter):
        raise B4Bot.InvalidAdapterException(
            '{} trebuie sa fie o subclasa a {}'.format(
                validate_class,
                Adapter.__name__
            )
        )

    if not issubclass(import_module(validate_class), adapter_class):
        raise B4Bot.InvalidAdapterException(
            '{} trebuie sa fie o subclasa a {}'.format(
                validate_class,
                adapter_class.__name__
            )
        )


def input_function():
    user_input = input()

    return user_input


def nltk_download_corpus(corpus_name):
    from nltk.data import find
    from nltk import download

    zip_file = '{}.zip'.format(corpus_name)
    downloaded = False

    try:
        find(zip_file)
    except LookupError:
        download(corpus_name, quiet=True)
        downloaded = True

    return downloaded


def remove_stopwords(tokens, language):
    """
    Sterge "Stop words" ca "is, the, a "
    """
    from nltk.corpus import stopwords

    stop_words = stopwords.words(language)

    tokens = set(tokens) - set(stop_words)

    return tokens


def get_entity(text):
    from nltk import ne_chunk, pos_tag, word_tokenize
    from nltk.tree import Tree
    chunked = ne_chunk(pos_tag(word_tokenize(text)))
    prev = None
    continuous_chunk = []
    current_chunk = []

    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
            else:
                continue

    return continuous_chunk
