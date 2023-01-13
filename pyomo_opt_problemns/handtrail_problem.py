 #conda install -c conda-forge ipopt
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
 #model
model = pyo.ConcreteModel()

#decision variables
model.x1 = pyo.Var(domain=pyo.NonNegativeReals)
x1= model.x1

model.x2 = pyo.Var(domain=pyo.NonNegativeReals)
x2= model.x2

#objective function
def objective_rule(model):
    return x1*x2 - 180

model.Objf = pyo.Objective(rule=objective_rule,sense=pyo.maximize)

#Constraints
def Constraint1(model):
    return 0.5*x1-0.5*x2 <= -4
model.Const1 = pyo.Constraint(rule=Constraint1)
def Constraint2(model):
    return 2*x1+ 2*x2 <= 194
    
model.Const2 = pyo.Constraint(rule=Constraint2)

Solver = SolverFactory('ipopt',executable = "solvers\ipopt")
results = Solver.solve(model)

print(results)
print("Object Function =",model.Objf())
print("the amout of x1 =",x1())
print("the amout of x2 =",x2())