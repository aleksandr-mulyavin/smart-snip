from translate import Translator


def t():
    a = 'Work'
    return a


def tran(func):
    translator = Translator(to_lang="ru", from_lang="autodetect")
    translation = translator.translate(func)
    return translation
