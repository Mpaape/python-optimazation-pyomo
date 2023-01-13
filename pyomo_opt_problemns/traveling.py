

# Joe State lives in Gary, Indiana. He owns insurance agencies in Gary,
#  Fort Wayne, Evansville, Terre Haute, and South Bend. Each December, 
#  he visits each of his insurance agencies. The distance between each agency (in miles) is shown in Table 65. 
#  What order of visiting his agencies will minimize the total distance traveled?


#imports uteis
import numpy as np
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import pandas as pd 

model = pyo.ConcreteModel()


#sets 
model.i = pyo.Set(initialize=['City1','City2','City3','City4','City5'])
model.j = pyo.Set(initialize=['City1','City2','City3','City4','City5'])

model.ii =pyo.Set(initialize=['City2','City3','City4','City5'])

# Parameters
C = pd.read_excel('./Data/S5P3_Data.xlsx', 'TSP',header=0,index_col=0,usecols='A:F',nrows=5)
C.head()
print(C['City1']['City2'])

#Decision Variable
model.x = pyo.Var(model.i,model.j,domain=pyo.Binary)
x = model.x

model.u = pyo.Var(model.i,domain=pyo.NonNegativeReals)
u = model.u


#Objective function
def object_rule(model):
    return sum(sum(C[i][j]*x[i,j] for i in model.i) for j in model.j)

model.Objf = pyo.Objective(rule=object_rule,sense = pyo.minimize)


#contraints
def Constraint1(model,j):
    return sum(x[i,j] for i in model.i) == 1
model.Const1 = pyo.Constraint(model.i,rule=Constraint1)

def Constraint2(model,i):
    return sum(x[i,j] for j in model.j) == 1
model.Const2 = pyo.Constraint(model.j,rule=Constraint2)

def Constraint3(model,i,j):
    if i != j:
        return u[i]-u[j]+5*x[i,j]<=4
    else:
        return u[i] - u[i] == 0

model.Const3 = pyo.Constraint(model.ii,model.ii,rule=Constraint3)

#solver
solver = SolverFactory('cplex_direct')
results = solver.solve(model)

print(results)
print( 'Object func =',model.Objf())
for i in model.i:
    for j in model.j:
        if x[i,j]() != 0:
            print('Sales goes from',i,'to',j,'=',x[i,j]())