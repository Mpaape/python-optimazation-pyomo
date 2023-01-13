import pyomo.environ as pyo
from pyomo.opt import SolverFactory

#defining the model

model = pyo.ConcreteModel()

#Decision variables

# x1 number o deluxe belts produced week
# x2 number o regular belts produced week
model.x1 = pyo.Var(within=pyo.NonNegativeReals)
x1 = model.x1
model.x2 = pyo.Var(within=pyo.NonNegativeReals)
x2 = model.x2

#objective function
model.Obj = pyo.Objective(expr= 4*x1+3*x2,sense=pyo.maximize)

#constraints
model.Const1 = pyo.Constraint(expr= x1+x2<=40)
model.Const2 = pyo.Constraint(expr= 2*x1+x2<=60)

#solve
optm = SolverFactory('glpk')
results = optm.solve(model)

print(results)
print("objective function = ", model.Obj())
print(" x1 = ", model.x1())
print("x2 =",model.x2())

