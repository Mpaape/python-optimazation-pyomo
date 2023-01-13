#Challenge problem
#three eletric power plants for four cities

import pyomo.environ as pyo
from pyomo.opt import SolverFactory

#defining model
model = pyo.ConcreteModel()

#decision Variables
    #i = 1,2,3
    #plant1,plant2,plant3
    #j = 1,2,3,4
    # city1,city2,city3,city4
#xij = planti sent to cityj

#set 
model.i = pyo.RangeSet(1,3)
model.j = pyo.RangeSet(1,4)

# paramaters (P,S,D) #preco, #oferta # demanda
# Parameters
model.S = pyo.Param(model.i,initialize = {1:35,2:50,3:40})
S = model.S
model.D = pyo.Param(model.j,initialize = {1:45,2:20,3:30,4:30})
D = model.D
model.P = pyo.Param(model.i,model.j, initialize = {(1,1):8,(1,2):6,(1,3):10,(1,4):9,
                                                   (2,1):9,(2,2):12,(2,3):13,(2,4):7,
                                                   (3,1):14,(3,2):9,(3,3):16,(3,4):5})
P = model.P
#DECISION VARIABLES
model.x = pyo.Var(model.i,model.j, within=pyo.NonNegativeReals)
x = model.x
 
#objective function 
#minimize the cost of peak city
def objective_rule(model):
    return sum(sum(P[i,j]*x[i,j] for i in model.i) for j in model.j)

model.Objf = pyo.Objective(rule=objective_rule,sense=pyo.minimize)



# restriction of resources
# the combination of resources must be less than all avaible

#constranints
    #supply constraints
 
# Constraints
def Constraint1(model,i):
  return sum(x[1,j] for j in model.j) <= S[1]
model.Const1 = pyo.Constraint(model.j, rule = Constraint1)

def Constraint2(model,i):
  return sum(x[2,j] for j in model.j) <= S[2]
model.Const2 = pyo.Constraint(model.j, rule = Constraint2)

def Constraint3(model,i):
  return sum(x[3,j] for j in model.j) <= S[3]
model.Const3 = pyo.Constraint(model.j, rule = Constraint3)

def Constraint4(model,j):
  return sum(x[i,1] for i in model.i) >= D[1]
model.Const4 = pyo.Constraint(model.i, rule = Constraint4)

def Constraint5(model,j):
  return sum(x[i,2] for i in model.i) >= D[2]
model.Const5 = pyo.Constraint(model.i, rule = Constraint5)

def Constraint6(model,j):
  return sum(x[i,3] for i in model.i) >= D[3]
model.Const6 = pyo.Constraint(model.i, rule = Constraint6)

def Constraint7(model,j):
  return sum(x[i,4] for i in model.i) >= D[4]
model.Const7 = pyo.Constraint(model.i, rule = Constraint7)

#solver
Solver = SolverFactory('glpk')
results = Solver.solve(model)


print(results)
print('Objective Function = ', model.Objf())

for i in model.i:
  for j in model.j:
    print('Electricity send from Plant',i, 'to City',j, '=', x[i,j]())
