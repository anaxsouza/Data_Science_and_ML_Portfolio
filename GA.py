import numpy as np
import optproblems
import optproblems.cec2005
import xlwt

global OptimumFit,nIndividuos,bounds,nParentes,Prob_Rec,nRecombinacoes,Prob_Mut,nMutacoes,best_ref

def GA():
    Population = [0]*nIndividuos #Lista da população
    Cost = [0]*nIndividuos #Lista da custo população
    #Histórico    
    best_par = []
    Best_Mean_J = []
    Best_J = []
    J0 = 0
    success = 0      
    stopCriteria = StopCriteriaFit
    
    #Preenchendo população inicial
    for i in range(nIndividuos):
        Population[i] = np.random.uniform(-bounds,+bounds,Dimensions)
        Cost[i] = Fitness(Population[i])
        stopCriteria -= 1
    
    fim = False
    counter = 0
    while (not fim):
        counter += 1
        J0 = np.min(Cost)
    
        #seleção de pais
        pais_selecionados = False
        pp = []
        while not (pais_selecionados):
            for i in range(nParentes):
                prob_Pai_1 = np.random.randint(0,nIndividuos)
                prob_Pai_2 = np.random.randint(0,nIndividuos)
                if prob_Pai_1 != prob_Pai_2:
                    max_apt = min(Cost[prob_Pai_1], Cost[prob_Pai_2])
                    pp.append(Population[Cost.index(max_apt)])
                if len(pp) == nParentes: pais_selecionados=True; break
    
        #recombinação
        rec = []
        pp_copy = pp.copy()
        for r in range(nRecombinacoes):           
            if np.random.rand(1) < Prob_Rec:
                Pick_Pai_1 = np.random.randint(0,nParentes)
                Pick_Pai_2 = np.random.randint(0,nParentes)
                Pai_1 = pp_copy[Pick_Pai_1]
                Pai_2 = pp_copy[Pick_Pai_2]
                randomPosition = np.random.randint(0,Dimensions)
                Part_Pai_1 = [] 
                Part_Pai_2 = []
                for i in range(randomPosition,Dimensions):
                    Part_Pai_1.append(Pai_1[i])
                    Part_Pai_2.append(Pai_2[i])
                Rec_1 = list(Pai_1)
                Rec_2 = list(Pai_2)
                for i in range(randomPosition,Dimensions):
                    Rec_1[i] = Part_Pai_2[i-randomPosition]
                    Rec_2[i] = Part_Pai_1[i-randomPosition]
                rec.append(Rec_1)
                rec.append(Rec_2)
        for i in range(len(rec)):
            Population.append(np.array(rec[i]))
            Cost.append(Fitness(rec[i]))
            stopCriteria -= 1
    
        #mutação
        mut = []
        for i in range(nMutacoes):
            if np.random.rand(1) < Prob_Mut:
                randomPosition = np.random.randint(0,len(Population))
                Selecionado = Population[randomPosition]
                randomPosition_1 = np.random.randint(0,Dimensions)
                randomPosition_2 = np.random.randint(0,Dimensions)
                aux_1 = Selecionado[randomPosition_1]
                aux_2 = Selecionado[randomPosition_2]
                Selecionado[randomPosition_1] = aux_2
                Selecionado[randomPosition_2] = aux_1
                mut.append(Selecionado)
        for i in range(len(mut)):
            Population.append(np.array(mut[i]))
            Cost.append(Fitness(mut[i]))
            stopCriteria -= 1        
    
        #Historico médio
        Best_Mean_J.append(np.mean(Cost))
        if np.min(Cost) > J0:
            Best_J.append(J0)
        else:
            Best_J.append(np.min(Cost))
    
        #ordenando as listas por J   
        OrderedList = sorted(dict(zip(Cost,Population)).items(), key = lambda kv:(kv[0]))
        #seleção de melhores
        Next_gen = [0]*nIndividuos
        Next_genFit = [0]*nIndividuos
        for i in range(nIndividuos):
            Next_gen[i] = OrderedList[i][1]
            Next_genFit[i] = OrderedList[i][0]
        Population = Next_gen
        Cost = Next_genFit
    
        erro = min(Best_J) - OptimumFit
        print(counter,erro)
        if counter % 10 == 0:
            best_par.append(erro)
        
        #Critério de Parada        
        if erro < StopCriteriaError:
            success = 1
            fim = True
        if stopCriteria <= 0:
            fim = True
            
    # print final results
    print("Best: ", min(Best_J), Population[Cost.index(min(Best_J))])
    best_in = min(Best_J) - OptimumFit
    worst_in = max(Best_J) - OptimumFit
    mean_in = np.mean(Best_J) - OptimumFit
    median_in = np.median(Best_J) - OptimumFit
    print(success)
    return best_in, worst_in, mean_in, median_in, best_par, counter, success
    print(min(Best_J),Population[0])

def Output_Excel(number_runs):
      success_rate = 0

      # Workbook is created 
      wb = xlwt.Workbook() 

      # add_sheet is used to create sheet. 
      sheet1 = wb.add_sheet('GA')

      sheet1.write(1, 1, "RUN nº")
      sheet1.write(2,  1, "Closed in run")
      sheet1.write(3,  1, "Best result")
      sheet1.write(4,  1, "Worst result")
      sheet1.write(5,  1, "Mean result")
      sheet1.write(6,  1, "Median result")
      sheet1.write(7, 1, "Success rate")
      sheet1.write(8,  1, "Parcials")

      for run in range(number_runs):
          print("Start of run ", run)
          
          BEST, WORST, MEAN, MEDIAN, BEST_PAR, NUM_RUNS, SUCCESS = GA()
          
          sheet1.write(1, run+2, (run+1))
          sheet1.write(2, run+2, (NUM_RUNS))
          sheet1.write(3, run+2, (BEST))
          sheet1.write(4, run+2, (WORST))
          sheet1.write(5, run+2, (MEAN))
          sheet1.write(6, run+2, (MEDIAN))
          
          success_rate += SUCCESS
                              
          for index in range(len(BEST_PAR)):              
              sheet1.write(9+index,  run+2, (BEST_PAR[index]))
                        
      sheet1.write(7, 2, (success_rate))                  
      wb.save('CEC2005 Function_3 - GA.xls')

Dimensions = 10 #Dimensão do problema
nIndividuos = 1000 #Número de indivíduos
bounds = 100 #espaço de busca

nParentes = int(nIndividuos/2) #Número de pais
Prob_Rec = 0.8 #Chance de recombinção
nRecombinacoes = int(nIndividuos/2) #Número de recombinações
Prob_Mut = 0.1 #chance de mutação
nMutacoes = int(nIndividuos/2) #Número de mutações

#Criterios de Parada
StopCriteriaFit = 10000*Dimensions #chamadas da função custo
StopCriteriaError = 10e-8 #proximidade com fitness minimo

#Função Custo
Fitness = optproblems.cec2005.F3(Dimensions) 
OptimumFit = -450

#GA()
Output_Excel(25)



