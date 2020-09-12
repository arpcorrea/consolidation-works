from .domains import RectangularDomain
from .boundaryconditions import LinearBC


class TwoPlates:

    def __init__(self, deck):
        self.required_fields = ["Initial Temperature", "Thermal Conductivity X", "Thermal Conductivity Y", "Density",
                                "Specific Heat", "Input Power Density", "dx", "dy", "External Temperature"]
        self.set_simulation_parameters(deck)
        self.set_problem_parameters(deck)
        self.set_domains2(deck)
        self.set_initialconds(deck)
        # self.set_boundaryconds(deck)

    def set_simulation_parameters(self, deck):
        self.SimulationParameters = {}
        for par in deck.doc["Simulation"]:
            self.SimulationParameters[par] = deck.doc["Simulation"][par]

    def set_problem_parameters(self, deck):
        ny = 0
        t = 0
        for domain in deck.doc["Domains"]:
            ny = ny + int(deck.doc["Domains"][domain]["Mesh"]["Number of Elements in Y"])
            nx = int(deck.doc["Domains"][domain]["Mesh"]["Number of Elements in X"])
            t = t + float(deck.doc["Domains"][domain]["Geometry"]["Thickness (Y)"])

        self.totalNy = ny
        self.totalNx = nx
        self.total_thickness = t

    def set_domains2(self, deck):
        self.domains = []
        mesh = {}
        initialcond = {}
        material = {}
        boundarycond = {}
        bc_edge = {}

        for deck_domain in deck.doc["Domains"]:
            position = int(deck.doc["Domains"][deck_domain]["Geometry"]["Pos"])
            if position == 1:
                corner0 = (0, 0)
                corner1 = (float(deck.doc["Domains"][deck_domain]["Geometry"]["Width (X)"]),
                           float(deck.doc["Domains"][deck_domain]["Geometry"]["Thickness (Y)"]))
                ele_x0 = 0
                ele_x1 = int(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in X"])
                ele_y0 = 0
                ele_y1 = int(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in Y"]) - 1

            if position == 2:
                for domain_aux in deck.doc["Domains"]:
                    if deck.doc["Domains"][domain_aux]["Geometry"]["Pos"] == "1":
                        aux = float(deck.doc["Domains"][domain_aux]["Geometry"]["Thickness (Y)"])
                        auxeley = int(deck.doc["Domains"][domain_aux]["Mesh"]["Number of Elements in Y"])
                        corner0 = (0, aux)
                        corner1 = (float(deck.doc["Domains"][deck_domain]["Geometry"]["Width (X)"]),
                                   aux + float(deck.doc["Domains"][deck_domain]["Geometry"]["Thickness (Y)"]))
                        ele_x0 = 0
                        ele_x1 = int(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in X"])
                        ele_y0 = auxeley
                        ele_y1 = int(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in Y"]) + auxeley - 1

            if position == 3:
                corner0 = (
                    0, self.total_thickness - float(deck.doc["Domains"][deck_domain]["Geometry"]["Thickness (Y)"]))
                corner1 = (float(deck.doc["Domains"][deck_domain]["Geometry"]["Width (X)"]), self.total_thickness)
                ele_x0 = 0
                ele_x1 = int(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in X"])
                ele_y0 = int(self.totalNy) - int(
                    float(deck.doc["Domains"][deck_domain]["Mesh"]["Number of Elements in Y"]))
                ele_y1 = int(self.totalNy) - 1

            for material_prop in deck.doc["Domains"][deck_domain]["Material"]:
                material[material_prop] = float(deck.doc["Domains"][deck_domain]["Material"][material_prop])
            for initcond in deck.doc["Domains"][deck_domain]["Initial Condition"]:
                initialcond[initcond] = float(deck.doc["Domains"][deck_domain]["Initial Condition"][initcond])
            for mesh_dir in deck.doc["Domains"][deck_domain]["Mesh"]:
                mesh[mesh_dir] = int(deck.doc["Domains"][deck_domain]["Mesh"][mesh_dir])

            for bc in deck.doc["Domains"][deck_domain]["Boundary Condition"]:
                boundarycond[bc] = {}
                for edge in deck.doc["Domains"][deck_domain]["Boundary Condition"][bc]:
                    bc_edge[edge] = {}
                    for variable in deck.doc["Domains"][deck_domain]["Boundary Condition"][bc][edge]:
                        bc_edge[edge].update({variable: float(
                            deck.doc["Domains"][deck_domain]["Boundary Condition"][bc][edge][variable])})
                    boundarycond[bc].update({edge: bc_edge[edge]})

            self.domains.append(
                RectangularDomain(deck_domain, corner0, corner1, ele_x0, ele_x1, ele_y0, ele_y1, position, material,
                                  initialcond, boundarycond, mesh))

    def set_initialconds(self, deck):
        for domain in self.domains:
            for field in self.required_fields:
                if field in deck.doc["Domains"][domain.name]["Initial Condition"]:
                    domain.set_field_init_value(
                        {field: float(deck.doc["Domains"][domain.name]["Initial Condition"][field])})
                elif field in deck.doc["Domains"][domain.name]["Material"]:
                    domain.set_field_init_value({field: deck.doc["Domains"][domain.name]["Material"][field]})
                elif field == "dx":
                    # import pdb; pdb.set_trace()
                    domain.set_field_init_value({field: domain.Lx / domain.mesh["Number of Elements in X"]})
                elif field == "dy":
                    domain.set_field_init_value({field: domain.Ly / domain.mesh["Number of Elements in Y"]})
