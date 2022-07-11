import tempfile
import os
from funcs_classes import Translation, TranslationConfig
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont

font_ratio: float = 240  # How much font size should be relatively in/deflated (higher number means a smaller font)
arial_avg_char_width_px: float = 0.716

def run(tr_cfg: TranslationConfig) -> None:
    temp_dir: str = tempfile.mkdtemp()
    temp_path: str = os.path.join(temp_dir, 'temp.jpg')
    
    original_images_list: list = convert_from_path(tr_cfg.originalFileName)
    output_pdf_path = tr_cfg.outputFileName
    output_images_list: list = []
    starting_image = None

    for page_ind, page in enumerate(tr_cfg.translations):
        current_image = original_images_list[page_ind]
        current_image.save(temp_path, 'JPEG')
        current_image = Image.open(temp_path)
        draw = ImageDraw.Draw(current_image)
        
        tr: Translation
        for tr in page:
            # Blank out the selection with the given background color
            rect_corners: list = [(tr.xPos, tr.yPos), (tr.xPos+tr.width, tr.yPos+tr.height)]
            fill_color: tuple = tr.backgroundColor.to_tuple()
            draw.rectangle(xy=rect_corners, fill=fill_color)
            # Draw the translation string over the selection using the given text color
            # pixel_area: int = tr.width * tr.height
            
            # font_size: int = int((pixel_area/len(tr.translatedText)) / font_ratio)
            
            font = ImageFont.truetype('assets/arial.ttf', 55)
            text_loc: tuple = (tr.xPos, tr.yPos)
            text_color: tuple = tr.textColor.to_tuple()
            print(text_color)
            draw.text(xy=text_loc, text=tr.translatedText, fill=text_color, font=font)
        if page_ind == 0:
            starting_image = current_image.convert('RGB') 
        else:
            output_images_list.append(current_image).convert('RGB') 
    # Output to final PDF
    starting_image.save(output_pdf_path, save_all=True, append_images=output_images_list)