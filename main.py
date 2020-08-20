from consolidate import *

cwd = os.getcwd()
# All the data from deck.yaml is now in the following deck variable

deck = Deck( cwd + "/TwoPlates.yaml" )

problem = TwoPlates(deck)

mesh = Mesher( problem )
