import torch
import cv2
import numpy as np
import os
import wx

def detect_licenseplates(images, output, self):
    
    progress = wx.ProgressDialog("Censoring in progress", "please wait", maximum=100, parent=self, style=wx.PD_SMOOTH|wx.PD_AUTO_HIDE)
    percent = 0
    progress.Update(percent)
    
    # Step 1: Load the YOLO model from a .pt file
    model_path = 'models\\best.pt'  # Replace with the path to your YOLO model
    model = torch.hub.load('ultralytics/yolov5:master', 'custom', path=model_path)  # 'custom' model for loading from a .pt file
    model.eval()
    classes = model.names
    
    print(classes)
    try: 
        os.mkdir(output) 
    except FileExistsError as error: 
        None
        
    percent_per_image = int(100 / len(images))
    # Step 2: Load and process the input image
    for image in images:
        percent += percent_per_image
        progress.Update(percent)
        img = cv2.imread(image)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, c = img.shape
        
        # Step 3: Perform object detection
        results = model(img_rgb, w if w > h else h)
        print(results)
        print(image)

        # You can also access the detected objects and their information
        detected_objects = results.pandas().xyxy[0]  # Get detected objects as a Pandas DataFrame
        
        # Create a copy of the image to apply blur
        img_with_blur = img.copy()

        for _, obj in detected_objects.iterrows():
            box = [int(obj.iloc[0]), int(obj.iloc[1]), int(obj.iloc[2]), int(obj.iloc[3])]
            
            # Extract the bounding box coordinates
            x1, y1, x2, y2 = box
            
            # Crop and blur the region within the bounding box
            roi = img[y1:y2, x1:x2]
            blurred_roi = cv2.GaussianBlur(roi, (21, 21), 0)
            
            # Replace the region in the original image with the blurred version
            img_with_blur[y1:y2, x1:x2] = blurred_roi
        
        # Save the modified image with the blurred bounding boxes
        output_image_path = os.path.join(output, os.path.basename(image))
        cv2.imwrite(output_image_path, img_with_blur)
    progress.Destroy()
