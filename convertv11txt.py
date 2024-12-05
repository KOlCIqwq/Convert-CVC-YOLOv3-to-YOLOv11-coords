'''
Convert the CVC-YOLOv3 format to YOLOv11 txt format
'''

import csv
import os
import re

# Normalize bounding box
def NormalizeBbox(bbox,width,height,id):
    x,y,h,w = [int(coord) for coord in bbox.strip('[]').split(',')]
    x = x
    y = y
    w = w
    h = h
    id = 1 # This is an id that need to be changed, since the data don't tell which class, leave it 1
    centerX = (x + w/2) / width
    centerY = (y + h/2) / height
    normWidth = w / width
    normHeight = h / height
    return f"{id} {centerX:.6f} {centerY:.6f} {normWidth:.6f} {normHeight:.6f}"

# Clear Corrupted Data
def cleanbboxData(bboxData):
    cleaned = re.findall(r'\[\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\]',bboxData)
    return cleaned

csvPath = "./inputs/yolov3-training-validate.csv"
outputDir = "./output/"

os.makedirs(outputDir,exist_ok=True)

with open(csvPath) as f:
    reader = csv.reader(f)
    for row in reader:
        # Skip if the name of the image is empty
        if row[0] == '':
            continue
        imageName = row[0].strip()
        imageWidth = int(row[2])
        imageHeight = int(row[3])
        scale = float(row[4])
        rawBboxes = ','.join(row[5:])

        bboxes = cleanbboxData(rawBboxes)

        txtFile = os.path.splitext(imageName)[0] + '.txt'

        with open(os.path.join(outputDir,txtFile),'w') as txt:
            for i,bbox in enumerate(bboxes):
                id = i
                txt.write(NormalizeBbox(bbox,imageWidth,imageHeight,id) + '\n')