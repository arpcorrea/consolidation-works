# -*- coding: utf-8 -*-
import numpy as np
from .mesh import Mesh
from .fields import Field

class Mesher():

    def __init__(self,  problem):
        self.totalNx = problem.totalNx
        self.totalNy = problem.totalNy
        self.create_masks(problem)
        self.set_intial_condition_fields(problem)

    def create_masks(self, problem):
        self.meshes=[]
        for domain in problem.domains:
            self.meshes.append(Mesh( domain, self.totalNx, self.totalNy))

    def set_intial_condition_fields(self, problem):
        self.fields=[]
        for fields in set(problem.domains[0].initial_condition) & set(problem.domains[1].initial_condition) & set(problem.domains[2].initial_condition):
            self.fields.append(Field(fields, problem)) 
        for location in set(problem.domains[0].boundary_condition) & set(problem.domains[1].boundary_condition) & set(problem.domains[2].boundary_condition):
            for fields in set(problem.domains[0].boundary_condition[location]) & set(problem.domains[1].boundary_condition[location]) & set(problem.domains[2].boundary_condition[location]):
                self.fields.append(Field(fields, problem))