from funcs_classes import import_tr_to_translationconfig, TranslationConfig, Translation
from os import system

def run(tr_file_name: str) -> None:
    tr_cfg: TranslationConfig = import_tr_to_translationconfig(tr_file_name)
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