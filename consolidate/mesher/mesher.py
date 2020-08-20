# -*- coding: utf-8 -*-
import numpy as np
from .mesh import Mesh
from .fields import Field

class Mesher():

    def __init__(self,  problem):
        self.mesh_domains( problem)
        self.initialize_fields(problem)

    def mesh_domains(self, problem):
        self.meshes = {}
        X = []
        Y = []
        for domain in problem.domains:
            self.meshes[domain.name] = ( Mesh(domain) )
            for elem in self.meshes[domain.name].X:
                X.append(elem)
            for elem in self.meshes[domain.name].Y:
                Y.append(elem)
        X.sort() ; Y.sort()
        self.X = list(set(X))
        self.Y = list(set(Y))
        self.M = np.zeros( (len(self.X), len(self.Y)) )
        

    def initialize_fields(self, problem):
        self.fields = {}
        for field_ in problem.required_fields:
            self.fields[field_] = Field(field_, self.M, problem)
        import pdb; pdb.set_trace()
