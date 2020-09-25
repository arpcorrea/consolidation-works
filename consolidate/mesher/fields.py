# import numpy as np
import numpy as np

            
class Field:
    
    def __init__(self, field, problem):
        self.field=field
        self.set_field(field, problem)

    def set_field(self, field, problem):
        value=0
        for domain in problem.domains:
            if field in domain.initial_condition:
                value = value + domain.mask * domain.initial_condition[field]
            for location in domain.boundary_condition:
                if field in domain.boundary_condition[location]:
                    for edge in domain.boundary_condition[location][field]:
                        if location == "External":
                            value=value+domain.mask_external_boundary[edge]*float(domain.boundary_condition[location][field][edge])
                        else:
                            value=value + domain.mask_contact_interface[edge]*float(domain.boundary_condition[location][field][edge])
        self.value=value
