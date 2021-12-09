# -*- coding: utf-8 -*-

import random
import time
from class_DAG import DAG
from class_DAG import one_entry_DAG
from class_ClusteredManyCore import ClusteredManyCoreProcessor
from class_Scheduler import Scheduler
from calc_gene_makespan import calc_gene_makespan


class Chromosome:
    # ＜コンストラクタ＞
    def __init__(self, CHROMOSOME_LENGTH):
        '''
        fitness : 評価値
        gene_list : 遺伝子情報
        makespan : メイクスパン
        result_core : プロセッサへの割り当て結果（評価用）
        result_node : プロセッサへの割り当て結果（評価用）
        match_ratio : 遺伝子情報と実際の割り当ての一致度
        '''
        
        self.fitness = -1
        self.gene_list = self.init_gene_list(CHROMOSOME_LENGTH)
        
    
    # ＜メソッド＞
    # 遺伝子情報をランダムにセット
    def init_gene_list(self, CHROMOSOME_LENGTH):
        gene_list = []
        for i in range(CHROMOSOME_LENGTH):
            gene_list.append(random.randint(0, 1))  # 0 or 1
            
        return gene_list



class GeneticAlgorithm():
    # ＜コンストラクタ＞
    def __init__(self, dag, target, num_of_population, mutation_ratio, max_population, result_path):
        '''
        DAG : 評価するDAG
        ONE_ENTRY_DAG : DAGに仮想エントリーノードを加えたもの
        TARGET : 割り当て対象のプロセッサ
        COMM_CORRESPONDENCE : GAの遺伝子と、DAGのエッジの対応表
        CHROMOSOME_LENGTH : 遺伝子の長さ＝DAG内のエッジの数
        NUM_OF_POPULATION : 1世代中の個体数
        MUTATION_RATIO : 突然変異確率
        MAX_POPULATION : 繰り返す世代数
        RESULT_PATH : 結果を書き込むパス
        population : 現在の世代
        START_TIME : 進化を開始した時間
        '''
        
        self.DAG = dag
        self.ONE_ENTRY_DAG = one_entry_DAG(self.DAG.file_name)
        self.TARGET = ClusteredManyCoreProcessor(target.num_of_cluster, target.num_of_core, target.inout_ratio)
        self.COMM_CORRESPONDENCE = self.generate_comm_list()
        self.CHROMOSOME_LENGTH = self.DAG.num_edge()
        self.NUM_OF_POPULATION = num_of_population
        self.MUTATION_RATIO = mutation_ratio
        self.MAX_POPULATION = max_population
        self.RESULT_PATH = result_path
        
        self.population = self.first_population()
        self.START_TIME = time.time()
        self.start_evo()
        
        
    # ＜メソッド＞
    # GAで用いるリストと、DAGの通信の対応表を生成
    def generate_comm_list(self):
        comm_list = []
        
        for i in range(self.DAG.num_of_node):
            for j in range(self.DAG.num_of_node):
                if (self.DAG.edge[i][j] != 0):  # エッジがあれば
                    comm_list.append(str(i) + "_" + str(j))  # i_j : Ti と Tj の通信
                    
        return comm_list
    
    
    # 第一世代を生成
    def first_population(self):
        population = []
        
        for i in range(self.NUM_OF_POPULATION):
            individual = Chromosome(self.CHROMOSOME_LENGTH)
            population.append(individual)
        
        return population
    
    
    # 進化開始
    def start_evo(self):
        for i in range(self.MAX_POPULATION):
            offspring = self.selected_by_elite()  # エリート選択
            
            # 交叉
            children = []
            for j in range(self.NUM_OF_POPULATION - len(offspring)):  # 不足分
                # エリートからランダムに2つの遺伝子を取り出し、1点交叉
                gene1 = random.choice(offspring)
                gene2 = random.choice(offspring)
                child1, child2 = self.single_point_crossover(gene1, gene2)
                children.append(child1)
                children.append(child2)  
            offspring.extend(children)
            
            self.mutate(offspring)  # 突然変異
            
            self.population = offspring  # 世代交代
            
            self.calc_fitness()  # 評価値計算
            
            # 結果の出力
            elapsed_time = time.time() - self.START_TIME
            best_chromosome = self.return_best_chromosome()

            f = open(self.RESULT_PATH, "a")
            f.write(str(elapsed_time) + "\t" + str(i) + "\t"+ str(best_chromosome.fitness) + "\t" + str(best_chromosome.match_ratio) + "\n")
            f.close()
    
    
    # 現在の世代の遺伝子をすべて評価
    def calc_fitness(self):
        for chromosome in self.population:
            target = ClusteredManyCoreProcessor(self.TARGET.num_of_cluster, self.TARGET.num_of_core, self.TARGET.inout_ratio)
            scheduling_list = calc_gene_makespan(self.DAG, self.COMM_CORRESPONDENCE, chromosome.gene_list, self.TARGET.inout_ratio)
            scheduler = Scheduler(scheduling_list, self.DAG, target)
            scheduler.schedule()
            chromosome.result_core = scheduler.result_core
            chromosome.result_node = scheduler.result_node
            chromosome.makespan = scheduler.makespan()
            self.calc_match_ratio(chromosome)
            chromosome.fitness = chromosome.makespan
            
            
    # エリート選択
    def selected_by_elite(self):
        elite = sorted(self.population, key=lambda x: x.fitness)
        return elite[:self.NUM_OF_POPULATION // 2]  # 1世代の遺伝子数//2分残す
    
    
    # 一点交叉
    def single_point_crossover(self, gene1, gene2):
        gene1_after_cross = Chromosome(self.CHROMOSOME_LENGTH)
        gene2_after_cross = Chromosome(self.CHROMOSOME_LENGTH)

        cross_point = random.randint(0, self.CHROMOSOME_LENGTH)  # 入れ替える点を設定

        gene1_after_cross.gene_list = gene1.gene_list[cross_point:] + gene2.gene_list[:cross_point]
        gene2_after_cross.gene_list = gene2.gene_list[cross_point:] + gene1.gene_list[:cross_point]

        return gene1_after_cross, gene2_after_cross
    
    
    # 突然変異
    def mutate(self, population):
        for i in range(1, len(population)):  # 最もエリート以外が対象
            for j in range(len(population[i].gene_list)):
                if(random.random() < self.MUTATION_RATIO):
                    population[i].gene_list[j] = abs(population[i].gene_list[j] - 1)  # 0<->1
                    
    
    # 最もメイクスパンが小さい染色体を返す
    def return_best_chromosome(self):
        gene_list_sorted = sorted(self.population, key=lambda x: x.fitness)
        
        return gene_list_sorted[0]
    
    
    # 現在の世代の fitness 平均を表示
    def print_population_ave(self):
        sum = 0
        for i in range(self.NUM_OF_POPULATION):
            sum += self.population[i].fitness
        
        ave = sum / self.NUM_OF_POPULATION
        
        print("平均値: {}" .format(ave))
    
    
    # 遺伝子情報と実際の割り当ての一致度計算
    def calc_match_ratio(self, chromosome):
        # 遺伝子情報によって、クラスタ外通信として計算したエッジを出力
        gene_list_out = []
        for i in range(self.CHROMOSOME_LENGTH):
            if(chromosome.gene_list[i] == 1):
                gene_list_out.append(self.COMM_CORRESPONDENCE[i])
        
        #print("遺伝子情報によって、クラスタ外通信として計算したエッジ: \n{}" .format(gene_list_out))
        
        
        # 割り当て後の、実際にクラスタ外通信が行われたエッジを出力
        allocate_out = []
        for n in range(self.DAG.num_of_node):
            for pred_n in self.DAG.pred[n]:
                if(chromosome.result_node[pred_n][0] != chromosome.result_node[n][0]):
                    allocate_out.append(str(pred_n) + "_" + str(n))
        
        #print("割り当て後の、実際にクラスタ外通信が行われたエッジ: \n{}" .format(allocate_out))
        
        
        # allocate_out をもとに、01のリストを作成（遺伝子情報と比較するため）
        allocate_list = [0] * self.CHROMOSOME_LENGTH
        
        for i in range(len(self.COMM_CORRESPONDENCE)):
            if(self.COMM_CORRESPONDENCE[i] in allocate_out):
                allocate_list[i] = 1
        
        match = 0
        for i in range(self.CHROMOSOME_LENGTH):
            if(chromosome.gene_list[i] == allocate_list[i]):
                match += 1
        
        match_ratio = match / self.CHROMOSOME_LENGTH * 100
        chromosome.match_ratio = match_ratio