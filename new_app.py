import cv2
import numpy as np
import tempfile
from main import Point
from os.path import exists
from pdf2image import convert_from_path
from tkinter import filedialog as fd
  
def click_event(event, x, y, flags, params) -> Point:
    if event in [cv2.EVENT_LBUTTONDOWN, cv2.EVENT_RBUTTONDOWN]:
        print(Point(x, y).to_dict())
        return Point(x, y)
    return None
 
 
# driver function
if __name__=="__main__":
    pdf_file_name = ''
    while pdf_file_name == '' or not exists(pdf_file_name) or pdf_file_name.split('.')[1].lower() != 'pdf':
        pdf_file_name = fd.askopenfilename()
    
    image_list: list = convert_from_path(pdf_file_name)

    with tempfile.TemporaryDirectory() as td:
        print(td)
    exit()
    for image in image_list:
        cv2_img = np.array(image.convert('RGB'))
        cv2_img = cv2_img[:, :, ::-1].copy() 
        

    # reading the image
    img = cv2.imread('test.jpg', 1)
 
    # displaying the image
    cv2.imshow('image', img)
 
    # setting mouse handler for the image
    # and calling the click_event() function
    cv2.setMouseCallback('image', click_event)
 
    # wait for a key to be pressed to exit
    cv2.waitKey(0)
 
    # close the window
    cv2.destroyAllWindows()