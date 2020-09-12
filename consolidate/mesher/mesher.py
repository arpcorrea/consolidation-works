# -*- coding: utf-8 -*-
import numpy as np
from .mesh import Mesh
from .fields import Field


class Mesher():

    def __init__(self, problem):
        self.fields = []
        self.meshes = []
        self.totalNx = problem.totalNx
        self.totalNy = problem.totalNy
        self.create_masks(problem)
        self.set_intial_condition_fields(problem)

    def create_masks(self, problem):
        for domain in problem.domains:
            self.meshes.append(Mesh(domain, self.totalNx, self.totalNy))

    def set_intial_condition_fields(self, problem):
        for fields in problem.required_fields:
            self.fields.append(Field(fields, problem))
