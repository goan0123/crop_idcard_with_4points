import cv2
import numpy as np
import os
from pathlib import Path


img_dir=r"E:\Works\camera\new"
save_dir= Path(img_dir)/"result"

if not os.path.exists(save_dir):
    os.mkdir(save_dir)

file_list=os.listdir(img_dir)
img_list=[img for img in file_list if img.endswith(".jpg")]


COLOR = (0, 0, 255) # BGR
red=(0, 0, 255)
green=(0,255,0)
THICKNESS = 2
drawing = False

def mouse_handler(event, x, y, flags, param):
    global drawing
    copy_img = origin_img.copy()
    
    if event == cv2.EVENT_LBUTTONDOWN : 
        if len(point_list) < 5:
            drawing = True 
            point_list.append((x, y))
    
    if drawing:
        point1 = None # preparation

        # click and added into point_list 
        for current_point in point_list:
            cv2.circle(copy_img, current_point, 5, COLOR, cv2.FILLED)

            if point1:
                # static line
                cv2.line(copy_img, point1, current_point, green, THICKNESS, cv2.LINE_AA) 
            point1 = current_point      

        # active line
        point2 = (x, y)
        cv2.line(copy_img, point1, point2, red, THICKNESS, cv2.LINE_AA)      

    if len(point_list) == 4:
        # show result image and save the image
        show_new_image()   
        point2 = point_list[0]                                              
        drawing=False
        cv2.destroyAllWindows()
        
    cv2.imshow(window1, copy_img)
    
def show_new_image():
    height = origin_img.shape[0]
    width = int(height*1.6)
    
    final_point_list = np.float32(point_list)
    final_coord = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=np.float32) 

    matrix = cv2.getPerspectiveTransform(final_point_list, final_coord) 
    result_img = cv2.warpPerspective(origin_img, matrix, (width, height)) 

    ### save
    save_img_name= img_name
    save_img_path=os.path.join(save_dir, save_img_name)
    cv2.imwrite(save_img_path, result_img)


for img_name in img_list:

    point_list = []

    window1=img_name

    img_path=os.path.join(img_dir, img_name)
    origin_img = cv2.imread(img_path)
    resized_x=float(round(1200/origin_img.shape[1],1))
    origin_img = cv2.resize(origin_img, None, fx=resized_x, fy=resized_x)
    
    cv2.namedWindow(window1)
    cv2.setMouseCallback(window1, mouse_handler)
    cv2.imshow(window1, origin_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()