import os
from translate import Translator as ExtTranslator


class Translator():
    def __init__(self, to_lang, from_lang='en'):
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.provider = os.getenv('TRANSLATE_PROVIDER')
        if self.provider is None:
            self.provider = 'mymemory'
        self.secret_key = os.getenv('TRANSLATE_KEY')
        self.base_url = os.getenv('TRANSLATE_BASE_URL')

    def translate(self, text: str) -> str:
        translator = ExtTranslator(
            to_lang=self.to_lang,
            from_lang=self.from_lang,
            provider=self.provider,
            secret_access_key=self.secret_key,
            base_url=self.base_url,
        )
        return translator.translate(text)
