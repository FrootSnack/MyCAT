import cv2
import numpy as np
import os
import pytesseract
import tempfile
from funcs_classes import import_tr_to_translationconfig, TranslationConfig, Translation, Color
from pdf2image import convert_from_path
from PIL import Image
from tkinter import filedialog as fd

tessdata_dir_config = r'--tessdata-dir "/Users/nolanwelch/homebrew/Cellar/tesseract/5.2.0/share/tessdata"'

def run(tr_file_name: str) -> None:
    temp_dir: str = tempfile.mkdtemp()
    temp_path: str = os.path.join(temp_dir, 'temp.jpg')
    
    tr_cfg: TranslationConfig = import_tr_to_translationconfig(tr_file_name)
    if len(tr_cfg.translations) == 0:
        exit()

    original_pdf_path: str = tr_cfg.originalFileName
    original_image_list: list = convert_from_path(original_pdf_path)
    
    page: list
    for page_ind, page in enumerate(original_image_list):
        page.save(temp_path, 'JPEG')
        page_img = cv2.imread(temp_path)
        
        cfg_page: list = tr_cfg.translations[page_ind]

        translation: Translation
        for translation in cfg_page:
            # Cropping the image to only include the selected region
            end_x: int = translation.xPos + translation.width
            end_y: int = translation.yPos + translation.height

            cropped_page_img = page_img[translation.yPos:end_y, translation.xPos:end_x]
            # Using pytesseract to extract the text from the cropped region and adding it to the Translation
            original_text: str = pytesseract.image_to_string(cropped_page_img, config=tessdata_dir_config)
            translation.originalText = original_text
            # Convert to PIL Image format and pull background (most common) and foreground (second-most common) colors
            pil_img = cv2.cvtColor(cropped_page_img, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(pil_img)
            
            img_colors = sorted(pil_img.getcolors())
            bg_color_tuple: tuple = (img_colors[-1][-1][0], img_colors[-1][-1][1], img_colors[-1][-1][2])
            fg_color_tuple: tuple = (img_colors[-2][-1][0], img_colors[-2][-1][1], img_colors[-2][-1][2])
            translation.backgroundColor = Color(bg_color_tuple[0], bg_color_tuple[1], bg_color_tuple[2])
            translation.textColor = Color(fg_color_tuple[0], fg_color_tuple[1], fg_color_tuple[2])
    tr_cfg.save()

    