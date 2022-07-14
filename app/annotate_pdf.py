import cv2
import os
import shutil
import tempfile
from funcs_classes import Point, Translation, TranslationConfig
from pdf2image import convert_from_path
from tkinter import filedialog as fd


image_list: list = []
start_point: Point = None
mouse_pressed: bool = False
current_img = None
img_ind: int = 0
max_img_ind = 0
img_copy = None
pdf_file_name: str = ''
temp_dir: str = tempfile.mkdtemp()
temp_path: str = os.path.join(temp_dir, 'temp.jpg')
tr_config: TranslationConfig = None


def click_event(event, x, y, flags, params) -> None:
    global start_point
    global mouse_pressed
    global current_img
    global image_list
    global img_ind
    global max_img_ind
    global img_copy
    global pdf_file_name
    global tr_config

    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = Point(x, y)
        mouse_pressed = True
    
    elif event == cv2.EVENT_MOUSEMOVE and mouse_pressed:
        img_copy = current_img.copy()
        # Draw red rectangle with corners at start_point and current position
        cv2.rectangle(img_copy, start_point.to_tuple(), (x, y), (0, 0, 255), 2)
        cv2.imshow('PDF', img_copy)
    
    elif event == cv2.EVENT_LBUTTONUP:
        if x > start_point.x and y > start_point.y:
            tr_config.translations[img_ind].append(Translation(start_point.x, start_point.y, x-start_point.x, y-start_point.y))
            current_img = img_copy
        mouse_pressed = False
        cv2.imshow('PDF', current_img)
    
    # Middle click progresses the PDF to the next page
    elif event == cv2.EVENT_MBUTTONDOWN:
        # Turn to the next page
        img_ind = 0 if img_ind == max_img_ind else img_ind+1
        image_list[img_ind].save(temp_path, 'JPEG')
        current_img = cv2.imread(temp_path)
        cv2.imshow('PDF', current_img)

 
def run() -> TranslationConfig:
    global image_list
    global max_img_ind
    global current_img
    global pdf_file_name
    global tr_config

    pdf_file_name = ''
    while pdf_file_name == '' or not os.path.exists(pdf_file_name)\
         or pdf_file_name.split('.')[1].lower() != 'pdf':
        pdf_file_name = fd.askopenfilename()
    
    image_list = convert_from_path(pdf_file_name)
    max_img_ind = len(image_list)-1

    tr_config = TranslationConfig(pdf_file_name, f"{pdf_file_name.split('.')[0]}_out.pdf")
    tr_config.translations = [[] for x in range(len(image_list))]
    
    image_list[0].save(temp_path, 'JPEG')
    current_img = cv2.imread(temp_path)
    cv2.imshow('PDF', current_img)
    cv2.setMouseCallback('PDF', click_event)
    cv2.waitKey(0)

    tr_config.save()
    shutil.rmtree(temp_dir)
    cv2.destroyAllWindows()
    return tr_config
