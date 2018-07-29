# -*- coding: utf-8 -*-
import numpy as np
import random
from mahjongWIN import MahjongWin
import mahjongSavestatetwo as MS
import mahjongnnAI_eval
import os
from mahjongUI import mahjongui as MUI
import robot as R

def selfplay(gamenum):

    #奖励位
    rewords=[0,0]
    #初始化胡牌类
    MAHJONG=MahjongWin()
    for i in range(gamenum):
        #保存文件名
        filesave=[]
        #产生牌组
#        [[ 0  0  0  0]
#         [ 1  1  1  1]
#         [ 2  2  2  2]
#         [ 3  3  3  3]
#....
#         [30 30 30 30]
#         [31 31 31 31]
#         [32 32 32 32]
#         [33 33 33 33]]
        mahjongcards=np.array([[0 for i in range(4)]for j in range(34)])
        for i in range(34):
            for j in range(4):
                mahjongcards[i][j]=i    
        player1,player2,residualcards=Dealler(mahjongcards)
        player1=player1.tolist()
        player2=player2.tolist()
        player1=Bubble_sort(player1)
        player2=Bubble_sort(player2)
        players=[player1,player2]
        
        #玩家状态（玩家的桌号，出牌标识位,步数）
        playerstate=[[0,1,0],[1,0,0]]
       
        MUI(players[0],playerstate[0][0])
        MUI(players[1],playerstate[1][0])
        #明牌组
        player1ming=[]
        player2ming=[]
        playermings=[player1ming,player2ming]
        #神经网络输入结构态
        player1save=[[0 for col in range(35)] for row in range(34)]
        player2save=[[0 for col in range(35)] for row in range(34)]
        #保存手牌到各式中
        player1save=MS.savestatecreate(player1,player1ming,player2ming,player1save)
        player2save=MS.savestatecreate(player2,player2ming,player1ming,player2save)
        playersaves=[player1save,player2save]
        
        
        #游戏状态为1时运行，为0时游戏结束
        playing=1
        while(playing):
            #状态标识位chistate=pengstate=gangstate=hustate=passstate=0
            policyflag=[0,0,0,0,0]
            
            playerstate[0][2]+=1
            playerstate[1][2]=playerstate[0][2]
            if playerstate[0][1]==1:
                playflag=0
            else:
                playflag=1
            #摸牌阶段
            selectonecard,residualcards=Deallerone(residualcards,mahjongcards)
            print("玩家"+str(playflag+1)+"摸牌:")
            MUI(selectonecard,None)
            MUI(players[playflag],playflag)
            #更新手牌状态
            players[playflag].append(selectonecard)
            players[playflag]=Bubble_sort(players[playflag])
            playersaves[playflag]=MS.savestateget(players[playflag],playersaves[playflag])   
            #能否胡
            playerss=MAHJONG.list2array(players[playflag])
            if MAHJONG.zp_HU(playerss):
                policyflag[3]=1
            #能否杠
            minggang,angang=isgang(players[playflag],playermings[playflag],selectonecard)
            if minggang==1 or angang==1:
                policyflag[2]=1
                 
#            print("aaaa")
#            print(policyflag)
            #输入神经网络，执行策略 
            nninput=reshape34(playersaves[playflag])
            policy,value=mahjongnnAI_eval.NNAIeval(nninput)       
            policy=policy.tolist()
            policy=flatten(policy)
            value=value.tolist()
            value=flatten(value)
            pv=policy+value
            #将不用的策略为置0
           
                    
            for i in range(len(policyflag)):
                if policyflag[i]==0:
                    policy[14+i]=0
            for i in range(14-len(players[playflag])):
                policy[13-i]=0 
            print("s1层")    
            print(policy)
            decision=policy.index(max(policy))
            #加入机器人策略
            decision=R.smartAI(players[playflag])
            #半监督学习
            if policyflag[3]==1:
                decision=17
            elif policyflag[2]==1:
                decision=16
                
                
            #保存决策
            playersaves[playflag],filesave=MS.savestatepostmaster(players[playflag],playersaves[playflag],decision,pv,filesave,playerstate[playflag],gamenum)
            #出牌阶段
            if decision<14:
                
                #选择出牌
                print("决策者和决策")
                print([playflag,decision])
                playoutcard=players[playflag][decision]
                players[playflag].pop(players[playflag].index(playoutcard))
                MUI(playoutcard,playflag)
                #更新数据
                for i in range(2):
                    playflag=(playflag+i)%2
                    playersaves[playflag]=MS.savestatepost(playoutcard,playersaves[playflag],i)               
                #检验有人要此牌吗
                players,playermings,playersaves,playerstate,filesave,rewords,playing,residualcards=Wantcard(playoutcard,players,playermings,playersaves,playerstate,filesave,rewords,playing,residualcards,mahjongcards,gamenum)
            if decision ==16:
                #选择杠
                if minggang==1:
                    playermings[playflag].append(selectonecard)
                if angang==1:
                    for i in range(4):
                        players[playflag].pop(players[playflag].index(selectonecard))
                        playermings[playflag].append(selectonecard)
                print("玩家"+str(playflag+1)+"杠牌:")
                MUI(selectonecard,None)
                MUI(playermings[playflag],None)
                 #刷新数据
                for i in range(2):
                     playflag=(playflag+i)%2
                     playersaves[playflag]=MS.savestatecreate(players[playflag],playermings[playflag],playermings[playflag],playersaves[playflag])
                 
                        
            if decision ==17:
#                print("aa胡")
                #选择胡
                rewords[playflag]=2
                rewords[(playflag+1)%2]=-2
                print("大吉大利，玩家"+str(playflag+1)+"胡牌:")
                MUI(players[playflag],None)
                #产生数据
                for i in filesave:
                    plyersavedd=np.loadtxt(i)
                    ss1="gamenum"+str(gamenum)+"player"+str(playflag)
                    ss2="gamenum"+str(gamenum)+"player"+str((playflag+1)%2)
                    dession=int(plyersavedd[20][34])
                    if ss1 in i:
                        plyersavedd[dession][34]=rewords[playflag]
                        plyersavedd[19][34]=1
                    if ss2 in i:
                        plyersavedd[dession][34]=rewords[(playflag+1)%2]
                        plyersavedd[19][34]=-1
                playing=0
            #荒牌    
            if len(residualcards)==0:
                print("荒牌，这局白玩了")
                playing=0 
                #删掉所有文件
                for i in filesave:
                    file = os.getcwd()+"/"+i
                    if os.path.exists(file):
                        os.remove(file)
                    else:
                        print('no such file:%s' % file)
 

#可以要此牌
def Wantcard(playoutcard,players,playermings,playersaves,playerstate,filesave,rewords,playing,residualcards,mahjongcards,gamenum):
    if playerstate[0][1]==1:
                playflag=0
    else:
                playflag=1
    player1=players[(playflag+1)%2]
    player1ming=playermings[(playflag+1)%2]
    player1save=playersaves[(playflag+1)%2]
    #吃，碰，杠，胡
    flag=[0,0,0,0]
    if isWin(playoutcard,player1): 
        flag[3]==1
    if isgangone(playoutcard,player1,player1ming):
        flag[2]==1
    if isPeng(playoutcard,player1):
        flag[1]==1
    if isChi(playoutcard,player1):
        flag[0]==1
    print("bbbb")
    print(flag)    
    #输入神经网络给出决策
    if flag[0]==1 or flag[1]==1 or flag[2]==1 or flag[3]==1:
        #步骤加一
        playerstate[0][2]+=1
        playerstate[1][2]=playerstate[0][2]
        player1.append(playoutcard)
        
        player1save=MS.savestateget(player1,player1save) 

        #输入神经网络，执行策略 
        nninput=reshape34(player1save)
        policy,value=mahjongnnAI_eval.NNAIeval(nninput)       
        policy=policy.tolist()
        policy=flatten(policy)
        value=value.tolist()
        value=flatten(value)
        pv=policy+value
        #将不用的策略为置0
        #将吃位置0
        policy[14]=0
        print("s2层")    
        print(policy)
        decision=policy.index(max(policy))
        #加入机器人策略
        decision=R.smartAI(player1)
        
        #半监督学习
        if flag[3]==1:
            decision=17
        elif flag[2]==1:
            decision=16
        elif flag[1]==1:
            decision=16
        
        
        #保存决策
        playersaves[(playflag+1)%2],filesave=MS.savestatepostmaster(player1,player1save,decision,pv,filesave,playerstate[(playflag+1)%2],gamenum)
        #胡
        if decision ==17:
    #                print("aa胡")
            #选择胡
            playflag=(playflag+1)%2
            rewords[playflag]=2
            rewords[(playflag+1)%2]=-2
            print("大吉大利，玩家"+str(playflag+1)+"胡牌:")
            MUI(players[playflag],None)
            #产生数据
            for i in filesave:
                plyersavedd=np.loadtxt(i)
                ss1="gamenum"+str(gamenum)+"player"+str(playflag)
                ss2="gamenum"+str(gamenum)+"player"+str((playflag+1)%2)
                dession=plyersavedd[20][34]
                if ss1 in i:
                    plyersavedd[dession][34]=rewords[playflag]
                    plyersavedd[19][34]=1
                if ss2 in i:
                    plyersavedd[dession][34]=rewords[(playflag+1)%2]
                    plyersavedd[19][34]=-1
            playing=0   
#        #吃
#        if decision ==14:   
        #碰
        if decision ==15:
           playflag=(playflag+1)%2
           playermings[playflag].append(playoutcard) 
           playermings[playflag].append(playoutcard) 
           playermings[playflag].append(playoutcard)
           for i in range(len(players[playflag])):
               if players[playflag][i]==playoutcard:
                   players[playflag].pop(playoutcard)
                   players[playflag].pop(playoutcard)  
           
           print("玩家"+str(playflag)+"碰牌:")
           MUI(playoutcard,None)
           MUI(playermings[playflag],None)
           #刷新数据
           for i in range(2):
                 playersaves[playflag]=MS.savestatecreate(players[playflag],playermings[playflag],playermings[playflag],playersaves[playflag])
            #出牌
          #输入神经网络，执行策略 
           nninput=reshape34(playersaves[playflag])
           policy,value=mahjongnnAI_eval.NNAIeval(nninput)       
           policy=policy.tolist()
           policy=flatten(policy)
           value=value.tolist()
           value=flatten(value)
           pv=policy+value
           
           for i in range(20-len(players[playflag])):
               policy[20-i-1]=0
           
           print("bbb1")    
           print(policy) 
           decision=policy.index(max(policy))
           #加入机器人策略
           decision=R.smartAI(players[playflag])
            #保存决策
           playersaves[playflag],filesave=MS.savestatepostmaster(players[playflag],playersaves[playflag],decision,pv,filesave,playerstate[playflag],gamenum)
           #选择出牌
           playoutcard=players[playflag][decision]
           players[playflag].pop(decision)
           MUI(playoutcard,playflag)
            #更新数据
           for i in range(2):
                playersaves[playflag]=MS.savestatepost(playoutcard,playersaves[playflag],i)    
           #检验有人要此牌吗   
           players,playermings,playersaves,playerstate,filesave,rewords,playing,residualcards=Wantcard(playoutcard,players,playermings,playersaves,playerstate,filesave,rewords,playing,residualcards,mahjongcards,gamenum)

           
        #杠
        if decision ==16:
            playflag=(playflag+1)%2
            minggang,angang=isgang(players[playflag],playermings[playflag],playoutcard)
           #选择杠
            if minggang==1:
                playermings[playflag].append(playoutcard)
            if angang==1:
                players[playflag].append(playoutcard)
                for i in range(4):
                    players[playflag].pop(len(players[playflag])-1)
                    playermings[playflag].append(playoutcard)
            print("玩家"+str(playflag+2)+"杠牌:")
            MUI(playoutcard,None)
            MUI(playermings[playflag],None)
             #刷新数据
            for i in range(2):
                 playersaves[playflag]=MS.savestatecreate(players[playflag],playermings[playflag],playermings[playflag],playersaves[playflag],gamenum)
            
        
    else:
        playflag=(playflag+1)%2
        print("玩家"+str(playflag+1)+"不要此牌")
        playerstate[playflag][1]=1
        playerstate[(playflag+1)%2][1]=0
        
    return [players,playermings,playersaves,playerstate,filesave,rewords,playing,residualcards]
         
    

def isWin(playoutcard,player):
    
    player.append(playoutcard)
    MAHJONG=MahjongWin()
    player1s=MAHJONG.list2array(player)
    player.pop(len(player)-1)
    if MAHJONG.zp_HU(player1s):
        return True
    return False
def isgangone(playoutcard,player,playerming):
    num=0           
    if len(player)>=3:
        for i in player:
            if playoutcard==i:
                num+=1
    if len(playerming)>=3:
        for i in playerming:
            if playoutcard==i:
                num+=1
    if num==3:
        return True
    else:
        return False

def isPeng(playoutcard,player):
    for i in range(len(player)):
        if i>len(player)-2:
            break
        if player[i]==playoutcard and player[i+1]==playoutcard:
            return True
    return False    
    
def isChi(playoutcard,player):
    for i in range(len(player)):
        if i==len(player)-1:
            break
        if player[i]-1==playoutcard and player[i+1]-2==playoutcard:
            return True
        if player[i]+1==playoutcard and player[i+1]-1==playoutcard:
            return True
        if player[i]+2==playoutcard and player[i+1]+1==playoutcard:
            return True
    return False

               
                
def reshape34(xx):
    a=[[0 for i in range(34)]for j in range(34)]
    for i in range(34):
        for j in range(34):
            a[i][j]=xx[i][j]   
    return a                
                
def isgang(listt,listm,selectonecard):
    minggang=angang=0
    a=0
    if len(listt)>=4:
        for i in range(len(listt)-3):
            if a>len(listt)-4:
                break
            elif listt[a]==listt[a+1] and listt[a+1]==listt[a+2] and listt[a+2]==listt[a+3]:
                angang=1
                break
            else:
                a+=1
    num=0           
    if len(listm)>=3:
        for i in listm:
            if selectonecard==i:
                num+=1
    if num==3:
        minggang=1           
    return [minggang,angang]          
            
                
            
def Deallerone(residualcards,mahjongcards):
    #摸牌
    selectone=random.sample(residualcards,1)
    residualcards=list(set(residualcards).difference(set(selectone)))
    Cone=np.array(selectone)
    x=int(Cone/4)
    y=int(Cone%4)
    selectonecard=mahjongcards[x][y]
    return [selectonecard,residualcards]            
        
def Dealler(mahjongcards):
    #发牌
    listN=range(0,136)
    selectlist=random.sample(listN,26)
    residualcards=list(set(listN).difference(set(selectlist)))
    Clist=np.array(selectlist)
    player1=np.array([0 for i in range(13)])
    player2=np.array([0 for i in range(13)])
    for i in range(0,13):
        x=int(Clist[i]/4)
        y=Clist[i]%4 
        player1[i]=mahjongcards[x][y]
    a=0
    for i in range(13,26):  
        x=int(Clist[i]/4)
        y=int(Clist[i]%4) 
        player2[a]=mahjongcards[x][y]
        a+=1
    return [player1,player2,residualcards]
def Bubble_sort(lists):
    # 冒泡排序
    count = len(lists)
    for i in range(0, count):
        for j in range(i + 1, count):
            if lists[i] > lists[j]:
                lists[i], lists[j] = lists[j], lists[i]
    return lists       
def isSan(lists):
    flag=[]
    i=0
    while i<=len(lists)-3:
        if lists[i]==lists[i+1] and lists[i+1]==lists[i+2]:
            flag.append(i)
            i+=3
            continue
        i+=1
    return   flag      

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
            
    
def flatten(x):  
   result = []  
   for i in range(len(x)):
       for j in range(len(x[i])):
           result.append(x[i][j])
   return result 
   
   
def main(argv=None):
    gamenum=input("输入自对弈局数")
    gamenum=int(gamenum)
    selfplay(gamenum)
          
if __name__ == '__main__':
    main()             


