import annotate_pdf
import extract_image_data
import translate_text
import output_translations
from funcs_classes import TranslationConfig

# TODO: Add finalization step (separate program) that blanks the given translation area with the background color and places the translation text in the foreground color.
# TODO: Once done, remove all the messy imports via tr_file_name and just pass the TranslationConfig object itself around.

if __name__ == '__main__':
    tr_cfg: TranslationConfig = annotate_pdf.run()
    extract_image_data.run(tr_cfg)
    translate_text.run(tr_cfg)
    output_translations.run(tr_cfg)
