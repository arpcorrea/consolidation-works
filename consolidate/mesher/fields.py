# numpy is not used
import numpy as np


class Field:

    def __init__(self, field, problem):
        self.field = field
        self.set_field(field, problem)

    def set_field(self, field, problem):
        value = 0
        for domain in problem.domains:
            if field in domain.initial_fields:
                value = value + domain.mask * domain.initial_fields[field]
            if field == "External Temperature":
                for edge in domain.boundary_fields[field]:
                    value = value + domain.mask_external_boundary[edge] * float(
                        domain.boundary_fields[field][edge]["Temperature"])
        self.value = value
