# -*- coding: utf-8 -*-


import random
import math


# Q-learning
class Q_learning:
    # ＜コンストラクタ＞
    def __init__(self, alpha, gamma, dag):
        '''
        alpha : 学習率
        gamma : 割引率
        dag : 学習対象のDAG
        q_sa : Qテーブル
        reward[i] : niを行動として選択した時の即時報酬
        '''
        
        self.alpha = alpha
        self.gamma = gamma
        self.dag = dag
        self.q_sa = [[0 for j in range(self.dag.num_of_node)] for i in range(self.dag.num_of_node)]
        self.reward = []
        self.reward_calc()
        
    
    
    # ＜メソッド＞
    # 最適なQテーブルを得る
    def learning(self):
        convergence_flag = 0  # 1エピソード内でq_saが一度も更新されていない場合+1
        
        # エピソードループ
        while(True):
            '''
            current_state : 現在の状態
            finish_nodes : 選択済みのノード
            wait_nodes : 選択可能なノード
            selected_node : 行動で選択したノード
            before_state : 遷移前の状態
            r : 行動で得られた即時報酬
            max_value_action : 遷移後の状態から見た行動価値が最大の行動
            '''
            
            current_state = self.dag.ve_index  # 初期状態は仮想entryノード
            finish_nodes = [self.dag.ve_index]  # 仮想entryノードは選択済み
            wait_nodes = []
            wait_nodes += self.check_succ(current_state, finish_nodes, wait_nodes)
            
            no_update_flag = 0  # 1ステップでq_saの更新が0の時+1.
            
            # ステップループ
            for k in range(self.dag.num_of_node - 1):
                selected_node = random.choice(wait_nodes)  # ランダム方策でアクションを決定
                wait_nodes.remove(selected_node)
                finish_nodes.append(selected_node)
                before_state = current_state
                current_state = selected_node
                r = self.reward[selected_node]
                wait_nodes += self.check_succ(current_state, finish_nodes, wait_nodes)

                max_q_value = 0
                max_value_action = 0

                for n in range(self.dag.num_of_node):
                    if(self.q_sa[current_state][n] >= max_q_value):
                        max_q_value = self.q_sa[current_state][n]
                        max_value_action = n
                
                # q_saの更新
                before_q_sa = self.q_sa[before_state][selected_node]  # 更新前の値を保持
                self.q_sa[before_state][selected_node] = self.q_sa[before_state][selected_node] + self.alpha * (r + self.gamma * self.q_sa[current_state][max_value_action] - self.q_sa[before_state][selected_node])

                if(abs(self.q_sa[before_state][selected_node] - before_q_sa) <= 0.00000001):
                    no_update_flag+=1
            
            # エピソードループ終了判定
            if(no_update_flag == (self.dag.num_of_node - 1)):  # 1エピソード内でq_saの更新が無かった場合
                convergence_flag+=1
                if(convergence_flag == 300000):  # 100では300000ぐらい必要
                    break
                
    
    # 「nの後続ノード かつ legal かつ wait_nodesに入っていない」ノードのリストを返す
    def check_succ(self, n, finish_nodes, wait_nodes):
        list = []
        
        for succ_n in self.dag.succ[n]:
            if(self.legal(succ_n, finish_nodes) and succ_n not in wait_nodes):
                list.append(succ_n)
        
        return list
    
    
    # nがlegalであればTrue, そうでなければFalse
    def legal(self, n, finish_nodes):
        for pred_n in self.dag.pred[n]:
            if(pred_n not in finish_nodes):
                return False
        
        return True
    
    
    # 報酬を定義
    def reward_calc(self):
        for i in range(self.dag.num_of_node):
            self.reward.append(self.dag.ranku[i])
    
    
    # q_saを表示（整数に変換）
    def print_q_sa_int(self):
        q_sa_int = [[0 for j in range(self.dag.num_of_node)] for i in range(self.dag.num_of_node)]
        
        for i in range(self.dag.num_of_node):
            for j in range(self.dag.num_of_node):
                q_sa_int[i][j] = int(self.q_sa[i][j])
        
        print("q_sa_int = ", end = "")
        for i in range(self.dag.num_of_node):
            print(q_sa_int[i])