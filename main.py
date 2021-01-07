from consolidate import *

cwd = os.getcwd()
# All the data from deck.yaml is now in the following deck variable

deck = Deck( cwd + "/twoplates.yaml" )

problem = TwoPlates(deck)

mesh = Mesher( problem )

model_HT = HeatTransfer(mesh, problem)

# model_visc =  ViscosityCalculation(problem, mesh)

solves = SolvesTwoPlates( problem,model_HT,mesh)