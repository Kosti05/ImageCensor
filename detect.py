import torch
import cv2
import numpy as np
import os
import wx

def detect_licenseplates(images, output, self):
    progress = wx.ProgressDialog("Censoring in progress", "please wait", maximum=100, parent=self, style=wx.PD_SMOOTH|wx.PD_AUTO_HIDE)
    percent = 0
    progress.Update(percent)
    model_path = 'models\\licenseplates.pt'
    model = torch.hub.load('ultralytics/yolov5:master', 'custom', path=model_path)
    model.eval()
    classes = model.names
    try: 
        os.mkdir(output) 
    except FileExistsError as error: 
        None
    percent_per_image = int(100 / len(images))
    
    for image in images:
        percent += percent_per_image
        progress.Update(percent)
        img = cv2.imread(image)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, c = img.shape
        results = model(img_rgb, w if w > h else h)
        detected_objects = results.pandas().xyxy[0]
        img_with_blur = img.copy()

        for _, obj in detected_objects.iterrows():
            box = [int(obj.iloc[0]), int(obj.iloc[1]), int(obj.iloc[2]), int(obj.iloc[3])]
            x1, y1, x2, y2 = box
            roi = img[y1:y2, x1:x2]
            blurred_roi = cv2.GaussianBlur(roi, (21, 21), 0)
            img_with_blur[y1:y2, x1:x2] = blurred_roi
        
        output_image_path = os.path.join(output, os.path.basename(image))
        cv2.imwrite(output_image_path, img_with_blur)
    progress.Destroy()

def detect_faces(images, output, self):
    progress = wx.ProgressDialog("Censoring in progress", "please wait", maximum=100, parent=self, style=wx.PD_SMOOTH|wx.PD_AUTO_HIDE)
    percent = 0
    progress.Update(percent)
    model_path = 'models\\faces.pt'
    model = torch.hub.load('ultralytics/yolov5:master', 'custom', path=model_path)  # 'custom' model for loading from a .pt file
    model.eval()
    classes = model.names
    try: 
        os.mkdir(output) 
    except FileExistsError as error: 
        None
    percent_per_image = int(100 / len(images))
    
    for image in images:
        percent += percent_per_image
        progress.Update(percent)
        img = cv2.imread(image)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, c = img.shape
        results = model(img_rgb, w if w > h else h)
        detected_objects = results.pandas().xyxy[0]
        img_with_blur = img.copy()

        for _, obj in detected_objects.iterrows():
            box = [int(obj.iloc[0]), int(obj.iloc[1]), int(obj.iloc[2]), int(obj.iloc[3])]
            x1, y1, x2, y2 = box
            roi = img[y1:y2, x1:x2]
            blurred_roi = cv2.GaussianBlur(roi, (21, 21), 0)
            img_with_blur[y1:y2, x1:x2] = blurred_roi

        output_image_path = os.path.join(output, os.path.basename(image))
        cv2.imwrite(output_image_path, img_with_blur)
    progress.Destroy()

def detect_both(images, output, self):
    progress = wx.ProgressDialog("Censoring in progress", "please wait", maximum=100, parent=self, style=wx.PD_SMOOTH|wx.PD_AUTO_HIDE)
    percent = 0
    progress.Update(percent)
    model1_path = 'models\\faces.pt'
    model2_path = 'models\\licenseplates.pt'
    model1 = torch.hub.load('ultralytics/yolov5:master', 'custom', path=model1_path)
    model2 = torch.hub.load('ultralytics/yolov5:master', 'custom', path=model2_path) 
    model1.eval()
    model2.eval()
    try: 
        os.mkdir(output) 
    except FileExistsError as error: 
        None
    percent_per_image = int(100 / len(images))
    
    for image in images:
        percent += percent_per_image
        progress.Update(percent)
        img = cv2.imread(image)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, c = img.shape
        results = model1(img_rgb, w if w > h else h)
        results2 = model2(img_rgb, w if w > h else h)
        detected_objects1 = results.pandas().xyxy[0]
        detected_objects2 = results2.pandas().xyxy[0]
        img_with_blur = img.copy()

        for _, obj in detected_objects1.iterrows():
            box = [int(obj.iloc[0]), int(obj.iloc[1]), int(obj.iloc[2]), int(obj.iloc[3])]
            x1, y1, x2, y2 = box
            roi = img[y1:y2, x1:x2]
            blurred_roi = cv2.GaussianBlur(roi, (21, 21), 0)
            img_with_blur[y1:y2, x1:x2] = blurred_roi
            
        for _, obj in detected_objects2.iterrows():
            box = [int(obj.iloc[0]), int(obj.iloc[1]), int(obj.iloc[2]), int(obj.iloc[3])]
            x1, y1, x2, y2 = box
            roi = img[y1:y2, x1:x2]
            blurred_roi = cv2.GaussianBlur(roi, (21, 21), 0)
            img_with_blur[y1:y2, x1:x2] = blurred_roi

        output_image_path = os.path.join(output, os.path.basename(image))
        cv2.imwrite(output_image_path, img_with_blur)
    progress.Destroy()
