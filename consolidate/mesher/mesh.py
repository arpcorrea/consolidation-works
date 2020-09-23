import numpy as np

class Mesh:

    def __init__(self,  domain, totalNx=0, totalNy=0):
        self.set_mesh_grid(domain)
        self.name = domain.name
        if totalNx !=0 and totalNy !=0:
            self.set_create_mask(domain, totalNy, totalNx)

    def set_mesh_grid(self, domain):
        self.nx = domain.mesh["Number of Elements in X"]
        self.ny = domain.mesh["Number of Elements in Y"]
        self.dx=domain.dimensions["Lx"]/self.nx
        self.dy=domain.dimensions["Ly"]/self.ny
        X, Y = np.meshgrid(np.arange(domain.corners["X"][0], domain.corners["X"][1], self.dx), np.arange(domain.corners["Y"][0], domain.corners["Y"][1], + self.dy))
        X=X[0,:].copy()
        Y=Y[:,0].copy()
        self.X = X
        self.Y = Y

    def set_create_mask(self, domain, totalNy, totalNx):
        M=np.zeros((totalNy, totalNx))
        domain.generate_mask(totalNy,totalNx)
        initialmask=domain.mask
        self.mask=initialmask