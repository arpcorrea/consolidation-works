# -*- coding: utf-8 -*-
import numpy as np
from .fields import Field

class Mesher():

    def __init__(self,  problem):
        self.set_fields(problem)

    def set_fields(self, problem):
        self.fields=[]
        for field_name in problem.required_fields:
            if isinstance (problem.domains[0].local_fields[field_name], dict):
                aux ={}
                for domain in problem.domains:
                        for variable in domain.local_fields[field_name].keys():
                            if variable not in aux:
                                aux[variable] = domain.local_fields[field_name][variable]
                            else:
                                aux[variable] = aux[variable] + domain.local_fields[field_name][variable]
                self.fields.append(Field(field_name, aux ))
            else:
                aux=0
                for domain in problem.domains:
                    aux = aux + domain.local_fields[field_name]
                self.fields.append(Field(field_name, aux ))