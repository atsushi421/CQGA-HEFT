# -*- coding: utf-8 -*-
import copy


class Scheduler:
    # ＜コンストラクタ＞
    def __init__(self, scheduling_list, dag, target):
        '''
        scheduling_list : スケジューリングリスト
        dag : 割り当てるDAG
        target : ノードを割り当てるターゲットプロセッサ
        result_core[i][j] : クラスタiのコアjの割り当て結果. [ノード番号 , 処理開始時間, 処理終了時間]
        result_node[i] : niの割り当て結果. [割り当てられたクラスタ番号, 割り当てられたコア番号 , 処理開始時間, 処理終了時間]
        finish_nodes[] : 処理が終わったノード
        '''

        self.scheduling_list = copy.deepcopy(scheduling_list)
        self.dag = dag
        self.target = target
        self.result_core = [[[] for j in range(self.target.num_of_core)] for i in range(self.target.num_of_cluster)]
        self.result_node = [[] for i in range(self.dag.num_of_node)]
        self.finish_nodes = []
        
        self.schedule()
    
    
    # ＜メソッド＞
    # スケジューリングリストをもとに割り当て
    def schedule(self):
        
        
        while(len(self.finish_nodes) != self.dag.num_of_node):  #すべてのタスクの実行が終了したら、ループ終了

            # 処理を待つ場合
            if(len(self.scheduling_list) == 0):  # スケジューリングリストが空
                self.advance_time()
                continue
                
            if(self.legal(self.scheduling_list[0]) == False):  # スケジューリングリストの先頭がlegalでない
                self.advance_time()
                continue
            
            
            head = self.scheduling_list[0]  # スケジューリングリストの先頭
            
            earliest_CC = -1  # ESTが最小となるクラスタ番号
            earliest_core = -1  #ESTが最小となるコア番号
            min_EST = 99999999  # ESTの最小値
                
            for i in range(self.target.num_of_cluster):
                temp_EST = 0  # クラスタ毎のEST
                max_FT_plus_C = 0  # 前任ノードをすべて見た時の FT+C の最大値
                AT = 0  # 見ているクラスタのAT
                    
                # ATを求める
                idle_flag = self.target.cluster[i].idle_core()
                if(idle_flag != -1):  # クラスタiに空きがある
                    temp_earliest_core = idle_flag
                    AT = 0
                else:  # クラスタiに空きがない
                    AT, temp_earliest_core = self.AT(i)
                    
                # max(FT + C)を求める
                for pred_n in self.dag.pred[head]:
                    if(self.dag.entry[head] == 1):  # headがentryノードであれば
                        temp_FT_plus_C = 0
                    else:
                        temp_FT_plus_C = self.FT(pred_n) + self.comm_cost(pred_n, head , i)
                        
                    if(temp_FT_plus_C > max_FT_plus_C):
                        max_FT_plus_C = temp_FT_plus_C
                    
                # temp_EST を求める
                temp_EST = max(max_FT_plus_C, AT)
                    
                # ESTの更新
                if(temp_EST < min_EST):
                    min_EST = temp_EST
                    earliest_CC = i
                    earliest_core = temp_earliest_core
            
            if(self.target.current_time < min_EST):  # headのESTの時刻になっていない
                self.advance_time()
                continue
            
            # headの割り当て
            self.scheduling_list.pop(0)  # スケジューリングリストの先頭を削除
            self.allocate(head, earliest_CC, earliest_core)

    
    # nをクラスタi,コアjに割り当てる
    def allocate(self, n, i, j):
        self.target.cluster[i].core[j].idle = False
        self.target.cluster[i].core[j].processing_node = n
        self.target.cluster[i].core[j].remain_process = self.dag.node[n]
        
        # resultの書き込み
        self.result_core[i][j].append([n, self.target.current_time, (self.target.current_time + self.dag.node[n])])
        self.result_node[n] = [i, j, self.target.current_time, (self.target.current_time + self.dag.node[n])]
    
    
    # 時刻を1進め, 終了判定
    def advance_time(self):
        self.target.current_time+=1

        #終了判定
        processing_node = self.target.processing_nodes()
        for n in processing_node:
            if(self.result_node[n][3] == self.target.current_time):
                self.finish_nodes.append(n)
        
        self.target.advance_process()
    
    
    # pred_n の処理終了時間を返す
    def FT(self, pred_n):
        return self.result_node[pred_n][3]
        
        
    # pred_n~n の通信時間を返す
    def comm_cost(self, pred_n, n ,i):
        pred_CC = self.result_node[pred_n][0]  # 前任ノードが割り当てられたクラスタ
        
        if(pred_CC == i):  # 割り当てるクラスタが同じ

            return self.dag.edge[pred_n][n]
        else:  # 割り当てるクラスタが異なる
            return self.dag.edge[pred_n][n] * self.target.inout_ratio
                
        
    # クラスタiがIdle状態になる時間とその時のコアを返す
    def AT(self, i):
        min_idle = 99999999  # 最も早くidle状態となる時間
        earliest_core = -1
        
        for j in range(self.target.num_of_core):
            idle_time = self.result_core[i][j][-1][2]
            if(idle_time < min_idle):
                min_idle = idle_time
                earliest_core = j
        
        return min_idle, earliest_core
    
    
    # 受け取ったノードがlegalであればTrue, そうでなければFalse
    def legal(self, n):
        for pred_n in self.dag.pred[n]:
            if(pred_n not in self.finish_nodes):
                return False
        
        return True
    
    
    # result_core を表示
    def print_result_core(self):
        for i in range(self.target.num_of_cluster):
            for j in range(self.target.num_of_core):
                print("P(" + str(i) + ", " + str(j) + ") : ", end = "")
                print(self.result_core[i][j])
    
    
    # result_node を表示
    def print_result_node(self):
        for i in range(self.dag.num_of_node):
            print("node " + str(i) + " : ", end = "")
            print("{P(" + str(self.result_node[i][0]) + ", " + str(self.result_node[i][1]) + "), ST = " + str(self.result_node[i][2]) + ", FT = " + str(self.result_node[i][3]) + "}")
    
    
    # makespan を取得
    def makespan(self):
        makespan = 0
        
        for i in range(self.dag.num_of_node):
            if(self.result_node[i][3] > makespan):
                makespan = self.result_node[i][3]
        
        return makespan