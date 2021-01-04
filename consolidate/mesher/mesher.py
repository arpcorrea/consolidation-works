# -*- coding: utf-8 -*-
import numpy as np
from .fields import Field

class Mesher():

    def __init__(self,  problem):
        # self.totalNx = problem.totalpx
        # self.totalNy = problem.totalpy
        self.set_fields(problem)

    def set_fields(self, problem):
        self.fields=[]
        for field_name in problem.required_fields:
            field_value=0
            for domain in problem.domains:
                field_value = field_value + domain.local_fields[field_name]
            self.fields.append(Field(field_name, field_value))
            if field_name== "Temperature":
                self.fields.append(Field("Toldold", field_value))
                
