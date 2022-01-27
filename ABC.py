import numpy as np
import optproblems
import optproblems.cec2005
from random import randint, uniform
import xlwt

class sw(object):

    def __init__(self):

        self.__Positions = []
        self.__Gbest = []

    def _set_Gbest(self, Gbest):
        self.__Gbest = Gbest

    def _points(self, agents):
        self.__Positions.append([list(i) for i in agents])

    def get_agents(self):
        """Returns a history of all agents of the algorithm (return type:
        list)"""

        return self.__Positions

    def get_Gbest(self):
        """Return the best position of algorithm (return type: list)"""

        return list(self.__Gbest)
    

class aba(sw):
    """
    Artificial Bee Algorithm
    """

    def __init__(self, n, function, lb, ub, dimension, iteration):
        """
        :param n: number of agents
        :param function: test function
        :param lb: lower limits for plot axes
        :param ub: upper limits for plot axes
        :param dimension: space dimension
        :param iteration: number of iterations
        """

        super(aba, self).__init__()
        
        self.best_par = []
        self.best_all = []
        self.sucess_t = 0 

        self.__function = function
        self.__agents = np.random.uniform(lb, ub, (n, dimension))
        self._points(self.__agents)

        Pbest = self.__agents[np.array([function(x)
                                        for x in self.__agents]).argmin()]
        Gbest = Pbest
        globalBest = function(Pbest)

        if n <= 10:
            count = n - n // 2, 1, 1, 1
        else:
            a = n // 10
            b = 5
            c = (n - a * b - a) // 2
            d = 2
            count = a, b, c, d

        fim = False
        self.t = 0
        while (not fim):

            fitness = [function(x) for x in self.__agents]
            sort_fitness = [function(x) for x in self.__agents]
            sort_fitness.sort()

            best = [self.__agents[i] for i in
                    [fitness.index(x) for x in sort_fitness[:count[0]]]]
            selected = [self.__agents[i]
                        for i in [fitness.index(x)
                                  for x in sort_fitness[count[0]:count[2]]]]

            newbee = self.__new(best, count[1], lb, ub) + self.__new(selected,
                                                                   count[3],
                                                                   lb, ub)
            m = len(newbee)
            self.__agents = newbee + list(np.random.uniform(lb, ub, (n - m,
                                                                   dimension)))

            self.__agents = np.clip(self.__agents, lb, ub)
            self._points(self.__agents)

            Pbest = self.__agents[
                np.array([function(x) for x in self.__agents]).argmin()]
            if function(Pbest) < globalBest:
                Gbest = Pbest
                globalBest = function(Pbest)
            
            erro = globalBest - OptimumFit
            print(self.t,erro)
            self.best_all.append(erro)
            iteration -= 10
            self.t += 1
            if self.t % 10 == 0:
                self.best_par.append(erro)
            #Critério de Parada        
            if erro < StopCriteriaError:
                self.sucess_t = 1
                fim = True
            if iteration <= 0:
                fim = True
            
        # print final results
        self._set_Gbest(Gbest)
        print("Best: ",globalBest,Gbest)
        self.best_in = min(self.best_all)
        self.worst_in = max(self.best_all)
        self.mean_in = np.mean(self.best_all)
        self.median_in = np.median(self.best_all)
        print(self.sucess_t)

    def __new(self, l, c, lb, ub):

        bee = []
        for i in l:
            new = [self.__neighbor(i, lb, ub) for k in range(c)]
            bee += new
        bee += l

        return bee

    def __neighbor(self, who, lb, ub):

        neighbor = np.array(who) + uniform(-1, 1) * (
            np.array(who) - np.array(
                self.__agents[randint(0, len(self.__agents) - 1)]))
        neighbor = np.clip(neighbor, lb, ub)

        return list(neighbor)

def Output_Excel(number_runs):
      success_rate = 0

      # Workbook is created 
      wb = xlwt.Workbook() 

      # add_sheet is used to create sheet. 
      sheet1 = wb.add_sheet('ABC')

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
          
          ABC = aba(pop_size, Fitness,-bounds, +bounds, Dimensions, StopCriteriaFit)
          BEST, WORST, MEAN, MEDIAN, BEST_PAR, NUM_RUNS, SUCCESS = ABC.best_in, ABC.worst_in, ABC.mean_in, ABC.median_in, ABC.best_par, ABC.t, ABC.sucess_t
          
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
      wb.save('CEC2005 Function_4 - ABC.xls')
      
#--- EXECUTE
global StopCriteriaFit, OptimumFit
Dimensions = 10 #Dimensão do problema
Fitness = optproblems.cec2005.F2(Dimensions) #COST FUNCTION
bounds = 100  # input bounds
pop_size = 200

#Criterios de Parada
StopCriteriaFit = 10000*Dimensions #chamadas da função custo
StopCriteriaError = 10e-8 #proximidade com fitness minimo
OptimumFit = -450

#aba(pop_size, Fitness,-bounds, +bounds, Dimensions, StopCriteriaFit)
Output_Excel(25)