# -*- coding: utf-8 -*-

from class_DAG import one_entry_DAG
from class_Q_learning import Q_learning


def calc_gene_makespan(dag, comm_correspondence, gene_list, inout_ratio):
    one_entry_dag = one_entry_DAG(dag.file_name)  # one_entry_DAG に変換

    # 対応表に基づいて通信時間を再計算
    for i in range(len(gene_list)):
        if(gene_list[i] == 1):  # 1はクラスタ外の通信を示す
            sep = "_"
            temp = comm_correspondence[i].split(sep)
            ns = int(temp[0])  # エッジを入力するノード
            ne = int(temp[1])  # エッジが入力されるノード
            one_entry_dag.edge[ns][ne] = one_entry_dag.edge[ns][ne] * inout_ratio  # クラスタ外の通信時間とする
    
    # ranku を再計算
    one_entry_dag.ranku = [0] * one_entry_dag.num_of_node  # 初期化
    one_entry_dag.ranku_calc(one_entry_dag.ve_index)
    
    q_learning = Q_learning(1.0, 0.8, one_entry_dag)
    q_learning.learning()
    
    scheduling_list = []
    
    current_state = one_entry_dag.ve_index  # 初期状態は仮想entryノード
    finish_nodes = [one_entry_dag.ve_index]  # 仮想entryノードは選択済み
    wait_nodes = []
    wait_nodes += q_learning.check_succ(current_state, finish_nodes, wait_nodes)
    
    for k in range(one_entry_dag.num_of_node - 1):
        
        max_q_value = 0  # 現在の状態における行動価値の最大値を格納
        max_value_action = 0  # 行動価値が最大のノード

        for wait_n in wait_nodes:
            if(q_learning.q_sa[current_state][wait_n] >= max_q_value):
                max_q_value = q_learning.q_sa[current_state][wait_n]  # 行動価値の最大値を更新
                max_value_action = wait_n

        selected_node = max_value_action  # 行動価値が最大の行動を選択
        wait_nodes.remove(selected_node)
        finish_nodes.append(selected_node)
        current_state = selected_node
        wait_nodes += q_learning.check_succ(current_state, finish_nodes, wait_nodes)
    
    scheduling_list = finish_nodes
    scheduling_list.remove(one_entry_dag.ve_index)  # 仮想entryノードを削除
    
    return scheduling_list