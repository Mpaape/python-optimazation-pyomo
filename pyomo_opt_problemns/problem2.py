import pyomo.environ as pyo
from pyomo.opt import SolverFactory


#defining model

model = pyo.ConcreteModel()

#decision variables
#must decides how many of each product must be produced
# i = 1,2,3
#x1 number of desks produced
#x2 number of tables produced
#x3 number of chairs produced 

model.i = pyo.Set(initialize=['Desk','Table','Chair'])

## parametrs
model.L = pyo.Param(model.i,initialize={'Desk':8,'Table':6,'Chair':1})
L = model.L

model.F = pyo.Param(model.i,initialize={'Desk':4,'Table':2,'Chair':1.5})
F = model.F

model.C = pyo.Param(model.i,initialize={'Desk':2,'Table':1.5,'Chair':1})
C = model.C

model.P = pyo.Param(model.i,initialize={'Desk':60,'Table':30,'Chair':20})
P = model.P


model.x=pyo.Var(model.i,within=pyo.NonNegativeReals)
x = model.x

#objective function
#wich variable is will be minimized of maximized. subject to the decision
#variables

#max z 60x1+ 30x2+20x3
def objective_rule(model):
    return sum(P[i]*x[i] for i in model.i)


model.Obj = pyo.Objective(rule=objective_rule,sense=pyo.maximize)


#constraints 
#8x1 + 6x2 + x3 <=48
#4x1 + 6x2 + 1.5x3 <= 20
#2x1 + 6x2 + 0.5x3 <= 8
#x2<= 5


def Constraint1(model,i):
    return sum(L[i]*x[i] for i in model.i) <=48

model.Const1 = pyo.Constraint(model.i,rule=Constraint1)

def Constraint2(model,i):
    return sum(F[i]*x[i] for i in model.i) <=20

model.Const2 = pyo.Constraint(model.i,rule=Constraint2)

def Constraint3(model,i):
    return sum(C[i]*x[i] for i in model.i) <=8

model.Const3 = pyo.Constraint(model.i,rule=Constraint3)


def Constraint4(model,i):
    return x['Table'] <=6
model.Const4 = pyo.Constraint(model.i,rule=Constraint4)

#solver
Solver = SolverFactory('glpk')
results = Solver.solve(model)

print(results)
print('Objective Function = ',model.Obj())
for i in model.i:
    print("Number of",i,"produced = ",x[i]())