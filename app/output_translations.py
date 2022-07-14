from funcs_classes import Translation, TranslationConfig
from os import path
from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path
from tempfile import mkdtemp
from textwrap import TextWrapper

max_font_size: int = 120
min_font_size: int = 16

def run(tr_cfg: TranslationConfig) -> None:
    temp_path: str = path.join(mkdtemp(), 'temp.jpg')
    
    original_images_list: list = convert_from_path(tr_cfg.originalFileName)
    output_pdf_path = tr_cfg.outputFileName
    output_images_list: list = []
    starting_image = None

    for page_ind, page_image in enumerate(original_images_list):
        # Save pdf image to a temporary directory and create a canvas on top of it
        page_image.save(temp_path, 'JPEG')
        current_image = Image.open(temp_path)
        draw = ImageDraw.Draw(current_image)
        
        tr: Translation
        for tr in tr_cfg.translations[page_ind]:
            # Blank out the selection with the given background color
            rect_corners: list = [(tr.xPos, tr.yPos), (tr.xPos+tr.width, tr.yPos+tr.height)]
            fill_color: tuple = tr.backgroundColor.to_tuple()
            draw.rectangle(xy=rect_corners, fill=fill_color)
            # Draw the translation string over the selection using the given text color
            font_size: int = max_font_size
            font = None
            wrapped_text: str = ''
            # Start at max_font_size and work down to min_font_size to find the right size
            while font_size >= min_font_size:
                font = ImageFont.truetype('assets/arial.ttf', font_size)
                # Find the approximate width in characters of the selected area at size font_size
                width_in_chars: int = int(tr.width/font.getsize('o')[0])
                # Split the text across lines at the given character using textwrap
                wrapper = TextWrapper(width=width_in_chars)
                wrapped_text = wrapper.wrap(text=tr.translatedText)
                # Approximate the height of the text generated with textwrap
                line_count: int = len(wrapped_text)
                wrapped_text = ('\n').join(wrapped_text)
                text_height_px: int = int(font.getsize(wrapped_text)[1])*line_count
                # If the text fits within the vertical range of the selection, font size is correct
                if text_height_px < tr.height:
                    break
                font_size -= 1
            text_loc: tuple = (tr.xPos, tr.yPos)
            text_color: tuple = tr.textColor.to_tuple()
            draw.multiline_text(xy=text_loc, text=wrapped_text, fill=text_color, font=font)
        if page_ind == 0:
            starting_image = current_image.convert('RGB') 
        else:
            output_images_list.append(current_image.convert('RGB'))
    # Output to final PDF
    starting_image.save(output_pdf_path, save_all=True, append_images=output_images_list)