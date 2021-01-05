# -*- coding: utf-8 -*-
import numpy as np
from .fields import Field

class Mesher():

    def __init__(self,  problem):
        # self.totalNx = problem.totalpx
        # self.totalNy = problem.totalpy
        self.set_fields(problem)
        self.set_fields_visc(problem)

    def set_fields(self, problem):
        self.fields=[]
        for field_name in problem.required_fields:
            if field_name == "Viscosity":
                continue
            else:
                field_value=0
                for domain in problem.domains:
                    field_value = field_value + domain.local_fields[field_name]
                self.fields.append(Field(field_name, field_value))
                if field_name== "Temperature":
                    self.fields.append(Field("Toldold", field_value))
                



    def set_fields_visc(self, problem):
        if "Viscosity" in problem.required_fields:
            visc_param ={}
            for domain in problem.domains:
                for parameter in domain.local_fields["Viscosity"].keys():
                    if parameter not in visc_param:
                        visc_param[parameter] = domain.local_fields["Viscosity"][parameter]
                    else:
                        visc_param[parameter] = visc_param[parameter] + domain.local_fields["Viscosity"][parameter]
            self.fields.append(Field("Viscosity", visc_param ))

