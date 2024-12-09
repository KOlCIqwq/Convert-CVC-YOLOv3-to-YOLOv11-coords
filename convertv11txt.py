'''
Convert the CVC-YOLOv3 format to YOLOv11 txt format
'''

import csv
import os

# Normalize bounding box
def NormalizeBbox(x,y,w,h,width,height):
    centerX = (x + w/2) / width
    centerY = (y + h/2) / height
    normWidth = w / width
    normHeight = h / height
    return centerX, centerY, normWidth, normHeight

def toNestedList(data):
    processed = []
    temp = []
    count = -1
    for i in range (len(data)):
        count += 1
        if count == 5:
            processed.append(temp)
            temp = []
            count = 0
        if data[i][0] == '[':
            temp.append(data[i][1:])
        elif data[i][0] == '"':
            temp.append(data[i][2:])
        elif data[i][-1] == '"':
            temp.append(data[i][:-2])
        else:
            temp.append(data[i])
        
    
    return processed

csvPath = "./inputs/labels.csv"
outputDir = "./output/"

os.makedirs(outputDir,exist_ok=True)

with open(csvPath) as f:
    reader = csv.reader(f)
    for row in reader:
        if not row[0] or not row[0].strip(): # Skip empty rows
            continue
        if row[1] != '':
            continue
        allInfo = row[0].strip().split(',')
        imageName = allInfo[0]
        if imageName == 'Name':
            continue
        imageWidth = int(allInfo[2])
        imageHeight = int(allInfo[3])
        scale = float(allInfo[4])
        
        rawbboxes = list(allInfo[5:])
        bboxes = toNestedList(rawbboxes)
        txtFile = os.path.splitext(imageName)[0] + '.txt'

        with open(os.path.join(outputDir,txtFile),'w') as txt:
            for bbox in bboxes:
                x,y,h,w,id = map(int,bbox)
                cX,cY,nW,nH = NormalizeBbox(x,y,w,h,imageWidth,imageHeight)
                txt.write(f"{int(id)} {cX:.6f} {cY:.6f} {nW:.6f} {nH:.6f}\n")

        print(f"Done {txtFile}")