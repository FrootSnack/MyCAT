import cv2
import numpy as np
import os
import tempfile
from main import Point, Translation, Color
from pdf2image import convert_from_path
from tkinter import filedialog as fd
  
translation_list: list = []
index: int = 0
start_point: Point = None
mouse_pressed: bool = False

 
def click_event(event, x, y, flags, params) -> None:
    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = Point(x, y)
        mouse_pressed = True
        print("Test!")
    elif event == cv2.EVENT_MOUSEMOVE and mouse_pressed:
        # draw rectangle with corners at start_point and current position
        pass
    elif event == cv2.EVENT_LBUTTONUP:
        translation_list.append(Translation(x=start_point.x, y=start_point.y, width=x-start_point.x, height=y-start_point.y))
        mouse_pressed = False
        # erase the rectangle

 
if __name__=="__main__":
    pdf_file_name = ''
    while pdf_file_name == '' or not os.path.exists(pdf_file_name) or pdf_file_name.split('.')[1].lower() != 'pdf':
        pdf_file_name = fd.askopenfilename()
    
    image_list: list = convert_from_path(pdf_file_name)

    # new loop
    with tempfile.TemporaryDirectory() as td:
        image_ind: int = 0
        max_image_ind = len(image_list) - 1
        cv2.setMouseCallback('PDF', test_event)
        while True:
            target_path: str = os.path.join(td, f"temp.jpg")
            image_list[image_ind].save(target_path, 'JPEG')
            cv2_img = cv2.imread(target_path)
            cv2.imshow('PDF', cv2_img)

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
            cv2_img = cv2.imread(target_path)
            cv2.imshow('PDF', cv2_img)
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