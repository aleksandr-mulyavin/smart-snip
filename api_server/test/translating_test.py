from api_server.src.service.translating import Translator


def test_translating():
    """
    """
    translator = Translator(to_lang='ru')

    source_text = 'Hello World!'
    translated_text = translator.translate(source_text)

    assert len(translated_text) > 0
    assert translated_text != source_text
