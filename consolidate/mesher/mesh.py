import numpy as np

class Mesh:

    def __init__(self,  domain):
        self.set_mesh_grid(domain)
        self.name = domain.name

    def set_mesh_grid(self, domain):
        self.nx = domain.Number_of_Elements_in_X
        self.ny = domain.Number_of_Elements_in_Y
        self.dx=domain.Lx/self.nx
        self.dy=domain.Ly/self.ny
        X, Y = np.meshgrid(np.arange(domain.x0, domain.x1, self.dx), np.arange(domain.y0, domain.y1, + self.dy))
        X=X[0,:].copy()
        Y=Y[:,0].copy()
        self.X = X
        self.Y = Y
        self.M=np.zeros((domain.Number_of_Elements_in_X,domain.Number_of_Elements_in_Y))