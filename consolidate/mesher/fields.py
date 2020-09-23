# import numpy as np
import numpy as np

            
class Field:
    
    def __init__(self, field, problem):
        self.field=field
        self.set_field(field, problem)

    def set_field(self, field, problem):
        value=0
        for domain in problem.domains:
            # import pdb; pdb.set_trace()
            if field in domain.initial_fields:
                value = value + domain.mask * domain.initial_fields[field]
            if field in domain.external_boundary_fields:
                for edge in domain.external_boundary_fields[field]:
                    for variable in domain.external_boundary_fields[field][edge]:
                        value=value+domain.mask_external_boundary[edge]*float(domain.external_boundary_fields[field][edge][variable])
        self.value=value
