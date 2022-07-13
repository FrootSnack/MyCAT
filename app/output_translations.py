import os
import tempfile
import textwrap
from funcs_classes import Translation, TranslationConfig
from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path

max_font_size: int = 60
min_font_size: int = 24

def run(tr_cfg: TranslationConfig) -> None:
    temp_dir: str = tempfile.mkdtemp()
    temp_path: str = os.path.join(temp_dir, 'temp.jpg')
    
    original_images_list: list = convert_from_path(tr_cfg.originalFileName)
    output_pdf_path = tr_cfg.outputFileName
    output_images_list: list = []
    starting_image = None

    for page_ind, page_image in enumerate(original_images_list):
        if page_ind == len(tr_cfg.translations):
            break

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
            while font_size >= min_font_size:
                font = ImageFont.truetype('assets/arial.ttf', font_size)
                width_in_chars: int = int(tr.width/font.getsize('o')[0])
                wrapper = textwrap.TextWrapper(width=width_in_chars)
                wrapped_text = wrapper.wrap(text=tr.translatedText)
                line_count: int = len(wrapped_text)
                wrapped_text = ('\n').join(wrapped_text)
                text_height_px: int = int(font.getsize(wrapped_text)[1])*line_count
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