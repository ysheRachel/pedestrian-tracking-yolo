# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 19:52:19 2019

@author: hkangae
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 23:07:50 2019

@author: Hua Kang
"""

import numpy as np
import matplotlib.pyplot as plt


def calIOU(bbox1,bbox2):
    S_rec2 = bbox2[2]*bbox2[3]
    S_rec1 = bbox1[2]*bbox1[3]
    sum_area=S_rec2+S_rec1
    top_line=max(bbox1[1],bbox2[1])
    bottom_line=min(bbox1[1]+bbox1[3],bbox2[1]+bbox2[3])
    left_line=max(bbox1[0],bbox2[0])
    right_line=min(bbox1[0]+bbox1[2],bbox2[0]+bbox2[2])
    if left_line>=right_line or top_line>=bottom_line:
        return 0
    else:
        intersect=(right_line-left_line)*(bottom_line-top_line)
        return (intersect/(sum_area-intersect))*1.0


#根据图中框的位置统计image中walkable的区域，其他的部分为障碍物
def walkable(framedict,imgW,imgH):
    stat=np.zeros((imgW,imgH))
    for i in framedict.keys():
        curframe=framedict[i]
        for obj in curframe:
            bbox=obj[2:6]
            bbox=[int(np.floor(float(b))) for b in bbox]
            stat[np.max([0,bbox[0]]):bbox[0]+bbox[2],np.max([0,bbox[1]]):bbox[1]+bbox[3]]+=1
             

filepath='P:\\Downloads\\motprocessing\\testresult\\a2.txt'
imgW=1920
imgH=1080
f=open(filepath,'r')
lines=f.readlines()
lines=[line.strip() for line in lines]
lines=[line.split(',') for line in lines]
#lines=[map(eval,line) for line in lines]
lines=np.asarray(lines)
tracks=np.unique(lines[:,1])
tracks=[int(tr) for tr in tracks]
trackdict=dict()
for i in tracks:
    trackdict[i]=[]
    for j in range(0,lines.shape[0]):
        if int(lines[j,1])==i:
            trackdict[i].append(lines[j,:])
framedict=dict()
for i in range(1,3001):
    framedict[i]=[]
    for j in range(0,lines.shape[0]):
        if int(lines[j,0])==i:
            framedict[i].append(lines[j,:])

nearthresh=3 #临近的几个frame里面找merge对象
lenthresh=10  #少于多少张的track视为较少的track

rmind=[]
for i in trackdict.keys():
    curtrack=trackdict[i]
    curtrack=np.array(curtrack)
    frames=curtrack[:,0]
    frames=[int(fr) for fr in frames]
    frames=np.sort(np.array(frames))
    #看track的长度
    lengthtrack=len(curtrack)
    if lengthtrack<=lenthresh:
        #检查是否在其出现的几帧中有另一个较长的帧和它重叠
        countoverlap=0
        trackoccur=[]
        for fr in frames:
            curframe=framedict[fr]
            for obj in curframe:
                trackoccur.append(int(obj[1]))
        stat=[trackoccur.count(i) for i in trackoccur]
        trackoccurunique=np.unique(np.array(trackoccur))
        trackoccurunique=[tr for tr in trackoccurunique if tr!=i]
        stat=[stat[trackoccur.index(tr)] for tr in trackoccurunique]
        selind=[i for i in range(len(stat)) if stat[i]>=0.8*lengthtrack]
        tracksel=np.array(trackoccurunique)[selind]
        flag=0
        for tr in tracksel:
            curt=trackdict[tr]
            curt=np.array(curt)
            if len(curt)>40:
                frameinter=np.intersect1d(frames,curt[:,0])
                frameinter=[int(fr) for fr in frameinter]
                overlap=0
                for frinter in frameinter:
                    fra=framedict[frinter]
                    bbox1=[obj[2:6] for obj in fra if int(obj[1])==i]
                    bbox1=[float(b) for b in bbox1[0]]
                    bbox2=[obj[2:6] for obj in fra if int(obj[1])==tr]
                    bbox2=[float(b) for b in bbox2[0]]
                    IOU=calIOU(bbox1,bbox2)
                    print('IOU:'+str(IOU))
                    if IOU>=0.4:
                        overlap=overlap+1
                print('overlap:'+str(overlap))
                print('lengthtrack:'+str(lengthtrack))
                if overlap>=0.6*lengthtrack:
                    flag=1  #意思是要删除这个track
                    print(str(i)+'delete')
                    break
        if flag==1:
#            del trackdict[i]
            rmind.append(i)
            for fr in frames:
                curframe=framedict[fr]
                curframe=[obj for obj in curframe if int(obj[1])!=i]
                framedict[fr]=curframe
                
                
    
            
for r in rmind:
    del trackdict[r]        
        

        
        
#interpolation
for i in trackdict.keys():
    curtrack=trackdict[i]
    curtrack=np.array(curtrack)
    #找每个track的frame是否连续
    frames=curtrack[:,0]
    frames=[int(fr) for fr in frames]
    frames=np.sort(np.array(frames))
    diffframes=np.diff(frames)
    ind=np.where(diffframes>1)
    if ind[0].size:   #如果非空
        for indd in ind[0]:
            indstart=frames[indd]
            indend=frames[indd+1]
            bbox1=curtrack[indd,2:6]
            bbox1=[float(b) for b in bbox1]
    #        prevbox=bbox1
            bbox2=curtrack[indd+1,2:6]
            bbox2=[float(b) for b in bbox2]
            for fr in range(indstart+1,indend):
                #检查相应的frame内的track，如果有IOU很大的框并且该框出现时间很短，则将其id改为当前id
                #如果没有这样的框，可能是被物体遮挡了
                #如果有这样的框，但是对应的track也很长，考虑是被人遮挡了，这时根据前后两帧的框在中间的帧上进行插值
                if fr not in framedict.keys():
#                    print(str(i)+',frnotin')
                    curxtl=bbox1[0]+(bbox2[0]-bbox1[0])/(indend-indstart)*(fr-indstart)
                    curytl=bbox1[1]+(bbox2[1]-bbox1[1])/(indend-indstart)*(fr-indstart)
                    curxbr=bbox1[2]+(bbox2[2]-bbox1[2])/(indend-indstart)*(fr-indstart)
                    curybr=bbox1[3]+(bbox2[3]-bbox1[3])/(indend-indstart)*(fr-indstart)
                    addline=np.array([str(fr),str(i),str(curxtl),str(curytl),str(curxbr),str(curybr)])
                    framedict[fr]=[];
                    framedict[fr].append(addline)
                    trackdict[i].append(addline)
                else:                       
                    curframe=framedict[fr]
                    count=-1
                    flag=0  #在该帧上还没有匹配的track
        #            isntiou=-1
                    for obj in curframe:
                        if flag==0:
                            count=count+1
                            bboxcur=obj[2:6]
                            bboxcur=[float(b) for b in bboxcur]
                            curxtl=bbox1[0]+(bbox2[0]-bbox1[0])/(indend-indstart)*(fr-indstart)
                            curytl=bbox1[1]+(bbox2[1]-bbox1[1])/(indend-indstart)*(fr-indstart)
                            curxbr=bbox1[2]+(bbox2[2]-bbox1[2])/(indend-indstart)*(fr-indstart)
                            curybr=bbox1[3]+(bbox2[3]-bbox1[3])/(indend-indstart)*(fr-indstart)
                            predbox=[curxtl,curytl,curxbr,curybr]
                            IOU1=calIOU(predbox,bboxcur)
        #                    prevbox=bboxcur                    
                            if IOU1>=0.75:
#                                print(i)
                                trackid=int(obj[1])
                                lentrack=len(trackdict[trackid])
                                #如果框在中间且lentrack>=10
                                if lentrack>=10:
                                    #此种情况考虑人是被他人遮挡
#                                    print(i)
                                    addline=np.array([str(fr),str(i),str(curxtl),str(curytl),str(curxbr),str(curybr)])
                                    framedict[fr].append(addline)
                                    trackdict[i].append(addline)
                                    flag=1
                                else:
                                    obj[1]=i
                                    framedict[fr][count][1]=i
                                    trackdict[i].append(obj)
                                    flag=1
                    if flag==0: #没在当前帧找到匹配的
#                        print(str(i)+',flag0')
                        curxtl=bbox1[0]+(bbox2[0]-bbox1[0])/(indend-indstart)*(fr-indstart)
                        curytl=bbox1[1]+(bbox2[1]-bbox1[1])/(indend-indstart)*(fr-indstart)
                        curxbr=bbox1[2]+(bbox2[2]-bbox1[2])/(indend-indstart)*(fr-indstart)
                        curybr=bbox1[3]+(bbox2[3]-bbox1[3])/(indend-indstart)*(fr-indstart)
                        addline=np.array([str(fr),str(i),str(curxtl),str(curytl),str(curxbr),str(curybr)])
                        framedict[fr].append(addline)
                        trackdict[i].append(addline)
                    

#write framedict to txt file
savefilepath='P:\\Downloads\\motprocessing\\testresult\\a2modifieddelete.txt'
f=open(savefilepath,'w')
for i in framedict.keys():
    curframe=framedict[i]
    for obj in curframe:
        string=obj[0]+','+obj[1]+','+obj[2]+','+obj[3]+','+obj[4]+','+obj[5]+'\n'
        f.write(string)
           
                        
                        
                

                
                
