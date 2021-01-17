# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 19:48:05 2020

@author: Berkay
"""

from zipfile import ZipFile
from PIL import Image
from PIL import ImageDraw
import pytesseract
import cv2 as cv
import numpy as np

face_cascade = cv.CascadeClassifier(r'C:\Users\Berkay\Desktop\B\Coursera\Python\frontalface.xml')


def zip_to_image(filename):
    zippedFile = ZipFile(filename)
    data = []
    i = 0
    for file in zippedFile.infolist():
        zippedFile.extract(file)
        image = Image.open(file.filename)
        data.append(dict())
        data[i]["File_name"] = file.filename
        data[i]["Pıl_image"] = image
        i += 1
    return data    
        
def cvt_to_grey(List):
    greyed_list = List
    i = 0
    for Dict in greyed_list:
        im = Dict["Pıl_image"]
        greyed = im.convert("L")
        greyed_list[i]["Pıl_image"] = greyed       
        i += 1
    return greyed_list
    
        
def store_texts(List):
    i = 0
    for Dict in List:
        text = pytesseract.image_to_string(Dict["Pıl_image"])
        Dict["Text"] = text
        i += 1

def List_to_cv(List):
    for Dict in List:
        img = cv.imread(Dict["File_name"])
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        #bin_img = to_bin(gray, mid)
        faces = face_cascade.detectMultiScale(gray)
        Dict["cv_boxes"] = faces
    
    
        
def to_bin(cv_img, mid):
    bin_img = cv.threshold(cv_img, mid, 255, cv.THRESH_BINARY)[1]
    return bin_img

def rect(List):
    for Dict in List:
        img = cv.imread(Dict["File_name"])
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        pil_img = Image.fromarray(gray, mode="L")
        drawing = ImageDraw.Draw(pil_img)
        for i in range(len(Dict["cv_boxes"].tolist())):
            rec = Dict["cv_boxes"].tolist()[i]
            drawing.rectangle((rec[0], rec[1], rec[0] +rec [2], rec[1] + rec[3]), outline = "white", width = 5)
        display(pil_img)
        
def find_matches(string, List):
    for i in range(len(List)):
        if string.lower() in List[i]["Text"].lower():
            List[i]["found"] = True
        else:
            List[i]["found"] = False
            
def contact_sheets(List):
    for Dict in List:
        if Dict["found"]:
            print("Found on {}".format(Dict["File_name"]))
            img = Image.open(Dict["File_name"])
            size = (500, (len(Dict["cv_boxes"].tolist()) // 5 + 1) * 100)
            contact_sheet = Image.new(img.mode, size)
            for i in range(len(Dict["cv_boxes"].tolist())):    
                rec = Dict["cv_boxes"].tolist()[i]
                face = (rec[0], rec[1], rec[0] +rec [2], rec[1] + rec[3])
                cropped = img.crop(face)
                final = cropped.resize((100, 100))
                contact_sheet.paste(final, ((i % 4)*100, i // 4))
            contact_sheet.save("contact_sheet{}".format(Dict["File_name"]), format = "png")  
                
data_small = cvt_to_grey(zip_to_image(r'C:\Users\Berkay\Desktop\B\Coursera\Python\small_img.zip'))

#data_big = cvt_to_grey(zip_to_image("readonly/images.zip"))        
            
Str = input("Enter a string to create a contact sheet which contains faces on the newspaper in which the string exists:")

file = input("Which file you want to search in (1- small_img.zip, 2- images.zip):")

while True:
    if file == "1":
        data = data_small
    else:
        data = data_big
   
    store_texts(data)

    find_matches(Str, data)

    List_to_cv(data)

    contact_sheets(data)

    Str = input("Enter a string to create a contact sheet which contains faces on the newspaper in which the string exists:")

    file = input("Which file you want to search in (1- small_img.zip, 2- images.zip):")           
                
            
            
            
            
        
        
        
    
    