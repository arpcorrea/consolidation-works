# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 11:38:36 2020

@author: andre
"""


class Geometry:
    def __init__(self, deck):
        self.deck = deck
        self.geometry()

    def geometry(self):
        self.Lx = float(self.deck.doc["Geometry"]["Length X"])
        self.Ly = float(self.deck.doc["Geometry"]["Length Y"])
