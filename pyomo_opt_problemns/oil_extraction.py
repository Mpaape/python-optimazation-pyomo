# Oilco must determine how many barrels of oil to extract during each of the next two years.
# If Oilco extracts x1 million barrels during year 1, each barrel can be sold for $30  x1.
# If Oilco extracts x2 million barrels during year 2, each barrel can be sold for $35  x2.
# The cost of extracting x1 million barrels during year 1 is x 2
# 1 million dollars, and the cost
# of extracting x2 million barrels during year 2 is 2x 2
# 2 million dollars. 
# A total of 20 million barrels of oil are available, and at most $250 million can be spent on extraction.
#  Formulate an NLP to help Oilco maximize profits (revenues less costs) for the next two years.

 #conda install -c conda-forge couenne
#chapter 11


#import
import pyomo.environ as pyo
from pyomo.opt import SolverFactory

#model instance

model = pyo.ConcreteModel()

#sets \ params
# i = 1,2 , no need to create

#Decision Variable
model.x1 = pyo.Var(domain = pyo.NonNegativeIntegers)
x1 = model.x1

model.x2 = pyo.Var(domain = pyo.NonNegativeIntegers)
x2 = model.x2

#Objective Function
model.Objf = pyo.Objective(expr = 30*x1+35*x2 - 2*(x1**2) - 3*(x2**2), sense = pyo.maximize)

#Constraints
model.Const1 = pyo.Constraint(expr = x1+x2 <= 20)

model.Const2 = pyo.Constraint(expr = (x1**2)+2*(x2**2)<=250)

Solver = SolverFactory('couenne',executable='/solvers/couenne')
results = Solver.solve(model)

print(results)
print('Objective Function= ',model.Objf())
print('x1 = ',x1())
print('x2 = ',x2())
