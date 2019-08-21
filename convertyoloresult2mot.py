# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 17:06:49 2019

@author: hkangae
"""


import os
import json
import cv2
import numpy as np

#txtfile='P:\\Downloads\\motprocessing\\testresult\\result.json'
#f=open(txtfile,'r')
#imglist=f.readlines()
#f.close()
#imgprevpath='P:/Downloads/motprocessing/MOT16/train'   #写之前的路径
#imgfolder=list()
#for imlist in imglist:
#    folder=imlist.split('/')[-3]
#    if folder not in imgfolder:
#        imgfolder.append(folder)
imgprevpath='P:\\Downloads\\motprocessing\\testimages\\a1'
imgprevpath1='P:\\Downloads\\motprocessing\\testimages'
savefilepath='P:\\Downloads\\motprocessing\\testresult\\resultjsondet.txt'
f1=open(savefilepath,'w')      
#all0='000000'
thresh=0.5
jsonname='P:\\Downloads\\motprocessing\\testresult\\result.json'
with open(jsonname,'r') as f:
    jsonstr=json.loads(f.read())
    for item in jsonstr:
#        frame_idx=item['frame_id']
        
        filename1=item['filename']
        filename=filename1.split('/')[-2]
        frame_idx=filename1.split('/')[-1]
        frame_idx=frame_idx.split('.')[0]
        imgpath=os.path.join(imgprevpath,str(frame_idx)+'.jpg')
        if filename=='a1':
            obj=item['objects']
            print(obj)
            for ob in obj:
                classid=ob['class_id']
                
                if str(classid)=='0':
                    print(classid)
#                    img=cv2.imread(imgpath)
                    size=np.shape(img)
                    wwhole=size[0]
                    hwhole=size[1]
                    xcenter=int(np.floor(ob['relative_coordinates']['center_x']*hwhole))
                    ycenter=int(np.floor(ob['relative_coordinates']['center_y']*wwhole))
                    width=int(np.floor(ob['relative_coordinates']['width']*hwhole))
                    height=int(np.floor(ob['relative_coordinates']['height']*wwhole))
                    confidence=ob['confidence']
                    xtl=int(np.floor(xcenter-width/2))
                    ytl=int(np.floor(ycenter-height/2))
                    string=str(frame_idx)+',-1,'+str(xtl)+','+str(ytl)+','+str(width)+','+str(height)+','+str(confidence)+',-1,-1,-1'+'\n'
                    f1.write(string)
#                    img=cv2.imread(imgpath)
                    text=str(confidence)
#                    cv2.rectangle(img,(xtl,ytl),(xtl+width,ytl+height),[255,0,0],5)#,8)#,0)
#                    font=cv2.FONT_HERSHEY_SIMPLEX
#                    cv2.putText(img,text,(xtl,ytl),font,2,[255,0,0],2,cv2.LINE_AA)
#                    save_file_path=os.path.join(imgprevpath1,'img1')
#                    cv2.imwrite(os.path.join(save_file_path,str(frame_idx)+'.jpg'),img)
                    
                    
            
#        imgid=item['image_id']
#        if imgid<previd:
#            count=count+1
#        previd=imgid
#        cate=item['category_id']
#        bbox=item['bbox']
#        score=item['score']
#        string1=imgfolder[count-1]+'/'+str(imgid)+','+str(bbox[0])+','+str(bbox[1])+','+str(bbox[2])+','+str(bbox[3])+','+str(score)+'\n'
#        f1.write(string1)
        
f1.close()
f.close()
        