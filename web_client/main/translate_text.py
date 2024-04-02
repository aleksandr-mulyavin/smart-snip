import os
import requests
from translate import Translator
from translate.exceptions import TranslationError


def get_to_text_translate(text, lang_code, from_='autodetect'):
    """
    Позволяет перевести текст.
    На вход подается исходный текст и код языка, на который нужно перевести.
    Язык исходного текста определяется автоматически.
    """
    if lang_code == from_:
        return text

    provider = os.getenv('TRANSLATE_PROVIDER')
    if provider is None:
        provider = 'mymemory'
    secret_key = os.getenv('TRANSLATE_KEY')
    base_url = os.getenv('TRANSLATE_BASE_URL')

    translator = Translator(
        to_lang=lang_code,
        from_lang=from_,
        provider=provider,
        secret_access_key=secret_key,
        base_url=base_url,
    )

    try:
        translated_text = translator.translate(text)
    except TranslationError as e:
        translated_text = ''
        print(str(e))

    if from_ == 'autodetect' \
            and translated_text == 'PLEASE SELECT TWO DISTINCT LANGUAGES':
        return text
    return translated_text


def __get_languages() -> dict:
    """Функция возвращает список языков в виде словаря (код и наименование).
    Если провайдер libre, то для получения списка языков выполняется
    запрос к серверу переводчика.
    Иначе возвращается список языков в соответствии со стандартом ISO 639-1.

    Returns:
        dict
    """
    result = {}
    provider = os.getenv('TRANSLATE_PROVIDER')
    base_url = os.getenv('TRANSLATE_BASE_URL')
    if provider == 'libre' and base_url is not None:
        try:
            response = requests.get(f'{base_url}languages')
            for lang in response.json():
                result[lang['code']] = lang['name']
        except Exception as e:
            print(str(e))
    if result:
        return result
    else:
        return {
            'ru': 'Russian',
            'en': 'English',
            'af': 'Afrikaans',
            'ak': 'Akan',
            'sq': 'Albanian',
            'am': 'Amharic',
            'ar': 'Arabic',
            'hy': 'Armenian',
            'as': 'Assamese',
            'az': 'Azerbaijani',
            'bm': 'Bambara',
            'ba': 'Bashkir',
            'eu': 'Basque',
            'be': 'Belarusian',
            'bn': 'Bengali',
            'bs': 'Bosnian',
            'bg': 'Bulgarian',
            'my': 'Burmese',
            'ca': 'Catalan',
            'ny': 'Chichewa',
            'zh': 'Chinese',
            'co': 'Corsican',
            'hr': 'Croatian',
            'cs': 'Czech',
            'da': 'Danish',
            'dv': 'Divehi',
            'nl': 'Dutch, Flemish',
            'dz': 'Dzongkha',
            'eo': 'Esperanto',
            'et': 'Estonian',
            'ee': 'Ewe',
            'fo': 'Faroese',
            'fj': 'Fijian',
            'fi': 'Finnish',
            'fr': 'French',
            'gd': 'Gaelic',
            'gl': 'Galician',
            'ka': 'Georgian',
            'de': 'German',
            'ki': 'Gikuyu',
            'el': 'Greek',
            'gn': 'Guarani',
            'gu': 'Gujarati',
            'ht': 'Haitian',
            'ha': 'Hausa',
            'he': 'Hebrew',
            'hi': 'Hindi',
            'id': 'Indonesian',
            'ga': 'Irish',
            'ig': 'Igbo',
            'is': 'Icelandic',
            'it': 'Italian',
            'iu': 'Inuktitut',
            'ja': 'Japanese',
            'kn': 'Kannada',
            'ks': 'Kashmiri',
            'kk': 'Kazakh',
            'km': 'Central Khmer',
            'rw': 'Kinyarwanda',
            'ky': 'Kirghiz',
            'kg': 'Kongo',
            'ko': 'Korean',
            'ku': 'Kurdish',
            'la': 'Latin',
            'lb': 'Luxembourgish',
            'lg': 'Ganda',
            'li': 'Limburgan',
            'ln': 'Lingala',
            'lo': 'Lao',
            'lt': 'Lithuanian',
            'lv': 'Latvian',
            'mk': 'Macedonian',
            'mg': 'Malagasy',
            'ms': 'Malay',
            'ml': 'Malayalam',
            'mt': 'Maltese',
            'mi': 'Maori',
            'mr': 'Marathi',
            'mn': 'Mongolian',
            'ne': 'Nepali',
            'nb': 'Norwegian Bokmål',
            'nn': 'Norwegian Nynorsk',
            'no': 'Norwegian',
            'or': 'Oriya',
            'fa': 'Persian',
            'pl': 'Polish',
            'ps': 'Pashto, Pushto',
            'pt': 'Portuguese',
            'rn': 'Rundi',
            'ro': 'Romanian, Moldavian, Moldovan',
            'sa': 'Sanskrit',
            'sc': 'Sardinian',
            'sd': 'Sindhi',
            'sm': 'Samoan',
            'sg': 'Sango',
            'sr': 'Serbian',
            'sn': 'Shona',
            'si': 'Sinhala, Sinhalese',
            'sk': 'Slovak',
            'sl': 'Slovenian',
            'so': 'Somali',
            'st': 'Southern Sotho, Southern Sesotho',
            'es': 'Spanish, Castilian',
            'su': 'Sundanese',
            'sw': 'Swahili',
            'ss': 'Swati',
            'sv': 'Swedish',
            'ta': 'Tamil',
            'te': 'Telugu',
            'tg': 'Tajik',
            'th': 'Thai',
            'ti': 'Tigrinya',
            'bo': 'Tibetan',
            'tk': 'Turkmen',
            'tl': 'Tagalog',
            'tn': 'Tswana',
            'to': 'Tonga',
            'tr': 'Turkish',
            'ts': 'Tsonga',
            'tt': 'Tatar',
            'tw': 'Twi',
            'ty': 'Tahitian',
            'ug': 'Uighur',
            'uk': 'Ukrainian',
            'ur': 'Urdu',
            'uz': 'Uzbek',
            'vi': 'Vietnamese',
            'cy': 'Welsh',
            'wo': 'Wolof',
            'fy': 'Western Frisian',
            'xh': 'Xhosa',
            'yi': 'Yiddish',
            'yo': 'Yoruba',
            'zu': 'Zulu'
        }


# Заполнение списка поддерживаемых языков
iso_639_1_languages = __get_languages()
