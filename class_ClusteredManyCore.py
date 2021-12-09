# -*- coding: utf-8 -*-


class Core:
    # ＜コンストラクタ＞
    def __init__(self):
        '''
        idle=True : このコアがアイドル状態
        processing_node : 処理中のノード番号
        remain_process : 残処理時間
        '''

        self.idle = True
        self.processing_node = -1
        self.remain_process = 0
    
    
    # ＜メソッド＞
    # 処理を1秒進める
    def advance_process(self, t):
        if(self.idle == False):
            self.remain_process-=1
            if(self.remain_process == 0):
                self.__init__()
    


class Cluster:
    # ＜コンストラクタ＞
    def __init__(self, num_of_core):
        '''
        num_of_core : 1クラスタ内のコア数
        self.core[] : クラスタ内にあるコア
        '''
        
        self.num_of_core = num_of_core
        # コアを用意
        self.core = []
        for i in range(self.num_of_core):
            self.core.append(Core())
    
    
    # ＜メソッド＞
    # 処理を1秒進める
    def advance_process(self, t):
        for i in range(self.num_of_core):
            self.core[i].advance_process(t)
    
    # クラスタに空きがあればそのコア番号, そうでなければ-1
    def idle_core(self):
        for i in range(self.num_of_core):
            if(self.core[i].idle == True):
                return i
        
        return -1
    
    # 現在処理中のノードを返す
    def processing_nodes(self):
        list = []
        
        for i in range(self.num_of_core):
            if(self.core[i].idle == False):
                list.append(self.core[i].processing_node)
        
        return list
    


class ClusteredManyCoreProcessor:
    # ＜コンストラクタ＞
    def __init__(self, num_of_cluster, num_of_core, inout_ratio):
        '''
        current_time : 現在時刻
        num_of_cluster : プロセッサ内のクラスタ数
        num_of_core : 1クラスタ内のコア数
        inout_ratio : クラスタ外の通信時間とクラスタ内の通信時間の比率
        cluster[] : このプロセッサ内にあるクラスタ
        '''

        self.current_time = 0
        self.num_of_cluster = num_of_cluster
        self.num_of_core = num_of_core
        self.inout_ratio = inout_ratio
        # プロセッサを形成
        self.cluster = []
        for i in range(self.num_of_cluster):
            self.cluster.append(Cluster(self.num_of_core))
    
    
    # ＜メソッド＞
    # 処理を1進める
    def advance_process(self):
        for i in range(self.num_of_cluster):
            self.cluster[i].advance_process(self.current_time)
            
    
    # 現在処理中のノードのリストを返す
    def processing_nodes(self):
        processing_nodes = []
        
        for i in range(self.num_of_cluster):
            list = self.cluster[i].processing_nodes()
            processing_nodes = processing_nodes + list
        
        return processing_nodes
    
    
    # プロセッサに空きがあればTrue, そうでなければFalse
    def empty_cluster(self):
        for i in range(self.num_of_cluster):
            if(self.cluster[i].idle_core() != -1):
                return True
        
        return False
            