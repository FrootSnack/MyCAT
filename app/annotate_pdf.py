import cv2
import os
from funcs_classes import Point, Translation, TranslationConfig, output_translationconfig_to_tr
from pdf2image import convert_from_path
from tkinter import filedialog as fd

# TODO: Add post-processing for .tr files (may need to be a separate program). Should scan image to find most common (background) and second most common (foreground) colors
# TODO: Add post-processing for .tr files to grab text with OCR and place it into the originalText field (part of previous item)
# TODO: Create (possibly separate) CLI where translator may view OCR text and input their translation and have it added to the translatedText field.
# TODO: Add finalization step (separate program) that blanks the given translation area with the background color and places the translation text in the foreground color.
  
translation_list: list = []
image_list: list = []
start_point: Point = None
mouse_pressed: bool = False
current_img = None
img_ind: int = 0
max_img_ind = 0
img_copy = None
pdf_file_name: str = ''


def click_event(event, x, y, flags, params) -> None:
    global translation_list
    global start_point
    global mouse_pressed
    global current_img
    global image_list
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
        # Save the given translations to a .tr file
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

 
def main() -> None:
    global image_list
    global max_img_ind
    global current_img
    global pdf_file_name

    pdf_file_name = ''
    while pdf_file_name == '' or not os.path.exists(pdf_file_name)\
         or pdf_file_name.split('.')[1].lower() != 'pdf':
        pdf_file_name = fd.askopenfilename()
    
    image_list = convert_from_path(pdf_file_name)
    
    max_img_ind = len(image_list) - 1
    
    target_path: str = "temp.jpg"
    image_list[0].save(target_path, 'JPEG')
    current_img = cv2.imread(target_path)
    cv2.imshow('PDF', current_img)
    cv2.setMouseCallback('PDF', click_event)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


if __name__=="__main__":
    main()