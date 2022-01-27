import numpy as np
import optproblems
import optproblems.cec2005
import xlwt

global StopCriteriaFit, OptimumFit,nPopulation,Cross_Prob,Mut_Prob,bounds,Fitness

def DE(fobj, bounds, mut=0.8, crossp=0.7, popsize=20, its=1000):
    best_par = []
    success = 0 
    dimensions = len(bounds)
    pop = np.random.rand(popsize, dimensions)
    min_b, max_b = np.asarray(bounds).T
    diff = np.fabs(min_b - max_b)
    pop_denorm = min_b + pop * diff
    fitness = np.asarray([fobj(ind) for ind in pop_denorm])
    its -= 1
    best_idx = np.argmin(fitness)
    best = pop_denorm[best_idx]
    fim = False
    i = 1
    while (not fim):
        for j in range(popsize):
            idxs = [idx for idx in range(popsize) if idx != j]
            a, b, c = pop[np.random.choice(idxs, 3, replace = False)]
            mutant = np.clip(a + mut * (b - c), 0, 1)
            cross_points = np.random.rand(dimensions) < crossp
            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True
            trial = np.where(cross_points, mutant, pop[j])
            trial_denorm = min_b + trial * diff
            f = fobj(trial_denorm)
            its -= 1
            if f < fitness[j]:
                fitness[j] = f
                pop[j] = trial
                if f < fitness[best_idx]:
                    best_idx = j
                    best = trial_denorm
            
            erro = fitness[best_idx] - OptimumFit  
            
            if i % 10 == 0:
                print(i,erro)
                best_par.append(erro)                    
            i += 1
            #Critério de Parada        
            if erro < StopCriteriaError:
                success = 1
                fim = True
            if its <= 0:
                fim = True
    # print final results
    print("Best: ", min(fitness),best)
    best_in = min(fitness) - OptimumFit
    worst_in = max(fitness) - OptimumFit
    mean_in = np.mean(fitness) - OptimumFit
    median_in = np.median(fitness) - OptimumFit
    print(success)
    return best_in, worst_in, mean_in, median_in, best_par, i, success
   
def Output_Excel(number_runs):
      success_rate = 0

      # Workbook is created 
      wb = xlwt.Workbook() 

      # add_sheet is used to create sheet. 
      sheet1 = wb.add_sheet('DE')

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
          
          BEST, WORST, MEAN, MEDIAN, BEST_PAR, NUM_RUNS, SUCCESS = DE(Fitness,bounds,Mut_Prob,Cross_Prob,nPopulation,StopCriteriaFit)
          
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
      wb.save('CEC2005 Function_4 - DE.xls')

Dimensions = 10 #Dimensão do problema
Fitness = optproblems.cec2005.F4(Dimensions) #COST FUNCTION
bounds=[(-100,100)]*Dimensions  # input bounds [(x1_min,x1_max),(x2_min,x2_max)...]
Mut_Prob = 0.8 #Fator de mutação
Cross_Prob = 0.9 #Probabilidade de crossover
nPopulation = 50 #tamanho da população

#Criterios de Parada
StopCriteriaFit = 10000*Dimensions #chamadas da função custo
StopCriteriaError = 10e-8 #proximidade com fitness minimo
OptimumFit = -450

#DE(Fitness,bounds,Mut_Prob,Cross_Prob,nPopulation,StopCriteriaFit)
Output_Excel(25)
