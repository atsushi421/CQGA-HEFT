# -*- coding: utf-8 -*-

import sys
from class_DAG import DAG
from class_ClusteredManyCore import ClusteredManyCoreProcessor
from class_CQGAHEFT import GeneticAlgorithm


class Evaluater:
    # <コンストラクタ>
    def __init__(self, args):
        '''
        EVA_NAME : 評価名
        TARGET : 対象のプロセッサ
        DAG : 対象のDAG
        LOG_PATH : ログファイルへのパス（実験パラメータを書いておく）
        RESULT_PATH : 結果を書き込むファイルへのパス
        '''
        self.EVA_NAME = args[1]
        self.DAG = DAG(args[2])
        self.TARGET = ClusteredManyCoreProcessor(int(args[3]), int(args[4]), float(args[5]))
        self.update_dag(float(args[6]), float(args[7]))
        self.RESULT_PATH = self.set_result_path(float(args[6]), float(args[7]))
        self.evaluate()
    
    
    # <メソッド>
    # -- 評価を行う --
    def evaluate(self):
        f = open(self.RESULT_PATH, "w")
        f.write("経過時間" + "\t" + "世代" + "\t" + "メイクスパン" + "\t" + "遺伝子情報と実際の割り当ての一致度" + "\n")
        f.close()
        
        GeneticAlgorithm(self.DAG, self.TARGET, 8, 0.01, 50, self.RESULT_PATH)
            
    
    # FACTORに基づいてDAGを更新
    def update_dag(self, factor_edge, factor_node):
        for i in range(self.DAG.num_of_node):
            for j in range(self.DAG.num_of_node):
                self.DAG.edge[i][j] = int(self.DAG.edge[i][j] * factor_edge)
        for i in range(self.DAG.num_of_node):
            self.DAG.node[i] = int(self.DAG.node[i] * factor_node)
        
        # rankuの再計算
        self.DAG.ranku = [0] * self.DAG.num_of_node  # 初期化
        for i in range(self.DAG.num_of_node):
            if(self.DAG.entry[i] == 1):
                self.DAG.ranku_calc(i)
        
        self.DAG.ccr_calc()  # CCRの再計算
    
    
    # 評価名に基づいて, result_path を決める
    def set_result_path(self, factor_edge, factor_node):
        if(self.EVA_NAME == "change_CCR"):
            if(factor_edge == 0.8 and factor_node == 2):
                return "./result/change_CCR/CCR_0.25/" + self.DAG.file_name + ".txt"
            if(factor_edge == 1 and factor_node == 1.3):
                return "./result/change_CCR/CCR_0.5/" + self.DAG.file_name + ".txt"
            if(factor_edge == 1.5 and factor_node == 1):
                return "./result/change_CCR/CCR_1.0/" + self.DAG.file_name + ".txt"
            if(factor_edge == 2 and factor_node == 0.7):
                return "./result/change_CCR/CCR_2.0/" + self.DAG.file_name + ".txt"
            if(factor_edge == 3 and factor_node == 0.5):
                return "./result/change_CCR/CCR_4.0/" + self.DAG.file_name + ".txt"
        
        if(self.EVA_NAME == "change_InoutRatio"):
            return "./result/change_InoutRatio/InoutRatio_" + str(self.TARGET.inout_ratio) + "/" + self.DAG.file_name + ".txt"
        
        if(self.EVA_NAME == "change_NumCore"):
            return "./result/change_NumCore/NumCore_" + str(self.TARGET.num_of_core) + "/" + self.DAG.file_name + ".txt"
        
        if(self.EVA_NAME == "change_NumNode"):
            if('20_' in self.DAG.file_name):
                return "./result/change_NumNode/NumNode_20" + "/" + self.DAG.file_name + ".txt"
            if('50_' in self.DAG.file_name):
                return "./result/change_NumNode/NumNode_50" + "/" + self.DAG.file_name + ".txt"
            if('100_' in self.DAG.file_name):
                return "./result/change_NumNode/NumNode_100" + "/" + self.DAG.file_name + ".txt"
            if('200_' in self.DAG.file_name):
                return "./result/change_NumNode/NumNode_200" + "/" + self.DAG.file_name + ".txt"



if __name__ == "__main__":
    args = sys.argv
    Evaluater(args)