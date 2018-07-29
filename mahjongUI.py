# -*- coding: utf-8 -*-

def mahjongui(player,flag):
    if type(player)!=list:
        pl=[]
        pl.append(player)
        player=pl
    if flag==None:
        ss=""
    else:
        if len(player)>1:
            ss="玩家"+str(flag+1)+":"
        else:
            ss="玩家"+str(flag+1)+"打出:"
   
    for i in range(len(player)):
        if player[i]<9:
            ss+=str(player[i]+1)+"万"+" "
        elif player[i]>8 and player[i]<18:
            ss+=str(player[i]-8)+"条"+" "
        elif player[i]>17 and player[i]<27:
            ss+=str(player[i]-17)+"筒"+" "
        elif player[i]==27:
            ss+="东"+" "
        elif player[i]==28:
            ss+="南"+" "   
        elif player[i]==29:
            ss+="西"+" "   
        elif player[i]==30:
            ss+="北"+" "   
        elif player[i]==31:
            ss+="中"+" "   
        elif player[i]==32:
            ss+="发"+" "   
        elif player[i]==33:
            ss+="白"+" "        
    print(ss)