# -*- coding: utf-8 -*-

class MahjongWin:
    def __init__(self):
        pass
    
    
    """判断是否胡牌"""
    def zp_HU(self,list):
        #满足2222222型
        _a=0
        for _p in list:
            for _y in _p:
                _m=_y%2
                if _m!=0:
                    _a=1 
        if _a==0:
            return True
        else:
            _kingPos=None
            _yuShu=None
            _kingExist=False
            _j=0
            #满足3,3,3,3,2模型
            for _p in list:
                _yuShu=_p[0]%3
                if _yuShu==1:
                    return False
                if _yuShu==2:
                    if(_kingExist):
                        return False
                    _kingPos=_j
                    _kingExist=True
                _j=_j+1
           
            #先计算没有将牌的LIST
            _j=0
            for _p in list:
                if _kingPos==_j:
                    pass
                else:
                    if not self.Analyze(_p,_j==3):
                        return False
                _j=_j+1
            #该列表中包含将牌，采用轮训迭代方式，效率较低
            #指示除掉将后能否通过
            _success=False
            _jlist=list[_kingPos]+[]
            
            _j=0
            for _card in _jlist:
                if _j==0:
                    pass
                else:
                    if _card==2:
                        _jlist[_j]-=2
                        _jlist[0]-=2
                        if self.Analyze(_jlist,_kingPos==3):
                            _success=True
                        _jlist[_j]+=2
                        _jlist[0]+=2
                        if _success:
                            break
                _j=_j+1
            return _success
    
    
    #分解为“刻” “顺”组合
    def Analyze(self,list,flag):
        if list[0]==0:
            return True
        
        #寻找第一张牌
        _j=0
        for _p in list:
            if _j==0:
                pass
            else:
                if _p!=0:
                    break
            _j=_j+1
        result=None
        if list[_j]>=3:
            list[_j]-=3
            list[0]-=3
            result=self.Analyze(list,flag)
            list[_j]+=3
            list[0]+=3
            return result
        
        #做为顺牌
        if not flag and _j<8 and list[_j+1]>0 and list[_j+2]>0:
            list[_j]=list[_j]-1
            list[_j+1]=list[_j+1]-1
            list[_j+2]=list[_j+2]-1
            list[0]=list[0]-3
            result=self.Analyze(list,flag)
            #还原这3张牌
            list[_j]=list[_j]+1
            list[_j+1]=list[_j+1]+1
            list[_j+2]=list[_j+2]+1
            list[0]=list[0]+3
            return result
        return False
        
    
    #计算LIST中的总数
    def countList(self,list):
        _a=0
        for i in list:
            _a=_a+i
        return _a
    
    
    #转化为二维数组
    def list2array(self,list):
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
        
        _w.insert(0,self.countList(_w))
        _t.insert(0,self.countList(_t))
        _s.insert(0,self.countList(_s))
        _z.insert(0,self.countList(_z))
        _allPai.append(_w)
        _allPai.append(_t)
        _allPai.append(_s)
        _allPai.append(_z)
        return _allPai
    
#def main(argv=None):
#    ls=[1,1]
#    ms=MahjongWin()
#    ss=ms.list2array(ls)
#    print ms.zp_HU(ss)
#          
#if __name__ == '__main__':
#    main()       

