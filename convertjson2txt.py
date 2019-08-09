# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 18:36:39 2019

@author: hkangae
"""

import os
import json
#import cv2

txtfile='P:/Downloads/motprocessing/mot16train.txt'
f=open(txtfile,'r')
imglist=f.readlines()
f.close()
imgprevpath='P:/Downloads/motprocessing/MOT16/train'   #写之前的路径
imgfolder=list()
for imlist in imglist:
    folder=imlist.split('/')[-3]
    if folder not in imgfolder:
        imgfolder.append(folder)
        
        
savefilepath='P:/Downloads/motprocessing/resultjson.txt'
f1=open(savefilepath,'a')      
all0='000000'
thresh=0.5
jsonname='P:\Downloads\motprocessing/results.json'
with open(jsonname,'r') as f:
    jsonstr=json.loads(f.read())
    count=1
    previd=1
    for item in jsonstr:
        imgid=item['image_id']
        if imgid<previd:
            count=count+1
        previd=imgid
        cate=item['category_id']
        bbox=item['bbox']
        score=item['score']
        string1=imgfolder[count-1]+'/'+str(imgid)+','+str(bbox[0])+','+str(bbox[1])+','+str(bbox[2])+','+str(bbox[3])+','+str(score)+'\n'
        f1.write(string1)
        
f1.close()
f.close()
        