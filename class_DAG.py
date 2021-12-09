# -*- coding: utf-8 -*-


import pprint


# DAG
class DAG:
    # ＜コンストラクタ＞
    def __init__(self, file_tgff):
        '''
        file_name : .tgffファイルの名前
        num_of_node : DAG内のノード数
        node[i] : niの実行時間
        edge[i][j] : ni~nj間の通信時間
        pred[i] : niの前任ノードのリスト
        succ[i] : niの後続ノードのリスト
        entry[i]=1 : niはentryノード. entry[i]=0 : niはentryノードではない
        exit[i]=1 : niはexitノード. exit[i]=0 : niはexitノードではない
        ranku[i] : niのranku
        CCR : 通信時間と実行時間の比率
        '''
        
        self.file_name = file_tgff
        self.num_of_node, self.node, self.edge, self.pred, self.succ, self.entry, self.exit = self.read_file_tgff()
        self.ranku = [0] * self.num_of_node
        
        # rankuの計算
        for i in range(self.num_of_node):
            if(self.entry[i] == 1):
                self.ranku_calc(i)
        
        self.ccr_calc()
        


    # ＜メソッド＞
    # .tgffファイルの読み込み
    def read_file_tgff(self):
        path = "./DAG/" + self.file_name + ".tgff"  # DAG直下にあることを想定
        file_tgff = open(path, "r")
        
        type_cost = []  # TYPEと実行時間の対応関係の配列
        read_flag = 0  # PE5の情報だけを読み込むためのフラグ
        info_flag = 0   #余計な部分を読み込まないためのフラグ
        
        for line in file_tgff:
            if(line == "\n"):
                continue  # 空行はスキップ
            
            line_list = line.split()  # 文字列の半角スペース・タブ区切りで区切ったリストを取得
            # 読み込む範囲を限定
            if(len(line_list) >= 2):
                if(line_list[0] == '@PE' and line_list[1] == '5'):
                    read_flag = 1

                if(line_list[1] == 'type' and line_list[2] == 'exec_time'):
                    info_flag = 1
                    continue
                
                # TYPEの情報取得
                if(read_flag == 1 and info_flag == 1):
                    type_cost.append(int(float(line_list[1])))  #TYPEに対応する実行時間をint型で格納
                    
            elif(line_list[0] == '}'):
                read_flag = 0
                info_flag = 0
        
        file_tgff.close()
        
        # TASKの情報の取得
        node = []
        file_tgff = open(path, "r")
        for line in file_tgff:
            if(line == "\n"):
                continue  # 空行はスキップ
            
            line_list = line.split()  # 文字列の半角スペース・タブ区切りで区切ったリストを取得
            if(line_list[0] == 'TASK'):
                node.append(type_cost[int(line_list[3])]) #line_list[3]がTYPEなので、それに対応する実行時間を格納
            
        file_tgff.close()
        
        num_of_node = len(node)  # タスク数を取得
        
        # ARC情報の取得
        edge = [[0 for j in range(num_of_node)] for i in range(num_of_node)]
        file_tgff = open(path, "r")
        for line in file_tgff:
            if(line == "\n"):
                continue  # 空行はスキップ
            
            line_list = line.split()  # 文字列の半角スペース・タブ区切りで区切ったリストを取得
            if(line_list[0] == 'ARC'):
                from_t = int(line_list[3][3:])  # エッジを出すタスク
                to_t = int(line_list[5][3:])  # エッジの先のタスク
                comm_cost = int(type_cost[int(line_list[7])])  # TYPEに書かれている時間を通信時間とする
                edge[from_t][to_t] = comm_cost
        file_tgff.close()
        
        # predを求める
        pred = [[] for i in range(num_of_node)]
        for in_node in range(num_of_node):
            for out_node in range(num_of_node):
                if(edge[in_node][out_node] != 0):  # エッジがあれば
                    pred[out_node].append(in_node)
        
        # succを求める
        succ = [[] for i in range(num_of_node)]
        for in_node in range(num_of_node):
            for out_node in range(num_of_node):
                if(edge[in_node][out_node] != 0):  # エッジがあれば
                    succ[in_node].append(out_node)
                    
        # entryノードを求める
        entry = [0] * num_of_node
        for i in range(num_of_node):
            if(len(pred[i]) == 0):
                entry[i] = 1
                
        # exitノードを求める
        exit = [0] * num_of_node
        for i in range(num_of_node):
            if(len(succ[i]) == 0):
                exit[i] = 1
        
        return num_of_node, node, edge, pred, succ, entry, exit


    # rankuの計算
    def ranku_calc(self, n):
        if(self.exit[n] == 1):  # exitノードであれば
            self.ranku[n] = self.node[n]  # rankuは実行時間
        
        else:
            # 後続ノードのrankuを計算
            for succ_n in self.succ[n]:  # 後任ノードでループ
                if(self.ranku[succ_n] != 0):  # すでにランク値が計算されていればスキップ
                    continue
                
                self.ranku_calc(succ_n)
                
            # 後続ノードの中で「n～succ_nの通信時間＋succ_nのranku」が最大になるノードを見つけ、その最大値を保持
            max_value = 0
            
            for succ_n in self.succ[n]:
                tmp = self.edge[n][succ_n] + self.ranku[succ_n]
                if(tmp > max_value):
                    max_value = tmp
            
            self.ranku[n] = self.node[n] + max_value  # rankuを計算
    
    
    # CCRの計算
    def ccr_calc(self):
        sum_comm = 0
        
        for i in range(self.num_of_node):
            for j in range(self.num_of_node):
                if(self.edge[i][j] != 0):  # エッジがあれば
                    sum_comm += self.edge[i][j]
        
        ave_comm = sum_comm / self.num_edge()  # 平均通信時間
        
        sum_exec = 0
        for i in range(self.num_of_node):
            sum_exec += self.node[i]
        
        ave_exec = sum_exec / self.num_of_node
        
        self.CCR = ave_comm / ave_exec
        
    
    # CP の長さを返す
    def cp_len(self):
        return max(self.ranku)  # rankuの最大値がCPの長さ
        
    
    # エッジの数を返す
    def num_edge(self):
        num_edge = 0  # DAGのエッジの総数
        
        for i in range(self.num_of_node):
            for j in range(self.num_of_node):
                if(self.edge[i][j] != 0):  # エッジがあれば
                    num_edge += 1
        
        return num_edge


    # 変数の表示
    def print_num_of_node(self):
        print("num_of_node = ", end = "")
        print(self.num_of_node)
    
    def print_node(self):
        print("node = ", end = "")
        print(self.node)
        
    def print_edge(self):
        print("edge = ", end = "")
        pprint.pprint(self.edge, compact=True)
    
    def print_pred(self):
        print("pred = ", end = "")
        pprint.pprint(self.pred)
    
    def print_succ(self):
        print("succ = ", end = "")
        pprint.pprint(self.succ)
    
    def print_entry(self):
        print("entry = ", end = "")
        print(self.entry)
        
    def print_exit(self):
        print("exit = ", end = "")
        print(self.exit)
        
    def print_ranku(self):
        print("ranku = ", end = "")
        print(self.ranku)
    
    def print_all(self):
        self.print_num_of_node()
        self.print_node()
        self.print_edge()
        self.print_pred()
        self.print_succ()
        self.print_entry()
        self.print_exit()
        self.print_ranku()



# 仮想entryノードによって, entryノードが1つになったDAG
class one_entry_DAG(DAG):
    # ＜コンストラクタ＞
    def __init__(self, file_tgff):
        '''
        file_name : .tgffファイルの名前
        num_of_node : DAG内のノード数
        node[i] : niの実行時間
        edge[i][j] : ni~nj間の通信時間
        pred[i] : niの前任ノードのリスト
        succ[i] : niの後続ノードのリスト
        entry[i]=1 : niはentryノード. entry[i]=0 : niはentryノードではない
        exit[i]=1 : niはexitノード. exit[i]=0 : niはexitノードではない
        ranku[i] : niのranku
        ve_index : 仮想entryノードのノード番号
        '''
        
        super().__init__(file_tgff)
        self.ve_index = self.virtual_entry_index()
        
    
    # ＜メソッド＞
    # .tgffファイルの読み込み時に仮想entryノードを追加
    def read_file_tgff(self):
        path = "./DAG/" + self.file_name + ".tgff"  # DAG直下にあることを想定
        file_tgff = open(path, "r")
        
        type_cost = []  # TYPEと実行時間の対応関係の配列
        read_flag = 0  # PE5の情報だけを読み込むためのフラグ
        info_flag = 0   #余計な部分を読み込まないためのフラグ
        
        for line in file_tgff:
            if(line == "\n"):
                continue  # 空行はスキップ
            
            line_list = line.split()  # 文字列の半角スペース・タブ区切りで区切ったリストを取得
            # 読み込む範囲を限定
            if(len(line_list) >= 2):
                if(line_list[0] == '@PE' and line_list[1] == '5'):
                    read_flag = 1

                if(line_list[1] == 'type' and line_list[2] == 'exec_time'):
                    info_flag = 1
                    continue
                
                # TYPEの情報取得
                if(read_flag == 1 and info_flag == 1):
                    type_cost.append(int(float(line_list[1])))  #TYPEに対応する実行時間をint型で格納
                    
            elif(line_list[0] == '}'):
                read_flag = 0
                info_flag = 0
        
        file_tgff.close()
        
        # TASKの情報の取得
        node = []
        file_tgff = open(path, "r")
        for line in file_tgff:
            if(line == "\n"):
                continue  # 空行はスキップ
            
            line_list = line.split()  # 文字列の半角スペース・タブ区切りで区切ったリストを取得
            if(line_list[0] == 'TASK'):
                node.append(type_cost[int(line_list[3])]) #line_list[3]がTYPEなので、それに対応する実行時間を格納
            
        file_tgff.close()
        
        node.append(0)  # 末尾に実行時間0の仮想entryノードを追加
        num_of_node = len(node)  # タスク数を取得
        ve_index = num_of_node - 1  # veのノード番号
        
        # ARC情報の取得
        edge = [[-1 for j in range(num_of_node)] for i in range(num_of_node)]  # edge[i][j] = -1 : i～jはエッジがない
        file_tgff = open(path, "r")
        for line in file_tgff:
            if(line == "\n"):
                continue  # 空行はスキップ
            
            line_list = line.split()  # 文字列の半角スペース・タブ区切りで区切ったリストを取得
            if(line_list[0] == 'ARC'):
                from_t = int(line_list[3][3:])  # エッジを出すタスク
                to_t = int(line_list[5][3:])  # エッジの先のタスク
                comm_cost = int(type_cost[int(line_list[7])])  # TYPEに書かれている時間を通信時間とする
                edge[from_t][to_t] = comm_cost
        file_tgff.close()
        
        # predを求める
        pred = [[] for i in range(num_of_node)]
        for in_node in range(num_of_node):
            for out_node in range(num_of_node):
                if(edge[in_node][out_node] != -1):  # エッジがあれば
                    pred[out_node].append(in_node)
        
        # succを求める
        succ = [[] for i in range(num_of_node)]
        for in_node in range(num_of_node):
            for out_node in range(num_of_node):
                if(edge[in_node][out_node] != -1):  # エッジがあれば
                    succ[in_node].append(out_node)
                    
        # entryノードを求める
        entry = [0] * num_of_node
        for i in range(num_of_node):
            if(len(pred[i]) == 0):
                entry[i] = 1
                
        # exitノードを求める
        exit = [0] * num_of_node
        for i in range(num_of_node):
            if(len(succ[i]) == 0):
                exit[i] = 1
        
        # 仮想entryノードとエッジをつなぐ
        before_entrys = []  # 本来のentryノード
        
        for i in range(num_of_node):
            if(entry[i] == 1):
                before_entrys.append(i)
        
        before_entrys.remove(ve_index)  # veは削除
        
        for before_entry in before_entrys:
            edge[ve_index][before_entry] = 0  # ve～before_entry までの通信時間は0
            pred[before_entry].append(ve_index)  # before_entryの前任ノードにveを追加
            succ[ve_index].append(before_entry)  # veの後続ノードにbefore_entryを追加
            entry[before_entry] = 0  # before_entry をentryから削除
        
        exit[ve_index] = 0  # veをexitから削除
        
        return num_of_node, node, edge, pred, succ, entry, exit
    
    
    # veの添え字を返す
    def virtual_entry_index(self):
        return self.num_of_node - 1
    
    
    # エッジの数を返す
    def num_edge(self):
        num_edge = 0  # DAGのエッジの総数
        
        for i in range(self.num_of_node):
            for j in range(self.num_of_node):
                if(self.edge[i][j] != -1):  # エッジがあれば
                    num_edge += 1
        
        return num_edge