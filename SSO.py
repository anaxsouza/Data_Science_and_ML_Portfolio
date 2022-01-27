import numpy as np
import optproblems
import optproblems.cec2005
from math import ceil, exp, floor
from random import random
import xlwt

global StopCriteriaFit, OptimumFit
    
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

class ssa(sw):
    """
    Social Spider Optimization
    """

    def __init__(self, n, function, lb, ub, dimension, iteration, pf):
        """
        :param n: number of agents
        :param function: test function
        :param lb: lower limits for plot axes
        :param ub: upper limits for plot axes
        :param dimension: space dimension
        :param iteration: the number of iterations
        :param pf: random parameter from 0 to 1 (default value is 0.4)
        """
        
        super(ssa, self).__init__()

        self.__agents = np.random.uniform(lb, ub, (n, dimension))

        nf = floor((0.9 - random() * 0.25) * n)
        nm = n - nf

        Nf = self.__agents[:nf]
        Nm = self.__agents[nf:]

        r = (ub - lb) / 2

        def Object_Funct(spider):
            spider = list(spider)
            for index1 in range(len(spider)):
                if spider[index1] > 100:
                    spider[index1] = 100

                elif spider[index1] < -100:
                    spider[index1] = -100

            return function(np.array(spider))


        pb = np.array([Object_Funct(x) for x in self.__agents]).argmin()
        pw = np.array([Object_Funct(x) for x in self.__agents]).argmax()
        Pbest = self.__agents[pb]
        Pworst = self.__agents[pw]
        Gbest = Pbest
        globalBest = Object_Funct(Pbest)
        
        self.best_par = []
        self.best_all = []
        self.sucess_t = 0 
        fim = False
        self.t = 0
        while (not fim):
            
            W = (np.array([Object_Funct(i) for i in self.__agents]) -
                 Object_Funct(Pworst)) / (Object_Funct(Pbest) - Object_Funct(Pworst))

            Wf = W[:nf]
            Wm = W[nf:]

            Distf = [self.__nearest_spider(i, Nf) for i in Nm]
            Vibrf = np.array([W[i[1]] * exp(-i[0]**2) for i in Distf])

            Distb = [np.linalg.norm(i - Pbest) for i in self.__agents]
            Vibrb = np.array([W[pb] * exp(-i**2) for i in Distb])

            Distc = [[(np.linalg.norm(self.__agents[i] - self.__agents[j]), j)
                     for j in range(n)] for i in range(n)]
            for i in range(len(Distc)):
                Distc[i].sort()
            Vibrc = []
            for i in range(n):
                for j in range(1, n):
                    dist = Distc[i][j][0]
                    k = Distc[i][j][1]
                    if W[k] < W[i]:
                        Vibrc.append(W[k] * exp(-dist**2))
                        break
                else:
                    Vibrc.append(W[i])
            Vibrc = np.array(Vibrc)

            fitness = [(Object_Funct(Nm[i]), i) for i in range(nm)]
            fitness.sort()
            cent_male = Nm[fitness[ceil(nm/2)][1]]
            a = sum([Nm[j] * Wm[j] for j in range(nm)]) / sum([Wm[j] for j
                                                               in range(nm)])
            for i in range(n):

                alpha = np.random.random((1, dimension))[0]
                betta = np.random.random((1, dimension))[0]
                gamma = np.random.random((1, dimension))[0]

                r1 = np.random.random((1, dimension))[0]
                r2 = np.random.random((1, dimension))[0]
                r3 = np.random.random((1, dimension))[0]

                if i < nf:
                    if random() < pf:
                        k = Distc[i][1][1]
                        self.__agents[i] += alpha * Vibrc[i] * \
                            (self.__agents[k] - self.__agents[i]) + betta * \
                                Vibrb[i] * (Pbest - self.__agents[i]) + \
                                            gamma * (r1 - 0.5)
                    else:
                        k = Distc[i][1][1]
                        self.__agents[i] -= alpha * Vibrc[i] * \
                            (self.__agents[k] - self.__agents[i]) - betta * \
                                Vibrb[i] * (Pbest - self.__agents[i]) + \
                                            gamma * (r2 - 0.5)
                else:
                    if Object_Funct(cent_male) > Object_Funct(self.__agents[i]):
                        m = i - nf - 1
                        k = Distf[m][1]
                        self.__agents[i] += alpha * Vibrf[m] * \
                            (self.__agents[k] - self.__agents[i]) +\
                                            gamma * (r3 - 0.5)
                    else:
                        self.__agents[i] += alpha * (a - self.__agents[i])


            Nf = self.__agents[:nf]
            Nm = self.__agents[nf:]

            best = Nm[np.array([Object_Funct(x) for x in Nm]).argmin()]
            indexes = [i for i in range(nf)
                       if np.linalg.norm(Nf[i] - best) <= r]

            nearest = [Nf[i] for i in indexes]

            L = len(nearest)

            if L:
                P = [Wf[i] / sum([Wf[i] for i in indexes]) for i in indexes]
                new_spiders = best + sum([P[i] * nearest[i] for i in range(L)])
                if Object_Funct(new_spiders) < Object_Funct(Pworst):
                    self.__agents[pw] = new_spiders

            self.__agents = np.clip(self.__agents, lb, ub)
            self._points(self.__agents)

            pb = np.array([Object_Funct(x) for x in self.__agents]).argmin()
            pw = np.array([Object_Funct(x) for x in self.__agents]).argmax()

            Pbest = self.__agents[pb]
            Pworst = self.__agents[pw]
            CurrentBest = Object_Funct(Pbest)
            iteration -= 10
            if CurrentBest < globalBest:
                Gbest = Pbest
                globalBest = CurrentBest
                            
            erro = globalBest - OptimumFit
            print(self.t,erro)
            self.best_all.append(erro)
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

    def __nearest_spider(self, spider, spiders):
        spudis = list(spiders)
        try:
            pos = spudis.index(spider)
            spudis.pop(pos)
        except ValueError:
            pass

        dists = np.array([np.linalg.norm(spider - s) for s in spudis])
        m = dists.argmin()
        d = dists[m]
        return d, m

def Output_Excel(number_runs):
      success_rate = 0

      # Workbook is created 
      wb = xlwt.Workbook() 

      # add_sheet is used to create sheet. 
      sheet1 = wb.add_sheet('SSO')

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
          
          SSO = ssa(pop_size, Fitness, -bounds, +bounds, Dimensions, StopCriteriaFit, pf)
          BEST, WORST, MEAN, MEDIAN, BEST_PAR, NUM_RUNS, SUCCESS = SSO.best_in, SSO.worst_in, SSO.mean_in, SSO.median_in, SSO.best_par, SSO.t, SSO.sucess_t
          
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
      wb.save('CEC2005 Function_3 - SSO.xls')

#--- EXECUTE
Dimensions = 10 #Dimensão do problema
Fitness = optproblems.cec2005.F3(Dimensions) #COST FUNCTION
bounds = 100  # input bounds
pop_size = 50 #tamanho da população
pf = 0.6 #probabilidade de alterar posição

#Criterios de Parada
StopCriteriaFit = 10000*Dimensions #chamadas da função custo
StopCriteriaError = 10e-8 #proximidade com fitness minimo
OptimumFit = -450

#ssa(pop_size, Fitness, -bounds, +bounds, Dimensions, StopCriteriaFit, pf)
Output_Excel(25)








