import numpy as np
class RectangularDomain:

    def __init__(self, name,x0,x1,y0,y1, nodes, power):
        self.name = name
        self.dimensions =  [[x0,x1],[y0,y1]]
        self.nodes = nodes
        self.material = {}
        self.initial_condition = {}
        self.boundary_condition = {}
        self.power = power
        self.local_fields={}
        
        


        
    def test_grid_inter_nodes(self, mesh):
        if mesh[0] >= self.nodes[1][0] and mesh[0] <= self.nodes[1][1]-1 and mesh[1] >= self.nodes[0][0] and mesh[1]<= self.nodes[0][1]-1:
            return True
        else:
             return False
         


    def generate_mask(self, i, totalpy, totalpx, total_thickness):

        self.mask_out = {}
        self.mask_inter_nodes ={}


        # if N nodes, it creates N-1 internodes. Adding +1, creates 2 out-of-doomain phantom nodes
        minterphanton = np.zeros((totalpy+1, totalpx+1))



        mask_out_top =  minterphanton.copy()
        mask_out_bottom = minterphanton.copy()
        mask_out_left = minterphanton.copy()
        mask_out_right = minterphanton.copy()




        for x_i in range (0,np.shape(minterphanton)[0]):
            for y_i in range (0,np.shape(minterphanton)[1]):
                if self.test_grid_inter_nodes( (x_i, y_i)):
                    minterphanton[x_i+1][y_i+1] = 1
                    mask_out_left[x_i+1][0] = 1
                    mask_out_right[x_i+1][-1] = 1
                    mask_out_bottom[self.nodes[1][0]][y_i+1] = 1
                    mask_out_top[self.nodes[1][1]+1][y_i+1] = 1
        # import pdb; pdb.set_trace()
                    
        self.mask_inter_nodes["Inner"] = minterphanton
        self.mask_inter_nodes["Right Edge"] = mask_out_right.copy()
        self.mask_inter_nodes["Left Edge"] = mask_out_left.copy()
        
        if self.nodes[1][0] == 0:
            self.mask_inter_nodes["Bottom Edge"] = mask_out_bottom.copy()
            return

        if self.nodes[1][1] == totalpy-1:
            self.mask_inter_nodes["Top Edge"] = mask_out_top.copy()
            return




    def set_field(self, field_name, value):
        self.local_fields.update({field_name: value})

    def set_points_domains(self, p_x0, p_x1, p_y0, p_y1):
        self.px = [p_x0, p_x1]
        self.py = [p_y0, p_y1]

    def set_material(self,material):
        self.material.update(material)

    def set_bc(self, bc):
        self.boundary_condition.update(bc)

    def set_power(self, power):
        self.power.update(power)

    def set_initial_cond(self, init_cond):
        self.initial_condition.update(init_cond)
