import cv2
import numpy as np
import os
from matplotlib import pyplot as plt

images_root = './original/'
new_images_root = './indexed/'

if not os.path.exists(new_images_root):
    os.makedirs(new_images_root)

leftMargin = 0
rightMargin = -90
topMargin = 115
bottomMargin = -105

files = os.listdir(images_root)

xRange = []
yRange = []
tRange = []
for fileName in files:
	if(fileName=='.DS_Store'):
		continue
	if(fileName=='count'):
		continue
	fileName = '.'.join(fileName.split('.')[:-1])
	y_val = fileName.split(',')[0]
	yRange.append(float(y_val))
	x_val = fileName.split(',')[1]
	xRange.append(float(x_val))
	t_val = fileName.split(',')[2]
	tRange.append(float(t_val))

xRange = list(set(xRange))
yRange = list(set(yRange))
yRange.sort()
yDict = dict(zip(yRange, range(len(yRange))))
tRange = list(set(tRange))

gridSize = len(xRange), len(yRange)

for fileName in files:
	if(fileName=='.DS_Store'):
		continue
	if(fileName=='count'):
		continue

	img = cv2.imread(images_root + fileName)
	if(img==None):
		continue
	
	img = img[topMargin:bottomMargin,leftMargin:rightMargin]
	rows, columns, depth = img.shape
	newRows = int(round(rows*0.5))
	newColumns = int(round(columns*0.5))
	newSize = newColumns, newRows
	img = cv2.resize(img, newSize)

	fileName = '.'.join(fileName.split('.')[:-1])
	ijkList = fileName.split(',')

	i = yDict[float(ijkList[0])]
	j = int(ijkList[1])
	k = int(ijkList[2])

	idx = (gridSize[0]*i) + j

	if(k==0):
		print(idx)
		print(fileName)
		print(str(i)+', '+str(j))
		img1 = img[:,-600:]
		name1 = str(2*idx)+'.jpg'
		cv2.imwrite(new_images_root + name1, img1)
		
		img2 = img[:,:600]
		name2 = str((2*idx)+1)+'.jpg'
		cv2.imwrite(new_images_root + name2, img2)
