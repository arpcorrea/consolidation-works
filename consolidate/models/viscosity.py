# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 08:38:50 2020

@author: andre
"""


class ViscosityCalculation:
    def __init__(self, problem, mesh):
        param =[]
        ea=0
        a=0
        for domain in problem.domains:
            for prop in domain.material:
                if prop == "Viscosity":
                    aux=[]
                    for param in domain.material[prop]:
                        aux.append(domain.material[prop][param])
            a= a + aux[0]*domain.mask_inter_nodes["Inner"]
            ea = ea + aux[1]*domain.mask_inter_nodes["Inner"]
        self.a = a
        self.ea= ea

    def do_timestep_viscosity(self,uu,temp):
        uu = self.a*np.exp(self.ea/temp)
        return uu