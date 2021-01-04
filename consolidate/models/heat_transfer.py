import numpy as np

class HeatTransfer:

    def __init__(self, mesh, problem):
        fields ={}
        for aux in mesh.fields:
            fields[aux.name]= aux.value
        self.dt = float(problem.SimulationParameters["Step Time"])
        self.dx = fields["dx"]
        self.dy = fields["dy"]
        self.dx2 = fields["dx"] * fields["dx"]
        self.dy2 = fields["dy"] * fields["dy"]
        self.rho = fields["Density"]
        self.cp = fields["Cp"]
        self.kx = fields["kx"]
        self.ky = fields["ky"]
        self.Q = fields["Power Input Heat"]
        self.h = fields ["Convection Coefficient"]
        self.Text = fields["Interface Temperature"]
        self.calc_diffusivity()
        
        

    def calc_diffusivity(self):
        self.diffy = self.ky/(self.rho*self.cp)
        self.diffx = self.kx/(self.rho*self.cp)
        self.wy = self.diffy/self.dy2
        self.wx = self.diffx/self.dx2
        
        k=[]
        disc=[]
        for i in range (1, np.shape(self.ky)[0]-2):
            if self.ky[i, 1] != self.ky[i+1, 1]:
                k.append( self.ky[i,1]/self.ky[i+1, 1])
                disc.append(i)
                
        self.disc = disc
        self.k = k
        
        gamma =[]
        for i in range (0, np.size(self.disc)):
            gamma.append((self.k[i]-1)/(self.k[i]+1))
        self.gamma = gamma


    def do_timestep_cond_conv(self, uu,uuold, uunodes):
        
        # ---------------------------------------------------------------------------------------------------------
        # -- ORDER 1 SOLVER --
        # import pdb; pdb.set_trace()
        
        # dU/dy = (uuold[2:,1:-1] - uuold[0:-2,1:-1]])/deltaY
        

        

        
        uu[0,1:-1] = 2*self.Text[0,1:-1] - uuold[1,1:-1]
        uu[-1,1:-1] = 2*self.Text[-1,1:-1] - uuold[-2,1:-1]
        uu[1:-1,0] = 2*self.Text[1:-1,0] - uuold[1:-1,1]
        uu[1:-1,-1] = 2*self.Text[1:-1,-1] - uuold[1:-1,-2]
        # import pdb; pdb.set_trace()
        
        # uu[-1,1:-1] = uu[-1,1:-1] - 2*self.dy[1,1:-1]*self.h[-1,1:-1]*(uu[-1,1:-1] - uu[-2,1:-1])/self.ky[-2,1:-1]
        # uu[1:-1,0] = uu[1:-1,0] - 2*self.dx[:-1,1]*self.h[1:-1,0]*(uu[1:-1,0] - uu[1:-1,1])/self.kx[1:-1,1] 
        # uu[1:-1,-1] = uu[1:-1,-1] - 2*self.dx[:-1,-2]*self.h[1:-1,-1]*(uu[1:-1,-1] - uu[1:-1,-2])/self.kx[1:-1,-2]
        

        
        # uu[1:-1, 1:-1] = uuold[1:-1, 1:-1] + self.dt*((self.diffy[1:-1, 1:-1])/self.dy2[1:, :-1])*(uuold[2:, 1:-1]-uuold[1:-1, 1:-1]) - self.dt*((self.diffy[1:-1, 1:-1])/self.dy2[:-1, :-1])*(uuold[1:-1, 1:-1]-uuold[:-2, 1:-1]) + self.dt*((self.diffx[1:-1, 1:-1])/self.dx2[1:, :-1])*(uuold[1:-1, 2:]-uuold[1:-1, 1:-1]) - self.dt*((self.diffx[1:-1, 1:-1])/self.dx2[:-1, :-1])*(uuold[1:-1, 1:-1]-uuold[1:-1, :-2])
        # in Y only
        # import pdb; pdb.set_trace()

        if not self.disc:
            uu[1:-1, 1:-1] = uuold[1:-1, 1:-1] + self.dt*(self.wy[1:-1, 1:-1])*(uuold[2:, 1:-1]-2*uuold[1:-1, 1:-1] + uuold[:-2,1:-1]) + self.dt*(self.wx[1:-1, 1:-1])*(uuold[1:-1, 2:]-2*uuold[1:-1, 1:-1] + uuold[1:-1, :-2])
        else:
            for i in range(0, np.size(self.disc)):
                uu[self.disc[i], 1:-1] = uuold[self.disc[i], 1:-1] + self.dt * self.wy[self.disc[i], 1:-1] * (uuold[self.disc[i]-1, 1:-1] - (2-self.gamma[i]) * uuold[self.disc[i], 1:-1] + 2/(self.k[i] +1) * uuold[self.disc[i]+1, 1:-1])  + self.dt*(self.wx[self.disc[i], 1:-1])*(uuold[self.disc[i], 2:]-2*uuold[self.disc[i], 1:-1] + uuold[self.disc[i], :-2])
                uu[self.disc[i]+1, 1:-1] = uuold[self.disc[i]+1, 1:-1] + self.dt * self.wy[self.disc[i]+1, 1:-1] * (2*self.k[i]/(self.k[i]+1) * uuold[self.disc[i], 1:-1] - (2+self.gamma[i])*uuold[self.disc[i]+1, 1:-1] + uuold[self.disc[i]+2, 1:-1]) + self.dt*(self.wx[self.disc[i]+1, 1:-1])*(uuold[self.disc[i]+1, 2:]-2*uuold[self.disc[i]+1, 1:-1] + uuold[self.disc[i]+1, :-2])
                if i == 0:
                    uu[1:self.disc[i], 1:-1] = uuold[1:self.disc[i], 1:-1] + self.dt * self.wy[1:self.disc[i], 1:-1] * (uuold[2:self.disc[i]+1, 1:-1] - 2*uuold[1:self.disc[i], 1:-1] + uuold[0:self.disc[i]-1, 1:-1]) + self.dt*(self.wx[1:self.disc[i], 1:-1])*(uuold[1:self.disc[i], 2:]-2*uuold[1:self.disc[i], 1:-1] + uuold[1:self.disc[i], :-2])
                    uu[self.disc[i]+2 : self.disc[i+1], 1:-1] = uuold[self.disc[i]+2 : self.disc[i+1], 1:-1] + self.dt * self.wy[self.disc[i]+2 : self.disc[i+1], 1:-1] * (uuold[self.disc[i]+3 : self.disc[i+1]+1, 1:-1] - 2*uuold[self.disc[i]+2 : self.disc[i+1], 1:-1] + uuold[self.disc[i]+1 : self.disc[i+1]-1, 1:-1]) + self.dt*(self.wx[self.disc[i]+2 : self.disc[i+1], 1:-1])*(uuold[self.disc[i]+2 : self.disc[i+1], 2:]-2*uuold[self.disc[i]+2 : self.disc[i+1], 1:-1] + uuold[self.disc[i]+2 : self.disc[i+1], :-2])

                elif i == np.size(self.disc) -1:
                    uu[self.disc[i]+2 : -1, 1:-1] = uuold[self.disc[i]+2 : -1, 1:-1] + self.dt * self.wy[self.disc[i]+2 : -1, 1:-1] * (uuold[self.disc[i]+3 : , 1:-1] - 2*uuold[self.disc[i]+2 : -1, 1:-1] + uuold[self.disc[i]+1 : -2, 1:-1]) + self.dt*(self.wx[self.disc[i]+2 : -1, 1:-1])*(uuold[self.disc[i]+2 : -1, 2:]-2*uuold[self.disc[i]+2 : -1, 1:-1] + uuold[self.disc[i]+2 : -1, :-2])

                else:
                    uu[self.disc[i-1]+2: self.disc[i], 1:-1] = uuold[self.disc[i-1]+2: self.disc[i], 1:-1] + self.dt * self.wy[self.disc[i-1]+2: self.disc[i], 1:-1] * (uuold[self.disc[i-1]+3: self.disc[i]+1, 1:-1] - 2*uuold[self.disc[i-1]+2: self.disc[i], 1:-1] + uuold[self.disc[i-1]+1: self.disc[i]-1, 1:-1]) + self.dt*(self.wx[self.disc[i-1]+2: self.disc[i], 1:-1])*(uuold[self.disc[i-1]+2: self.disc[i], 2:]-2*uuold[self.disc[i-1]+2: self.disc[i], 1:-1] + uuold[self.disc[i-1]+2: self.disc[i], :-2])

        
        
        uunodes[:,:] = (uu[:-1, :-1] + uu[1:, 1:]+ uu[1:, :-1] + uu[:-1, 1:])/4
        uunodes[0,0] = (uunodes[0,1]+uunodes[1,0])/2
        uunodes[-1,-1] = (uunodes[-1,-2]+uunodes[-2,-1])/2
        uunodes[0,-1] = (uunodes[0,-2]+uunodes[1,-1])/2
        uunodes[-1,0] = (uunodes[-2,0]+uunodes[-1,1])/2

        return uu,uunodes





