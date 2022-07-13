from funcs_classes import TranslationConfig, Translation
from os import system

def run(tr_cfg: TranslationConfig) -> None:
    system('clear')
    page: list
    for page in tr_cfg.translations:
        tr: Translation
        for tr in page:
            system('clear')
            print(tr.originalText)
            user_translation: str = ''
            while user_translation.strip() == '':
                user_translation = input('')
            tr.translatedText = user_translation
    system('clear')
    tr_cfg.save()