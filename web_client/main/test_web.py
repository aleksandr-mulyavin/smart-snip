from .translate_text import get_to_text_translate


def test_translating_when_from_equal_autodetect():
    """
    """
    source_text = 'Hello World!'
    translated_text = get_to_text_translate(
        source_text,
        lang_code='ru'
    )

    assert len(translated_text) > 0
    assert translated_text != source_text


def test_translating_when_from_equal_en():
    """
    """
    source_text = 'Hello World!'
    translated_text = get_to_text_translate(
        source_text,
        lang_code='ru',
        from_='en'
    )

    assert len(translated_text) > 0
    assert translated_text != source_text


def test_translating_when_from_equal_lang_code():
    """
    """
    source_text = 'Hello World!'
    translated_text = get_to_text_translate(
        source_text,
        lang_code='en',
        from_='en'
    )

    assert len(translated_text) > 0
    assert translated_text == source_text
