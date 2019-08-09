# -*- coding: utf-8 -*-
"""
Created on Fri Aug  9 20:24:03 2019

@author: hkangae
"""
import os

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
        
detfolder=[imgprevpath+'/'+imgf+'/det' for imgf in imgfolder]

detfiles=[detf+'/det.txt' for detf in detfolder]

savedetpath='P:/Downloads/motprocessing/detmerge'
f1=open(savedetpath,'r')
for det in detfiles:
    f=open(det,'r')
    lines=f.readlines()
    content=[line.split(',') for line in lines]
    
    