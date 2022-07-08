import cv2
import numpy as np
import os
import tempfile
from main import Point, Translation, Color
from pdf2image import convert_from_path
from tkinter import filedialog as fd
  
translation_list: list[Translation] = []
index: int = 1
point: Point = None

def click_event(event, x, y, images, flags, params) -> None:
    if event == cv2.EVENT_LBUTTONDOWN:
        print(Point(x, y).to_dict())
        if index % 2 == 1:
            point = Point(x, y)
        else:
            translation_list.append(Translation(x=point.x, y=point.y, width=x-point.x, height=y-point.y))
        return Point(x, y)
    elif event == cv2.EVENT_RBUTTONDOWN:
        # Go to the next image
        pass
 
def display_back(event, x, y, flags, params) -> None:
    pass

 
# driver function
if __name__=="__main__":
    pdf_file_name = ''
    while pdf_file_name == '' or not os.path.exists(pdf_file_name) or pdf_file_name.split('.')[1].lower() != 'pdf':
        pdf_file_name = fd.askopenfilename()
    
    image_list: list = convert_from_path(pdf_file_name)


    with tempfile.TemporaryDirectory() as td:
        for ind, img in enumerate(image_list):
            target_path: str = os.path.join(td, f"{str(ind)}.jpg")
            img.save(target_path, 'JPEG')
            print(target_path)
            cv2_img = cv2.imread(target_path, 1)
            cv2.imshow('image', img)

        
    

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