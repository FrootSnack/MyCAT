from gettext import translation
import cv2
import numpy as np
import os
import tempfile
from main import Point, Translation, TranslationConfig, output_translationconfig_to_tr
from pdf2image import convert_from_path
from tkinter import filedialog as fd

# TODO: Add post-processing for .tr files (may need to be a separate program). Should scan image to find most common (background) and second most common (foreground) colors
# TODO: Add post-processing for .tr files to grab text with OCR and place it into the originalText field
# TODO: Create interface (may need to be a separate program) where translator may view OCR text and input their translation.
# TODO: Add finalization step (may need to be a separate program) that blanks the given translation area with the background color and places the translation text in the foreground color.
  
translation_list: list = []
start_point: Point = None
mouse_pressed: bool = False
current_img = None
img_ind: int = 0
max_img_ind = 0
img_copy = None
pdf_file_name: str = ''


# This function works exactly as intended at the moment. 
def click_event(event, x, y, flags, params) -> None:
    global translation_list
    global start_point
    global mouse_pressed
    global current_img
    global img_ind
    global max_img_ind
    global img_copy
    global pdf_file_name

    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = Point(x, y)
        mouse_pressed = True
    elif event == cv2.EVENT_MOUSEMOVE and mouse_pressed:
        # draw rectangle with corners at start_point and current position
        img_copy = current_img.copy()
        cv2.rectangle(img_copy, start_point.to_tuple(), (x, y), (0, 0, 255), 2)
        cv2.imshow('PDF', img_copy)
    elif event == cv2.EVENT_LBUTTONUP:
        translation_list.append(Translation(xPos=start_point.x, yPos=start_point.y,\
             width=x-start_point.x, height=y-start_point.y))
        current_img = img_copy
        print(translation_list[-1].to_dict())
        mouse_pressed = False
    # Middle click progresses the PDF to the next page
    elif event == cv2.EVENT_MBUTTONDOWN:
        # Save the given translations to a .tr file (will need to be processed further)
        out_file_name: str = f"{pdf_file_name.split('.')[0]}_{img_ind}.tr"
        out_trconfig: TranslationConfig = TranslationConfig(pdf_file_name, f"{pdf_file_name.split('.')[0]}_out.pdf")
        out_trconfig.translations = translation_list
        output_translationconfig_to_tr(out_file_name, out_trconfig)

        # Turn to the next page
        img_ind = 0 if img_ind == max_img_ind else img_ind+1
        target_path: str = "temp.jpg"
        image_list[img_ind].save(target_path, 'JPEG')
        current_img = cv2.imread(target_path)
        cv2.imshow('PDF', current_img)

 
if __name__=="__main__":
    pdf_file_name = ''
    while pdf_file_name == '' or not os.path.exists(pdf_file_name)\
         or pdf_file_name.split('.')[1].lower() != 'pdf':
        pdf_file_name = fd.askopenfilename()
    
    image_list: list = convert_from_path(pdf_file_name)
    # Touch nothing above this line
    
    max_img_ind = len(image_list) - 1
    
    
    target_path: str = "temp.jpg"
    image_list[0].save(target_path, 'JPEG')
    current_img = cv2.imread(target_path)
    cv2.imshow('PDF', current_img)
    cv2.setMouseCallback('PDF', click_event)
    cv2.waitKey(0)

    exit()

    # new loop
    with tempfile.TemporaryDirectory() as td:
        image_ind: int = 0
        max_image_ind = len(image_list) - 1
        cv2.setMouseCallback('PDF', click_event)
        while True:
            target_path: str = os.path.join(td, f"temp.jpg")
            image_list[image_ind].save(target_path, 'JPEG')
            current_img = cv2.imread(target_path)
            cv2.imshow('PDF', current_img)

            key: int = cv2.waitKey(0)
            
            # Left arrow key
            if key == 2:
                image_ind = max_image_ind if image_ind==0 else image_ind-1
            # Right arrow key
            elif key == 3:
                image_ind = 0 if image_ind==max_image_ind else image_ind+1
            # Escape key
            elif key == 27:
                break
    exit()

    # old loop
    with tempfile.TemporaryDirectory() as td:
        for ind, img in enumerate(image_list):
            print(f"Image {ind+1}")
            target_path: str = os.path.join(td, f"{str(ind)}.jpg")
            img.save(target_path, 'JPEG')
            current_img = cv2.imread(target_path)
            cv2.imshow('PDF', current_img)
            k = cv2.waitKey(0)
            
            print(k)
            if k == 27:
                break
            elif k == 2:
                print("Left!")
            elif k == 3:
                print("Right!")
            continue
    exit()
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
    # close the window
    cv2.destroyAllWindows()

    exit()
    

    # reading the image
    img = cv2.imread('test.jpg', 1)
 
    # displaying the image
    cv2.imshow('image', img)
 
    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)

    # Add keyboard callback for escape (returns to processing for .tr file)
 
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
 
    # close the window
    cv2.destroyAllWindows()