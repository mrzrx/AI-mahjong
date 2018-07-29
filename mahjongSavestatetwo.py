# -*- coding: utf-8 -*-
#转化为二维数组
#计算LIST中的总数
import numpy as np
import socket
import time

def countList(list):
    _a=0
    for i in list:
        _a=_a+i
    return _a
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


def savestatecreate(player,player1ming,player2ming,playersave):
    players=list2array(player)
    player1mings=list2array(player1ming)
    player2mings=list2array(player2ming)
    for i in range(0,4):
        for j in range(1,10):
            if 3*i+j-1>33:
                break
            if players[i][j] ==1:
                playersave[3*i+j-1][2]=1
            elif players[i][j] ==2:
                playersave[3*i+j-1][1]=1
            elif players[i][j] ==3:
                playersave[3*i+j-1][1]=1
                playersave[3*i+j-1][2]=1
            elif players[i][j] ==4:
                playersave[3*i+j-1][0]=1
    for i in range(0,4):
        for j in range(1,10):
            if 3*i+j-1>33:
                break
            if player1mings[i][j] ==1:
                playersave[3*i+j-1][5]=1
            elif player1mings[i][j] ==2:
                playersave[3*i+j-1][4]=1
            elif player1mings[i][j] ==3:
                playersave[3*i+j-1][4]=1
                playersave[3*i+j-1][5]=1
            elif player1mings[i][j] ==4:
                playersave[3*i+j-1][3]=1
    for i in range(0,4):
        for j in range(1,10):
            if 3*i+j-1>33:
                break
            if player2mings[i][j] ==1:
                playersave[3*i+j-1][8]=1
            elif player2mings[i][j] ==2:
                playersave[3*i+j-1][7]=1
            elif player2mings[i][j] ==3:
                playersave[3*i+j-1][7]=1
                playersave[3*i+j-1][8]=1
            elif player2mings[i][j] ==4:
                playersave[3*i+j-1][6]=1 
    return playersave
def savestateget(player,playersave):                
    players=list2array(player)
    for i in range(0,4):
        for j in range(1,10):
            if 3*i+j-1>33:
                break
            if players[i][j] ==1:
                playersave[3*i+j-1][2]=1
            elif players[i][j] ==2:
                playersave[3*i+j-1][1]=1
            elif players[i][j] ==3:
                playersave[3*i+j-1][1]=1
                playersave[3*i+j-1][2]=1
            elif players[i][j] ==4:
                playersave[3*i+j-1][0]=1
    return playersave
def savestatepostmaster(player,playersave,position,pv,filesave,playerstate,gamenum): 
    for i in range(20):
        playersave[i][34]=pv[i]
    playersave[20][34]=position
    playersave=np.array(playersave)
#    print(playersave)
    np.savetxt("gamenum"+str(gamenum)+"player"+str(playerstate[0])+"playnum"+str(playerstate[2])+str(socket.gethostname())+str(time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(time.time())))+".txt",playersave,fmt="%f")
    aa="gamenum"+str(gamenum)+"player"+str(playerstate[0])+"playnum"+str(playerstate[2])+str(socket.gethostname())+str(time.strftime("%Y-%m-%d-%H-%M-%S",time.localtime(time.time())))+".txt"
    filesave.append(aa)
    
    return [playersave,filesave]    

def savestatepost(playoutcard,playersave,num):  
    if num==0:
        if playersave[playoutcard][9]==0 and  playersave[playoutcard][10]==0 and playersave[playoutcard][11]==0:
            playersave[playoutcard][11]=1
        elif playersave[playoutcard][9]==0 and  playersave[playoutcard][10]==0 and playersave[playoutcard][11]==1:
            playersave[playoutcard][10]=1 
            playersave[playoutcard][11]==0
        elif playersave[playoutcard][9]==0 and  playersave[playoutcard][10]==1 and playersave[playoutcard][11]==0:
            playersave[playoutcard][11]==1
        elif playersave[playoutcard][9]==0 and  playersave[playoutcard][10]==1 and playersave[playoutcard][11]==1:
            playersave[playoutcard][9]=1 
            playersave[playoutcard][10]==0
            playersave[playoutcard][11]==0
    if num==1:
        if playersave[playoutcard][12]==0 and  playersave[playoutcard][13]==0 and playersave[playoutcard][14]==0:
            playersave[playoutcard][14]=1
        elif playersave[playoutcard][12]==0 and  playersave[playoutcard][13]==0 and playersave[playoutcard][14]==1:
            playersave[playoutcard][13]=1 
            playersave[playoutcard][14]==0
        elif playersave[playoutcard][12]==0 and  playersave[playoutcard][13]==1 and playersave[playoutcard][14]==0:
            playersave[playoutcard][14]==1
        elif playersave[playoutcard][12]==0 and  playersave[playoutcard][13]==1 and playersave[playoutcard][14]==1:
            playersave[playoutcard][12]=1 
            playersave[playoutcard][13]==0
            playersave[playoutcard][14]==0
    return playersave



     
        
