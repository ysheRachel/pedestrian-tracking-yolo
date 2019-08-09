# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 23:02:08 2019

@author: Hua Kang
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
        
all0='000000'
thresh=0.5
jsonname='E:/motprocessing/txtfiles/results.json'
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
        if score>=thresh:
            if cate=='1':
                imgname=all0[1:6-len(str(imgid))]+str(imgid)
                imgpath=os.path.join(imgprevpath,imgfolder[count] +'/'+imgname+'.jpg')
                img=cv2.imread(imgpath)
                text=str(score)
                cv2.rectangule(img,(bbox[1],bbox[3]),(bbox[2],bbox[4]),[255,0,0],5,8,0)
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img,text,(bbox[1],bbox[3]),font,2,[255,0,0],2,cv2.LINE_AA)
                save_file_path=os.path.join(imgprevpath,imgfolder[count])
                cv2.imwrite(os.path.join(save_file_path,imgname+'.jpg'),img)
        
        