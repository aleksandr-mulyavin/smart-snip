from translate import Translator as ExtTranslator


class Translator():
    def __init__(self, to_lang, from_lang='en'):
        self.from_lang = from_lang
        self.to_lang = to_lang

    def translate(self, text: str) -> str:
        translator = ExtTranslator(
            to_lang=self.to_lang,
            from_lang=self.from_lang,
        )
        return translator.translate(text)
