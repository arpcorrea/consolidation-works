# import numpy as np
import numpy as np

            
class Field:
    
    def __init__(self, field):
        self.name=field


    def set_initial_conditions_field(self, problem):
        value=0
        for domain in problem.domains:
            value = value + domain.mask * domain.initial_conditions[self.name]
        self.value = value
        
    def set_material_field(self, problem):
        value=0
        for domain in problem.domains:
            if isinstance(domain.material[self.name],dict) == False:
                value = value + domain.mask*domain.material[self.name]
            if isinstance(domain.material[self.name], dict) == True:
                aux=[]
                for param in domain.material[self.name]:
                    aux.append(domain.material[self.name][param])
                value = value+domain.mask*aux[0]*np.exp(aux[1]/(8.31*domain.initial_conditions["Temperature"]))
        self.value=value
        
    def set_external_bc_field(self, problem):
        value=0
        for domain in problem.domains:
            for edge in domain.boundary_conditions["External"]:
                if edge=="Right Edge" or "Left Edge":
                    inc=domain.mesh["dx"]
                    k=domain.material["Thermal Conductivity X"]
                if edge == "Bottom Edge" or "Top Edge":
                    inc=domain.mesh["dy"]
                    k=domain.material["Thermal Conductivity Y"]
                et= (- 2*inc*domain.boundary_conditions["External"][edge]["Convection Coefficient"]/k)*(domain.initial_conditions["Temperature"]-domain.boundary_conditions["External"][edge]["Room Temperature"])+domain.initial_conditions["Temperature"]
                if et<0:
                    et=0
                value = value + domain.mask_external_boundary[edge]*et
        self.value=value
        
    def set_internal_bc_field(self, problem):
        value=0
        for domain in problem.domains:
            for edge in domain.boundary_conditions["Internal"]:
                ic=1/(1+domain.boundary_conditions["Internal"][edge]["Horizontal asperity ratio"])
                value=value+domain.mask_contact_interface[edge]*ic
        self.value=value