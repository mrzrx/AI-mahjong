#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 18:07:04 2018

@author: Joaming
"""
 #计算LIST中的总数
def countList(list):
    _a=0
    for i in list:
        _a=_a+i
    return _a


#转化为二维数组
def list2array(list):
    """麻将游戏规则中心
    具体如下表
    ============================================
    0    1     2   3    4    5    6    7    8
    ============================================
    一万 二万 三万 四万 五万 六万 七万 八万 九万
    ============================================
    9    10   11   12   13   14   15   16   17
    ============================================
    一条 二条 三条 四条 五条 六条 七条 八条 九条
    ============================================
    18    19   20   21   22   23   24   25   26
    ============================================
    一筒 二筒 三筒 四筒 五筒 六筒 七筒 八筒 九筒
    ============================================
    27    28   29   30   31   32   33   34   35
    ============================================
    东风 南风 西风 北风 红中 发财 白板 (花1 花2没有）
    ============================================
    [0,1-9]
    0表示总数，1-9分别用各自的个数表示
    [8,8,8,8,7,6,5,4,3,2,1,0,0,0]
    转化为
    [[14, 3, 1, 1, 1, 1, 1, 1, 1, 4], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    """
    _allPai=[]
    _w=[]
    _t=[]
    _s=[]
    _z=[]
    for k in range(0,9):
        _w.append(list.count(k))
        
    for k in range(9,18):
        _t.append(list.count(k))
        
    for k in range(18,27):
        _s.append(list.count(k))
    
    for k in range(27,36):
        _z.append(list.count(k))
    
    _w.insert(0,countList(_w))
    _t.insert(0,countList(_t))
    _s.insert(0,countList(_s))
    _z.insert(0,countList(_z))
    _allPai.append(_w)
    _allPai.append(_t)
    _allPai.append(_s)
    _allPai.append(_z)
    return _allPai
    
def smartAI(ls):
    #-1代表胡了
    decision=-1
    duizi=0
    lsa=list2array(ls)
    print(lsa)
    if lsa[3][0]>0:
        for i in range(1,len(lsa[3])):
            if lsa[3][i]==1:
                decision=26+i
                return ls.index(decision)
    for i in range(4):
        for j in range(1,10):
            if lsa[i][j]>2:
                lsa[i][0]-=lsa[i][j]
                lsa[i][j]=0        
            if duizi==0 and lsa[i][j]==2:
                lsa[i][0]-=lsa[i][j]
                lsa[i][j]=0
                duizi+=1
    for i in range(3):
        for j in range(1,8):
            if lsa[i][j]>0 and lsa[i][j+1]>0 and lsa[i][j+2]>0:
                 lsa[i][0]-=3
                 lsa[i][j]-=1   
                 lsa[i][j+1]-=1   
                 lsa[i][j+2]-=1 
    for i in range(3):
        for j in range(1,10):
            if lsa[i][j]==1:
                decision=i*9+j-1
                print(decision)
                return ls.index(decision)
    


    
    
                    
             
                
    
    
    
    
    
   