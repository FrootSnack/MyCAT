from funcs_classes import TranslationConfig, Translation
from tkinter import simpledialog, Tk


def run(tr_cfg: TranslationConfig) -> None:
    root = Tk()
    root.withdraw()

    page: list
    tr: Translation
    for page in tr_cfg.translations:
        for tr in page:
            user_translation: str = simpledialog.askstring(title='Translation', prompt=tr.originalText)
            tr.translatedText = user_translation
    tr_cfg.save()