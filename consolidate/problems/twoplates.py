from .domains import RectangularDomain
from .boundaryconditions import LinearBC

class TwoPlates:

    def __init__(self, deck):

        self.required_fields = ["Temperature", "Thermal Conductivity X", "Thermal Conductivity Y", "Density", "Specific Heat"]
C
        self.set_problem_parameters(deck)
        self.set_domains(deck)
        self.set_boundaryconds(deck)
        self.set_initialconds(deck)


    
    def set_problem_parameters(self, deck):
        self.dimensions = 2
        Keys = []
        for deck_geometry in deck.doc["Geometry"]:
            # if deck_geometry == "Bottom Plate":
            Keys.append(deck_geometry)
        self.geometry=dict.fromkeys(Keys,None)    
        for deck_geometry in deck.doc["Geometry"]:
            # if deck_geometry == "Bottom Plate":
            self.geometry[deck_geometry]= [((float(deck.doc["Geometry"][deck_geometry]["Width (X)"]), float(deck.doc["Geometry"][deck_geometry]["Thickness (Y)"])))]
           

    def set_domains(self, deck):
        self.domains = []
        for deck_domain in deck.doc["Materials"]:
            if deck_domain == "Bottom Plate":
                corner0 = (0,0)
                corner1 = self.geometry[deck_domain][0]
                plate_material = deck.doc["Materials"][deck_domain]
                plate_initial_temperature=float(deck.doc["Initial Conditions"][deck_domain]["Initial Temperature"])
                element_order_0 = (0, 0)
                element_order_1 = (int(deck.doc["Mesh"][deck_domain]["Number of Elements in X"]), int(deck.doc["Mesh"][deck_domain]["Number of Elements in Y"])) 
                number_of_elements_X = int(deck.doc["Mesh"][deck_domain]["Number of Elements in X"])
                number_of_elements_Y = int(deck.doc["Mesh"][deck_domain]["Number of Elements in Y"])

                Power_Input_Density = float(deck.doc["Initial Conditions"][deck_domain]["Power Input Density"])
                Initial_Dic = 1/(1+float(deck.doc["Materials"][deck_domain]["DicW0OverB0"]))
                self.domains.append(RectangularDomain(deck_domain, corner0, corner1, plate_material,plate_initial_temperature, number_of_elements_X, number_of_elements_Y,Power_Input_Density,Initial_Dic ))

            elif deck_domain == "Heat Element":
                corner0 = (0,self.geometry["Bottom Plate"][0][1])
                corner1 = (self.geometry[deck_domain][0][0],self.geometry["Bottom Plate"][0][1]+self.geometry[deck_domain][0][1])
                plate_material = deck.doc["Materials"][deck_domain]
                plate_initial_temperature=float(deck.doc["Initial Conditions"][deck_domain]["Initial Temperature"])
                element_order_0 = (0, element_order_1[1])
                element_order_1 = (int(deck.doc["Mesh"][deck_domain]["Number of Elements in X"]), element_order_1[1]+int(deck.doc["Mesh"][deck_domain]["Number of Elements in Y"])+element_order_1[1]) 
                number_of_elements_X = int(deck.doc["Mesh"][deck_domain]["Number of Elements in X"])
                number_of_elements_Y = int(deck.doc["Mesh"][deck_domain]["Number of Elements in Y"])

                
                Power_Input_Density = float(deck.doc["Initial Conditions"][deck_domain]["Power Input Density"])
                Initial_Dic = 1/(1+float(deck.doc["Materials"][deck_domain]["DicW0OverB0"]))
                self.domains.append(RectangularDomain(deck_domain, corner0, corner1, plate_material,plate_initial_temperature, number_of_elements_X, number_of_elements_Y,Power_Input_Density,Initial_Dic ))

                
            elif deck_domain == "Top Plate":
                corner0 = (0,self.geometry["Bottom Plate"][0][1]+self.geometry["Heat Element"][0][1])
                corner1 = (self.geometry[deck_domain][0][0],self.geometry["Bottom Plate"][0][1]+self.geometry["Heat Element"][0][1]+self.geometry[deck_domain][0][1])
                plate_material = deck.doc["Materials"][deck_domain]
                plate_initial_temperature=float(deck.doc["Initial Conditions"][deck_domain]["Initial Temperature"])
                element_order_0 = (0, element_order_1[1])
                element_order_1 = ( int(deck.doc["Mesh"][deck_domain]["Number of Elements in X"]), element_order_1[1]+int(deck.doc["Mesh"][deck_domain]["Number of Elements in Y"])+element_order_1[1] )
                number_of_elements_X = int(deck.doc["Mesh"][deck_domain]["Number of Elements in X"])
                number_of_elements_Y = int(deck.doc["Mesh"][deck_domain]["Number of Elements in Y"])
                
                Power_Input_Density = float(deck.doc["Initial Conditions"][deck_domain]["Power Input Density"])
                Initial_Dic = 1/(1+float(deck.doc["Materials"][deck_domain]["DicW0OverB0"]))
                self.domains.append(RectangularDomain(deck_domain, corner0, corner1, plate_material,plate_initial_temperature, number_of_elements_X, number_of_elements_Y,Power_Input_Density,Initial_Dic ))

                
    def set_boundaryconds(self, deck):
        self.boundaryconditions = []
        for deck_BC in deck.doc["Boundary Conditions"]:
            if deck_BC == "Top Plate Top":
                self.boundaryconditions.append( LinearBC( (0.,self.domains[2].y1), (self.domains[2].x1,self.domains[2].y1), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Top Plate Left":
                self.boundaryconditions.append( LinearBC( (0.,self.domains[2].y0), (0.,self.domains[2].y1), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Top Plate Right":
                self.boundaryconditions.append( LinearBC( (self.domains[2].x1,self.domains[2].y0), (self.domains[2].x1,self.domains[2].y1), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Bottom Plate Bottom":
                self.boundaryconditions.append( LinearBC( (self.domains[0].x0,self.domains[0].y0), (self.domains[0].x1,0.), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Bottom Plate Left":
                self.boundaryconditions.append( LinearBC( (0.,0.), (0.,self.domains[0].y1), deck.doc["Boundary Conditions"][deck_BC] ) )
            elif deck_BC == "Bottom Plate Right":
                self.boundaryconditions.append( LinearBC( (self.domains[0].x1,0.), (self.domains[0].x1,self.domains[0].y1), deck.doc["Boundary Conditions"][deck_BC] ) )

   
    def set_initialconds(self, deck):
        for domain in self.domains:
            for field in self.required_fields:
                if field in field in deck.doc["Materials"][domain.name]:

                    domain.set_field_init_value({field: deck.doc["Materials"][domain.name][field]})        
