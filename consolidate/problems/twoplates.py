from .domains import RectangularDomain
# from .local_mesh import LocalFields
# from .bc import BoundaryCondition
# from .power import PowerInput
import numpy as np


class TwoPlates:

    def __init__(self, deck):
        self.set_simulation_parameters(deck)
        self.create_fields(deck)
        self.set_problem_parameters(deck)
        self.set_domains(deck)
        
        self.set_material(deck)
        self.set_initial_cond(deck)
        self.set_bc_cond(deck)
        self.set_create_mask(deck)
        self.populate_fields_locally(deck)


    def set_simulation_parameters(self,deck):
        self.SimulationParameters = {}
        for par in deck.doc["Simulation"]:
            self.SimulationParameters[par] = deck.doc["Simulation"][par]


    def create_fields(self, deck):
        if deck.doc["Problem Type"]["Type"] == "Welding":
            self.required_fields=["Temperature", "kx", "ky", "Density", "Cp",  "Power Input Heat", "Intimate Contact", "dx","dy","Convection Coefficient", "Interface Temperature"]
        if deck.doc["Problem Type"]["Type"] == "Heat Transfer":
            self.required_fields=["Temperature", "Thermal", "Density", "Power Input Heat", "increments", "Convection Coefficient", "Interface Temperature", "Viscosity"]


    def set_problem_parameters(self, deck):
        ny = 0
        thickness = 0
        count = 0
        for domain in deck.doc["Domains"]:
            domain_dir = deck.doc["Domains"][domain]
            if count == 0:
                ny = int((domain_dir["Mesh"]["Points in Y"]))
                count = count+1
            else:
                ny = ny + int(domain_dir["Mesh"]["Points in Y"])-1
            nx = int(domain_dir["Mesh"]["Points in X"])
            current_thickness = float(domain_dir["Geometry"]["y1"])
            if current_thickness > thickness:
                thickness = current_thickness
        self.totalnodes = [nx, ny]
        self.thickness = thickness
        self.length = float(deck.doc["Problem Type"]["Length"])


    def is_top_plate(self,y1,totalthickness):
        return y1 == totalthickness


    def is_bottom_plate(self,y0):
        return y0 == 0


    def set_domains(self, deck):
        self.domains = []
        count=0
        for domain_name in deck.doc["Domains"]:
            bc ={}
            domain_dir = deck.doc["Domains"][domain_name]
            dimen_x0 = float(domain_dir["Geometry"]["x0"])
            dimen_x1 = float(domain_dir["Geometry"]["x1"])
            dimen_y0 = float(domain_dir["Geometry"]["y0"])
            dimen_y1 = float(domain_dir["Geometry"]["y1"])
            dimen_y0 = float(domain_dir["Geometry"]["y0"])
            dimen_y1 = float(domain_dir["Geometry"]["y1"])
            count=1
            if self.is_bottom_plate(dimen_y0):
                p_x0 = 0
                p_x1 = int(deck.doc["Domains"][domain_name]["Mesh"]["Points in X"])-1
                p_y0 = 0
                p_y1= int(deck.doc["Domains"][domain_name]["Mesh"]["Points in Y"])-1
            else:
                aux=0
                for i in range (1, int(domain_name[-1])):
                    aux = aux +  int(deck.doc["Domains"]["Plate " + str(i)]["Mesh"]["Points in Y"])-1
                p_x0 = 0
                p_x1 = int(deck.doc["Domains"][domain_name]["Mesh"]["Points in X"])-1*count
                p_y0 = aux
                p_y1 = aux + int(deck.doc["Domains"][domain_name]["Mesh"]["Points in Y"])-1*count
                count=count+1
            nodes=[[p_x0,p_x1],[p_y0, p_y1]]

            material={}
            for param in domain_dir["Material Properties"]:
                if isinstance(domain_dir["Material Properties"][param], str):
                    material[param] = float(domain_dir["Material Properties"][param])
                else:
                    material[param]={}
                    for aux in domain_dir["Material Properties"][param]:
                        material[param].update({aux: float(domain_dir["Material Properties"][param][aux])})

            power = {}
            for cond_name in domain_dir["Initial Condition"]:
                if cond_name == "Power Input":
                    for location in domain_dir["Initial Condition"]["Power Input"]:
                        power.update({location : float(domain_dir["Initial Condition"]["Power Input"][location])})


            self.domains.append(RectangularDomain(domain_name, dimen_x0, dimen_x1, dimen_y0, dimen_y1, nodes, power))


    def set_create_mask(self, deck):
        for i,domain in enumerate(self.domains):
            domain.generate_mask(i,self.totalnodes[1],self.totalnodes[0], self.thickness)


    def set_material(self, deck):
        for domain in self.domains:
            material ={}
            domain_dir = deck.doc["Domains"][domain.name]["Material Properties"]
            for param in domain_dir:
                if isinstance(domain_dir[param], str):
                    material[param] = float(domain_dir[param])
                else:
                    # import pdb; pdb.set_trace()
                    material[param]={}
                    for aux in domain_dir[param]:
                        material[param].update({aux: float(domain_dir[param][aux])})
            domain.set_material(material)


    def set_initial_cond(self, deck):
        for domain in self.domains:
            initial_cond ={}
            domain_dir = deck.doc["Domains"][domain.name]["Initial Condition"]
            for cond_name in domain_dir:
                if isinstance(domain_dir[cond_name], str):
                    initial_cond.update({cond_name: float(domain_dir[cond_name])})
                else:
                    initial_cond[cond_name] = {}
                    for location in domain_dir[cond_name]:
                        initial_cond[cond_name].update({location: float(domain_dir[cond_name][location])})
            domain.set_initial_cond(initial_cond)


    def set_bc_cond(self, deck):
        for domain in self.domains:
            domain_dir = deck.doc["Domains"][domain.name]["Boundary Condition"]
            bc ={}
            h={}
            for bc_type in domain_dir:
                bc[bc_type]={}
                for kind in domain_dir[bc_type]:
                    bc[bc_type][kind]={}
                    for edge in domain_dir[bc_type][kind]:
                        bc[bc_type][kind][edge]={}
                        for param in domain_dir[bc_type][kind][edge]:
                            bc[bc_type][kind][edge].update({param : float(domain_dir[bc_type][kind][edge][param])})
                            if kind == "Constant Temperature":
                                bc[bc_type][kind][edge].update({"h" : 0})
            domain.set_bc(bc)


    def populate_fields_locally(self, deck):
        for domain in self.domains:
            for field_name in self.required_fields:
                value=0
                value_dict ={}
                extTemp=0
                if field_name == "increments":
                    deltaX = domain.dimensions[0][1] - domain.dimensions[0][0]
                    incX = deltaX/(domain.nodes[0][1] - domain.nodes[0][0])
                    valueX = incX*domain.mask_inter_nodes["Inner"]
                    value_dict["dx"] = valueX

                    deltaY = domain.dimensions[1][1] - domain.dimensions[1][0]
                    incY = deltaY/(domain.nodes[1][1] - domain.nodes[1][0])
                    valueY = incY*domain.mask_inter_nodes["Inner"]
                    value_dict["dy"] = valueY
                    
                    domain.set_field(field_name, value_dict)


                elif field_name == "dy":
                    deltaY = domain.dimensions[1][1] - domain.dimensions[1][0]
                    incY = deltaY/(domain.nodes[1][1] - domain.nodes[1][0])
                    value = incY*domain.mask_inter_nodes["Inner"]
                    domain.set_field(field_name, value)
                    


                elif field_name == "Temperature":
                    value = domain.initial_condition["Temperature"]*domain.mask_inter_nodes["Inner"]
                    h=np.zeros((self.totalnodes[1], self.totalnodes[0]))
                    Tint = np.zeros(np.shape(domain.mask_inter_nodes["Inner"]))
                    
                    for kind in domain.boundary_condition["Thermal"]:
                        for edge in domain.boundary_condition["Thermal"][kind]:
                            Tint = Tint + domain.boundary_condition["Thermal"][kind][edge]["Temperature"]*domain.mask_inter_nodes[edge]
                            if kind == "Fixed Boundary":
                                h=h
                            elif kind == "Convection":
                                h = h + domain.boundary_condition["Thermal"][kind][edge]["Convection Coefficient"]*(domain.mask_inter_nodes[edge]) 
                            
                    #             value = value + domain.boundary_condition["Thermal"][kind][edge]["Temperature"]*domain.mask_out[edge]
                    #             h=h
                    #         elif kind == "Convection":
                    #             value = value + domain.boundary_condition["Thermal"][kind][edge]["Temperature"]*domain.mask_out[edge]
                    #             h = h + domain.boundary_condition["Thermal"][kind][edge]["Convection Coefficient"]*(domain.mask_out[edge])
                    # # if domain.nodes[1][0] !=0 and domain.nodes[1][1] != self.totalnodes[1]-1:
                    #     # for edge in domain.mask_interface:
                    #     #     value = value + domain.initial_condition["Temperature"]*domain.mask_inter_nodes
                    domain.set_field(field_name, value)
                    domain.set_field("Convection Coefficient", h)
                    domain.set_field("Interface Temperature", Tint)
                    
                elif field_name in domain.material:
                    if isinstance(domain.material[field_name], float):
                        value = domain.material[field_name] * domain.mask_inter_nodes["Inner"]
                    else:
                        value ={}
                        for var in domain.material[field_name].keys():
                            value.update({var: domain.material[field_name][var]*domain.mask_inter_nodes["Inner"] })
                    domain.set_field(field_name, value)


                elif field_name == "Power Input Heat":
                    value = np.zeros((self.totalnodes[1]+1, self.totalnodes[0]+1))
                    if bool(domain.power):
                        for location in domain.power:
                            value = value + domain.power[location]*domain.mask_inter_nodes[location]
                    else:
                        value = value
                    domain.set_field(field_name, value)





