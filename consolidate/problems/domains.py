import numpy as np


class RectangularDomain:

    def __init__(self, name, corner0: tuple, corner1, ex0, ex1, ey0, ey1, position, material,
                 initialcondition, boundarycond, mesh):
        # Rectangular domain boundaries
        self.x0 = float(corner0[0])
        self.y0 = float(corner0[1])
        self.x1 = float(corner1[0])
        self.y1 = float(corner1[1])
        # Lengths
        self.Lx = self.x1 - self.x0
        self.Ly = self.y1 - self.y0
        self.name = name
        self.material = material.copy()
        self.mesh = mesh.copy()
        self.initial_fields = initialcondition.copy()
        self.ex0 = ex0
        self.ex1 = ex1
        self.ey0 = ey0
        self.ey1 = ey1
        self.boundary_fields = boundarycond.copy()
        self.position = position
        # import pdb; pdb.set_trace()

    def test(self, point) -> bool:
        """
        Returns True if (Point[0], Point[1]) is on or within the rectangular domain boundary,
        False otherwise.

        :param point: (x-coordinate, y-coordinate)
        :return: bool
        """

        if self.x0 <= point[0] <= self.x1 and self.y0 <= point[1] <= self.y1:
            return True
        return False

    def test_mesh(self, mesh) -> bool:
        """
        Returns True if (mesh[0], mesh[1]) is on or within the rectangular domain boundary
        defined by (self.ey0, self.ey1, self.ex0, self.ex1), False otherwise.

        :param mesh:
        :return: bool
        """
        # import pdb; pdb.set_trace()
        if self.ey0 <= mesh[0] <= self.ey1 and self.ex0 <= mesh[1] <= self.ex1:
            # import pdb; pdb.set_trace()
            return True

        return False

    def set_field_init_value(self, field_dict):
        for key, value in field_dict.items():
            self.initial_fields[key] = float(value)

    def generate_mask(self, totalNy, totalNx):
        m = np.zeros((totalNy, totalNx))
        maux = np.zeros((totalNy + 2, totalNx + 2))
        self.mask = m.copy()
        self.mask_external_boundary = {}
        self.mask_contact_interface = {}
        mask_left = maux.copy()
        mask_right = maux.copy()
        mask_top = maux.copy()
        mask_bottom = maux.copy()
        contact_mask = m.copy()
        contact_mask_middle_top = m.copy()
        contact_mask_middle_bottom = m.copy()
        for x_i in range(0, np.shape(m)[0]):
            for y_i in range(0, np.shape(m)[1]):
                if self.test_mesh((x_i, y_i)):
                    self.mask[x_i][y_i] = 1
                    mask_left[x_i + 1][0] = 1
                    mask_right[x_i + 1][-1] = 1
                    self.mask_external_boundary.update({"Left Edge": mask_left})
                    self.mask_external_boundary.update({"Right Edge": mask_right})

                    if self.position == 1:
                        mask_bottom[self.ey0][y_i + 1] = 1
                        contact_mask[self.ey1][y_i] = 1
                        self.mask_external_boundary.update({"Bottom Edge": mask_bottom})
                        self.mask_contact_interface.update({"Top Edge": contact_mask})
                    if self.position == 3:
                        mask_top[-1][y_i + 1] = 1
                        self.mask_external_boundary.update({"Top Edge": mask_top})
                        contact_mask[self.ey0][y_i] = 1
                        self.mask_contact_interface.update({"Bottom Edge": contact_mask})
                    if self.position == 2:
                        contact_mask_middle_bottom[self.ey0][y_i] = 1
                        contact_mask_middle_top[self.ey1][y_i] = 1
                        self.mask_contact_interface.update({"Bottom Edge": contact_mask_middle_bottom})
                        self.mask_contact_interface.update({"Top Edge": contact_mask_middle_top})
