import tempfile
import os
from funcs_classes import import_tr_to_translationconfig, Translation, TranslationConfig
from pdf2image import convert_from_path
from PIL import Image, ImageDraw

def run(tr_file_name: str) -> None:
    temp_dir: str = tempfile.mkdtemp()
    temp_path: str = os.path.join(temp_dir, 'temp.jpg')
    
    tr_cfg: TranslationConfig = import_tr_to_translationconfig(tr_file_name)
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
            rect_corners: list = [(tr.xPos, tr.yPos), (tr.xPos+tr.width, tr.yPos+tr.height)]
            fill_color: tuple = tr.backgroundColor.to_tuple()
            draw.rectangle(xy=rect_corners, fill=fill_color)
            # TODO: Add text drawing & checking for size
        if page_ind == 0:
            starting_image = current_image.convert('RGB') 
        else:
            output_images_list.append(current_image).convert('RGB') 
    # Output to final PDF
    starting_image.save(output_pdf_path, save_all=True, append_images=output_images_list)