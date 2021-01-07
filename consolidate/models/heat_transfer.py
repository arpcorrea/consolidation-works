import numpy as np

class HeatTransfer:

    def __init__(self, mesh, problem):
        fields ={}
        for aux in mesh.fields:
            fields[aux.name]= aux.value
            # import pdb; pdb.set_trace()
            
        self.dx = fields["increments"]["dx"]
        self.dy = fields["increments"]["dy"]
        self.dx2 = self.dx*self.dx
        self.dy2 = self.dy*self.dy
        
        self.dt = float(problem.SimulationParameters["Step Time"])

        self.rho = fields["Density"]
        self.cp = fields["Thermal"]["Cp"]
        self.kx = fields["Thermal"]["kx"]
        self.ky = fields["Thermal"]["ky"]
        
        self.A = fields["Viscosity"]["A"]
        self.Ea = fields["Viscosity"]["Ea"]
        self.Tg = fields["Viscosity"]["Tg"]
        
        self.Q = fields["Power Input Heat"]
        self.h = fields ["Convection Coefficient"]
        self.Text = fields["Interface Temperature"]

        self.calc_diffusivity(self.kx, self.ky, self.rho, self.cp)
        self.calc_w(self.diffx, self.diffy, self.dx2, self.dy2)
        self.calc_disc(self.ky)


    def calc_diffusivity(self, kx, ky, rho, cp):
        self.diffy = np.zeros(np.shape(ky))
        self.diffx = np.zeros(np.shape(kx))
        self.diffy[1:-1, 1:-1] = ky[1:-1, 1:-1]/(rho[1:-1, 1:-1]*cp[1:-1, 1:-1])
        self.diffx[1:-1, 1:-1] = kx[1:-1, 1:-1]/(rho[1:-1, 1:-1]*cp[1:-1, 1:-1])

    def calc_w(self, diffx,diffy,dx2,dy2):
        self.wx = np.zeros(np.shape(diffx))
        self.wy = np.zeros(np.shape(diffx))
        self.wy[1:-1, 1:-1] = diffy[1:-1, 1:-1]/dy2[1:-1, 1:-1]
        self.wx[1:-1, 1:-1] = diffx[1:-1, 1:-1]/dx2[1:-1, 1:-1]


    def calc_disc(self, ky):
        k=[]
        disc=[]
        for i in range (1, np.shape(ky)[0]-2):
            if self.ky[i, 1] != ky[i+1, 1]:
                k.append( self.ky[i,1]/ky[i+1, 1])
                disc.append(i)

        gamma =[]
        for i in range (0, np.size(disc)):
            gamma.append((k[i]-1)/(k[i]+1))

        self.gamma = gamma
        self.disc = disc
        self.k = k


    def do_timestep_cond_conv(self, uu,uuold):

        
        uu[0,1:-1] = 2*self.Text[0,1:-1] - uuold[1,1:-1]
        uu[-1,1:-1] = 2*self.Text[-1,1:-1] - uuold[-2,1:-1]
        uu[1:-1,0] = 2*self.Text[1:-1,0] - uuold[1:-1,1]
        uu[1:-1,-1] = 2*self.Text[1:-1,-1] - uuold[1:-1,-2]


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


        uunodes = np.zeros((np.shape(uu)[0]-1, np.shape(uu)[1]-1))
        uunodes[:,:] = (uu[:-1, :-1] + uu[1:, 1:]+ uu[1:, :-1] + uu[:-1, 1:])/4
        uunodes[0,0] = (uunodes[0,1]+uunodes[1,0])/2
        uunodes[-1,-1] = (uunodes[-1,-2]+uunodes[-2,-1])/2
        uunodes[0,-1] = (uunodes[0,-2]+uunodes[1,-1])/2
        uunodes[-1,0] = (uunodes[-2,0]+uunodes[-1,1])/2

        return uu,uunodes

    def do_timestep_viscosity(self, uu):
        print("do something here")



