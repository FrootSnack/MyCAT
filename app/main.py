import annotate_pdf
import extract_image_data

# TODO: Create (possibly separate) CLI where translator may view OCR text and input their translation and have it added to the translatedText field.
# TODO: Add finalization step (separate program) that blanks the given translation area with the background color and places the translation text in the foreground color.


if __name__ == '__main__':
    tr_file_name: str = annotate_pdf.run()
    extract_image_data.run(tr_file_name)