import annotate_pdf
import extract_image_data
import translate_text
import write_translations

# TODO: Add finalization step (separate program) that blanks the given translation area with the background color and places the translation text in the foreground color.
# TODO: Once done, remove all the messy imports via tr_file_name and just pass the TranslationConfig object itself around.


if __name__ == '__main__':
    tr_file_name: str = annotate_pdf.run()
    extract_image_data.run(tr_file_name)
    translate_text.run(tr_file_name)
    write_translations.run(tr_file_name)
