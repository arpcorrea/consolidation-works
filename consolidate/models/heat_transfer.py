class HeatTransfer:

    def __init__(self, deck, meshes):
        self.dt = float(deck.doc["Simulation"]["Time Step"])
        self.dx2 = meshes.dx * meshes.dx
        self.dy2 = meshes.dy * meshes.dy
        self.rho = meshes.RhoTotal
        self.cp = meshes.CpTotal
        self.k = meshes.KtotalX

    # -------------- BEGIN HEAT TRANSFER CALCULATION----------
    def do_timestep(self, u0, u, Diffx, Diffy, Q):
        # Propagate with forward-difference in time, central-difference in space
        u[1:-1, 1:-1] = u0[1:-1, 1:-1] + Diffy[1:-1, 1:-1] * self.dt * \
                        ((u0[2:, 1:-1] - 2 * u0[1:-1, 1:-1] + u0[:-2, 1:-1]) / self.dy2) + \
                        Diffx[1:-1, 1:-1] * self.dt * ((u0[1:-1, 2:] - 2 * u0[1:-1, 1:-1] + u0[1:-1, :-2]) / self.dx2) \
                        + self.dt * Q[1:-1, 1:-1] / (self.cp[1:-1, 1:-1] * self.rho[1:-1, 1:-1])

        u0 = u.copy()

        return u0, u

# -------------- END HEAT TRANSFER CALCULATION----------
