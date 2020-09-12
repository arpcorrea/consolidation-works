# -*- coding: utf-8 -*-
import numpy as np


class SolvesTwoPlates:

    def __init__(self, deck, model_HT, meshes, plots):
        self.deck = deck
        # Compute the TEMPERATURE for each node
        self.model_HT = model_HT
        self.meshes = meshes
        self.plots = plots
        self.do_solver()

    def do_solver(self):
        for m in range(int(self.deck.doc["Simulation"]["Number Time Steps"])):
            # -------------- CALCULATE TEMPERATURE FOR EACH STEP INCREMENT----------
            # self.A=self.model_HT.convection(self.meshes.T0, self.meshes.T, self.meshes.DiffTotalX, self.meshes.DiffTotalY)
            self.meshes.T0, self.meshes.T = self.model_HT.do_timestep(self.meshes.T0, self.meshes.T,
                                                                      self.meshes.DiffTotalX, self.meshes.DiffTotalY,
                                                                      self.meshes.Q)
            # -------------- FORCE TEMPERATURE AT THE INTERFACE: ISOTHERMAL CONDITION----------
            # -------------- UPDATE T0----------
            self.meshes.T0 = self.meshes.T.copy()

            # -------------- DO PLOT ACCORDING TO THE SELECTED INTERVAL----------
            if m in self.plots.mfig:
                self.plots.update_T(self.meshes.T)
                self.plots.do_plots(m)
        self.plots.do_animation()
