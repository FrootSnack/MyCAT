from fnmatch import translate
import json
from typing import Type
from urllib.parse import ParseResultBytes

from click import File
from exceptions import DictConversionError, NoTranslationConfigError, ConfigInputError, ConfigOutputError
from fpdf import FPDF
from os.path import exists

class Color:
    def __init__(self, R: int, G: int, B: int) -> None:
        try:
            assert type(R) is int
            self.R = R
            assert type(G) is int
            self.G = G
            assert type(B) is int
            self.B = B
        except AssertionError:
            raise AssertionError("All initialization values must be of the correct type.")

    def to_dict(self) -> dict:
        try:
            out_dict: dict = {}
            out_dict['R'] = self.R
            out_dict['G'] = self.G
            out_dict['B'] = self.B
            return out_dict
        except Exception:
            DictConversionError("Color")

class Translation:
    def __init__(self, xPos: int, yPos: int, textColor: Color,\
         backgroundColor: Color, originalText: str, translatedText: str) -> None:
        try:
            assert type(xPos) is int
            self.xPos = xPos
            assert type(yPos) is int
            self.yPos = yPos
            assert type(textColor) is Color
            self.textColor = textColor
            assert type(backgroundColor) is Color
            self.backgroundColor = backgroundColor
            assert type(originalText) is str
            self.originalText = originalText
            assert type(translatedText) is str
            self.translatedText = translatedText
        except AssertionError:
            raise AssertionError("All initialization values must be of the correct type.")
    
    def to_dict(self) -> dict:
        try:
            out_dict: dict = {}
            out_dict['xPos'] = self.xPos
            out_dict['yPos'] = self.yPos
            out_dict['textColor'] = self.textColor.to_dict()
            out_dict['backgroundColor'] = self.backgroundColor.to_dict()
            out_dict['originalText'] = self.originalText
            out_dict['translatedText'] = self.translatedText
        except Exception:
            DictConversionError("Translation")

class TranslationConfig:
    def __init__(self, originalFileName: str, outputFileName: str) -> None:
        try:
            if 0 in [len(originalFileName), len(outputFileName)] \
                or '.' not in originalFileName or '.' not in outputFileName:
                raise FileNotFoundError("Improper file naming convention!")
            assert type(originalFileName) is str
            self.originalFileName = originalFileName
            assert type(outputFileName) is str
            self.outputFileName = outputFileName
            self.translations = []
        except AssertionError:
            raise AssertionError("All initialization values must be of the correct type.")
    
    def add_translation(self, translation: Translation) -> None:
        try:
            assert type(translation) is Translation
            self.translations.append(translation)
        except AssertionError:
            raise AssertionError("Provided object is not a Translation.")

    def to_dict(self) -> dict:
        try:
            out_dict: dict = {}
            out_dict['originalFileName'] = self.originalFileName
            out_dict['outputFileName'] = self.outputFileName
            out_dict['translations'] = [t.to_dict() for t in self.translations]
            return out_dict
        except Exception:
            DictConversionError("TranslationConfig")


def import_tr_to_translationconfig(filepath: str) -> TranslationConfig:
    if not exists(filepath):
        raise NoTranslationConfigError
    if '.' in filepath and filepath.split('.')[1].lower() != 'tr':
        raise FileNotFoundError("Given filepath does not have the .tr extension.")
    try:
        with open(filepath, 'r') as f:
            tr_dict: dict = json.load(f)
        out_config: TranslationConfig = TranslationConfig(tr_dict['originalFileName'], tr_dict['outputFileName'])
        out_config.translations = tr_dict['translations']
        return out_config
    except Exception:
        raise ConfigInputError


def output_translationconfig_to_tr(filepath: str, translation_config: TranslationConfig) -> None:
    if not exists(filepath):
        f = open(filepath, 'w+')
        f.close()
    try:
        translation_dict: dict = translation_config.to_dict()
        with open(filepath, 'w') as f:
            json.dump(translation_dict, f, indent=4)
    except Exception:
        raise ConfigOutputError


def main() -> None:
    pass

if __name__ == '__main__':
    main()