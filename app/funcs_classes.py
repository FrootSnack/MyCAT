import json
from exceptions import ConfigInputError, ConfigOutputError, DictConversionError, NoTranslationConfigError
from os.path import abspath, exists


class Point:
    def __init__(self, x: int, y: int) -> None:
        try:
            assert type(x) is int
            self.x = x
            assert type(y) is int
            self.y = y
        except AssertionError:
            raise TypeError("All initialization values must be of the correct type.")
    
    def __eq__(self, __o: object) -> bool:
        return type(__o) == Point and self.x == __o.x and self.y == __o.y


    def to_dict(self) -> dict:
        return {'x': self.x, 'y': self.y}

    def to_tuple(self) -> tuple[int, int]:
        """Returns the Point object as a tuple of the form (x, y)"""
        return (self.x, self.y)

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
            raise TypeError("All initialization values must be of the correct type.")
    
    def __eq__(self, __o: object) -> bool:
        return self.R == __o.R and self.G == __o.G and self.B == __o.B

    def __hash__(self) -> int:
        return hash((self.R, self.G, self.B))

    def to_dict(self) -> dict:
        try:
            out_dict: dict = {}
            out_dict['R'] = self.R
            out_dict['G'] = self.G
            out_dict['B'] = self.B
            return out_dict
        except Exception:
            DictConversionError("Color")
    
    def to_tuple(self) -> tuple:
        return (self.R, self.G, self.B)

class Translation:
    def __init__(self, xPos: int, yPos: int, width: int, height: int,\
         textColor: Color = Color(255, 255, 255), backgroundColor: Color = Color(0, 0, 0),\
             originalText: str = '', translatedText: str = '') -> None:
        try:
            assert type(xPos) is int
            self.xPos = xPos
            assert type(yPos) is int
            self.yPos = yPos
            assert type(width) is int
            self.width = width
            assert type(height) is int
            self.height = height
            assert type(textColor) is Color
            self.textColor = textColor
            assert type(backgroundColor) is Color
            self.backgroundColor = backgroundColor
            assert type(originalText) is str
            self.originalText = originalText
            assert type(translatedText) is str
            self.translatedText = translatedText
        except AssertionError:
            raise TypeError("All initialization values must be of the correct type.")
    
    def to_dict(self) -> dict:
        try:
            out_dict: dict = {}
            out_dict['xPos'] = self.xPos
            out_dict['yPos'] = self.yPos
            out_dict['width'] = self.width
            out_dict['height'] = self.height
            out_dict['textColor'] = self.textColor.to_dict()
            out_dict['backgroundColor'] = self.backgroundColor.to_dict()
            out_dict['originalText'] = self.originalText
            out_dict['translatedText'] = self.translatedText
            return out_dict
        except Exception:
            raise DictConversionError("Translation")

class TranslationConfig:
    def __init__(self, originalFileName: str, outputFileName: str) -> None:
        try:
            if 0 in [len(originalFileName), len(outputFileName)] \
                or '.' not in originalFileName or '.' not in outputFileName:
                raise ValueError("Improper file naming convention!")
            assert type(originalFileName) is str
            self.originalFileName = abspath(originalFileName)
            assert type(outputFileName) is str
            self.outputFileName = abspath(outputFileName)
            self.translations = []
        except AssertionError:
            raise TypeError("All initialization values must be of the correct type.")

    def to_dict(self) -> dict:
        try:
            out_dict: dict = {}
            out_dict['originalFileName'] = self.originalFileName
            out_dict['outputFileName'] = self.outputFileName
            dict_translations: list = []
            for page in self.translations:
                dict_translations.append([t.to_dict() for t in page])
            out_dict['translations'] = dict_translations
            return out_dict
        except Exception:
            DictConversionError("TranslationConfig")

    def save(self) -> None:
        output_translationconfig_to_tr(f"{self.originalFileName.split('.')[0]}.tr", self)


def import_tr_to_translationconfig(filepath: str) -> TranslationConfig:
    if not exists(filepath):
        raise NoTranslationConfigError
    if '.' in filepath and filepath.split('.')[1].lower() != 'tr':
        raise ValueError("Given filepath does not have the .tr extension.")
    try:
        with open(filepath, 'r') as f:
            tr_dict: dict = json.load(f)
        out_config: TranslationConfig = TranslationConfig(tr_dict['originalFileName'], tr_dict['outputFileName'])
        for page in tr_dict['translations']:
            page_list: list = []
            for tr in page:
                page_list.append(Translation(tr['xPos'], tr['yPos'], tr['width'], tr['height'],\
                    Color(tr['textColor']['R'], tr['textColor']['G'], tr['textColor']['B']),\
                    Color(tr['backgroundColor']['R'], tr['backgroundColor']['G'], tr['backgroundColor']['B']),\
                        tr['originalText'], tr['translatedText']))
            out_config.translations.append(page_list)
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
