import cv2
import numpy as np
import os
import pytesseract
import re
import tempfile
from collections import Counter
from funcs_classes import import_tr_to_translationconfig, TranslationConfig, Translation, Color
from pdf2image import convert_from_path

tessdata_dir_config = r'--tessdata-dir "/Users/nolanwelch/homebrew/Cellar/tesseract/5.2.0/share/tessdata"'
text_ratio: float = 0.1  # Estimate of how much of a selection will be text; used to find non-background pixels

def run(tr_cfg: TranslationConfig) -> None:
    temp_dir: str = tempfile.mkdtemp()
    temp_path: str = os.path.join(temp_dir, 'temp.jpg')

    original_pdf_path: str = tr_cfg.originalFileName
    original_image_list: list = convert_from_path(original_pdf_path)
    
    page: list
    for page_ind, page in enumerate(original_image_list):
        if page_ind >= len(tr_cfg.translations):
            break

        page.save(temp_path, 'JPEG')
        page_img = cv2.imread(temp_path)
        
        
        cfg_page: list = tr_cfg.translations[page_ind]

        translation: Translation
        for translation in cfg_page:
            # Cropping the image to only include the selected region
            end_x: int = translation.xPos + translation.width
            end_y: int = translation.yPos + translation.height
            cropped_page_img = page_img[translation.yPos:end_y, translation.xPos:end_x]
            cropped_page_img = cv2.cvtColor(cropped_page_img, cv2.COLOR_BGR2RGB)
            # Using pytesseract to extract the text from the cropped region and adding it to the Translation
            original_text: str = pytesseract.image_to_string(cropped_page_img, config=tessdata_dir_config)
            original_text = re.sub('\n', ' ', original_text)
            original_text = re.sub('\u2019', '\'', original_text)
            translation.originalText = original_text.strip()
            # Finds the most- and second-most common colors to be the background and foreground colors respectively
            img_height, img_width, _ = cropped_page_img.shape
            color_list: list = []
            for x in range(img_width):
                for y in range(img_height):
                    color_list.append(Color(int(cropped_page_img[y,x][0]), int(cropped_page_img[y,x][1]), int(cropped_page_img[y,x][2])))
            color_list.sort(key=Counter(color_list).get, reverse=True)
            print([x.as_tuple() for x in color_list])
            translation.backgroundColor = color_list[0]
            color_ctr = Counter(color_list)
            # TODO: Filter out values close to white.
            translation.textColor = color_ctr.most_common(2)[1][0]
            # translation.textColor = color_list[-int(img_height*img_width*text_ratio)]
    tr_cfg.save()

    