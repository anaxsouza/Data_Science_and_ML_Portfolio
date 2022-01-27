from __future__ import division
import random
import numpy as np
import optproblems
import optproblems.cec2005
import xlwt

#--- MAIN 
class Particle:
    def __init__(self,x0):
        self.position_i=[]          # particle position
        self.velocity_i=[]          # particle velocity
        self.pos_best_i=[]          # best position individual
        self.err_best_i=-1          # best error individual
        self.err_i=-1               # error individual

        for i in range(0,num_dimensions):
            self.velocity_i.append(random.uniform(-1,1))
            self.position_i.append(x0[i])

    # evaluate current fitness
    def evaluate(self,costFunc):
        self.err_i=costFunc(self.position_i)

        # check to see if the current position is an individual best
        if self.err_i < self.err_best_i or self.err_best_i==-1:
            self.pos_best_i=self.position_i
            self.err_best_i=self.err_i

    # update new particle velocity
    def update_velocity(self,pos_best_g,w,c1,c2):        
        ##w=0.5  # constant inertia weight (how much to weigh the previous velocity)
        ##c1=1   # cognative constant
        ##c2=2   # social constant

        for i in range(0,num_dimensions):
            r1=random.random()
            r2=random.random()

            vel_cognitive=c1*r1*(self.pos_best_i[i]-self.position_i[i])
            vel_social=c2*r2*(pos_best_g[i]-self.position_i[i])
            self.velocity_i[i]=w*self.velocity_i[i]+vel_cognitive+vel_social

    # update the particle position based off new velocity updates
    def update_position(self,bounds):
        for i in range(0,num_dimensions):
            self.position_i[i]=self.position_i[i]+self.velocity_i[i]

            # adjust maximum position if necessary
            if self.position_i[i]>bounds[i][1]:
                self.position_i[i]=bounds[i][1]

            # adjust minimum position if neseccary
            if self.position_i[i] < bounds[i][0]:
                self.position_i[i]=bounds[i][0]
                
def PSO(costFunc,x0,bounds,num_particles,maxiter,w,c1,c2):
    
        global num_dimensions
        best_par = []
        best_all = []
        success = 0 
        num_dimensions=len(x0)
        err_best_g=-1                   # best error for group
        pos_best_g=[]                   # best position for group

        # establish the swarm
        swarm=[]
        for i in range(0,num_particles):
            swarm.append(Particle(x0))

        # begin optimization loop
        fim = False
        i = 0
        while (not fim):
            # cycle through particles in swarm and evaluate fitness
            for j in range(0,num_particles):
                swarm[j].evaluate(costFunc)
                maxiter -= 1
                
                # determine if current particle is the best (globally)
                if swarm[j].err_i < err_best_g or err_best_g == -1:
                    pos_best_g=list(swarm[j].position_i)
                    err_best_g=float(swarm[j].err_i)

            # cycle through swarm and update velocities and position
            for j in range(0,num_particles):
                swarm[j].update_velocity(pos_best_g,w,c1,c2)
                swarm[j].update_position(bounds)
                
            erro = err_best_g - OptimumFit
            best_all.append(erro)
            print(i,erro)
            i+=1
            if i % 10 == 0:
                best_par.append(err_best_g)
            #Critério de Parada        
            if erro < StopCriteriaError:
                success = 1
                fim = True
            if maxiter <= 0:
                fim = True

        # print final results
        print("Best: ",err_best_g,list(pos_best_g))
        best_in = min(best_all)
        worst_in = max(best_all)
        mean_in = np.mean(best_all)
        median_in = np.median(best_all)
        print(success)
        return best_in, worst_in, mean_in, median_in, best_par, i, success

global StopCriteriaFit, OptimumFit,Fitness,initial,bounds,nParticles,w,c1,c2

#--- EXECUTE
Dimensions = 10 #Dimensão do problema
Fitness = optproblems.cec2005.F3(Dimensions) #COST FUNCTION 
initial= np.random.uniform(-100, +100, Dimensions)  # initial starting location [x1,x2...]
bounds=[(-100,100),(-100,100)]*Dimensions  # input bounds [(x1_min,x1_max),(x2_min,x2_max)...]
nParticles = 100
w=0.4  # constant inertia weight (how much to weigh the previous velocity)
c1=1  # cognative constant
c2=2   # social constant

#Criterios de Parada
StopCriteriaFit = 10000*Dimensions #chamadas da função custo
StopCriteriaError = 10e-8 #proximidade com fitness minimo
OptimumFit = -450

def Output_Excel(number_runs):
      success_rate = 0

      # Workbook is created 
      wb = xlwt.Workbook() 

      # add_sheet is used to create sheet. 
      sheet1 = wb.add_sheet('PSO')

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
          
          BEST, WORST, MEAN, MEDIAN, BEST_PAR, NUM_RUNS, SUCCESS = PSO(Fitness,initial,bounds,nParticles,StopCriteriaFit,w,c1,c2)
          
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
      wb.save('CEC2005 Function_3 - PSO.xls')

#PSO(Fitness,initial,bounds,nParticles,StopCriteriaFit,w,c1,c2)
Output_Excel(25)

