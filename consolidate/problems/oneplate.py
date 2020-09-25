from .domains import RectangularDomain
# from .boundaryconditions import LinearBC

class OnePlate:

    def __init__(self, deck):
        self.set_problem_parameters(deck)
        self.set_domains(deck)
        self.set_boundaryconds(deck)

    def set_problem_parameters(self, deck):
        self.dimensions = 2
        self.Lx = deck.doc["Geometry"]["Length (X)"]
        self.Ly = deck.doc["Geometry"]["Width (Y)"]

    def set_domains(self, deck):
        self.domains = []
        corner0 = (0,0)
        corner1 = (self.Lx ,self.Ly)
        plate_material = deck.doc["Materials"]["Plate"]
        self.domains.append(RectangularDomain( "Plate", corner0, corner1, plate_material))

    def set_boundaryconds(self, deck):
        self.boundaryconditions = []
        for deck_BC in deck.doc["Boundary Conditions"]:
            if deck_BC == "Top":
                self.boundaryconditions.append( LinearBC( (0.,self.Ly), (self.Lx,self.Ly), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Bottom":
                self.boundaryconditions.append( LinearBC( (0.,0.), (self.Lx, 0.), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Left":
                self.boundaryconditions.append( LinearBC( (0.,0.), (0.,self.Ly), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Right":
                self.boundaryconditions.append( LinearBC( (self.Lx,0.), (self.Lx,self.Ly), deck.doc["Boundary Conditions"][deck_BC] ) )