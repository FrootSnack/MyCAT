import annotate_pdf
import extract_image_data
import translate_text
import output_translations
import os
from funcs_classes import TranslationConfig

os.chdir('/Users/nolanwelch/Documents/CAT')

if __name__ == '__main__':
    tr_cfg: TranslationConfig = annotate_pdf.run()
    extract_image_data.run(tr_cfg)
    translate_text.run(tr_cfg)
    output_translations.run(tr_cfg)
