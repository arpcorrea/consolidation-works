# -*- coding: utf-8 -*-
import numpy as np
from .mesh import Mesh
from .fields import Field

class Mesher():

    def __init__(self,  problem):
        self.totalNx = problem.totalNx
        self.totalNy = problem.totalNy
        self.create_masks(problem)
        self.fields=[]
        self.set_fields_ic(problem)
        self.set_fields_material(problem)
        self.set_fields_external_bc(problem)
        self.set_fields_internal_bc(problem)

    def create_masks(self, problem):
        self.meshes=[]
        for domain in problem.domains:
            self.meshes.append(Mesh( domain, self.totalNx, self.totalNy))
            
    def set_fields_ic(self, problem):
        count=np.size(self.fields)
        for field in set(problem.domains[0].initial_conditions) & set(problem.domains[1].initial_conditions) & set(problem.domains[2].initial_conditions):
            self.fields.append(Field(field))
        for i in range(count, np.size(self.fields)):
            self.fields[i].set_initial_conditions_field(problem)
            
    def set_fields_material(self,problem):
        count=np.size(self.fields)
        for field in set(problem.domains[0].material) & set(problem.domains[1].material) & set(problem.domains[2].material):
            self.fields.append(Field(field))
        for i in range(count, np.size(self.fields)):
            self.fields[i].set_material_field(problem)
            
    def set_fields_external_bc(self,problem):
        count = np.size(self.fields)
        self.fields.append(Field("Equivalente External Temperature"))
        for i in range (count, np.size(self.fields)):
            self.fields[i].set_external_bc_field(problem)
                
    def set_fields_internal_bc(self, problem):
        count = np.size(self.fields)
        self.fields.append(Field("Intimate Contact"))
        for i in range (count, np.size(self.fields)):
            self.fields[i].set_internal_bc_field(problem)