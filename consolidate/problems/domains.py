import numpy as np
class RectangularDomain:

    def __init__(self, name, ex0, ex1, ey0, ey1, position,):
        self.elements = {"Elements in X":[ex0, ex1], "Elements in Y": [ey0,ey1]}
        self.name = name
        self.position = position

    def test_mesh(self, mesh):
        if mesh[0] >= self.elements["Elements in Y"][0] and mesh[0] <= self.elements["Elements in Y"][1] and mesh[1] >= self.elements["Elements in X"][0] and mesh[1]<= self.elements["Elements in X"][1]:
            return True
        else:
            return False


    

    def generate_mask(self, totalNy, totalNx):
        m=np.zeros((totalNy, totalNx))
        maux=np.zeros((totalNy+2, totalNx+2))
        self.mask = m.copy()
        self.mask_external_boundary={}
        self.mask_contact_interface={}
        mask_left= maux.copy()
        mask_right= maux.copy()
        mask_top= maux.copy()
        mask_bottom= maux.copy()
        contact_mask=m.copy()
        contact_mask_middle_top = m.copy()
        contact_mask_middle_bottom = m.copy()
        for x_i in range (0,np.shape(m)[0]):
            for y_i in range (0,np.shape(m)[1]):
                if self.test_mesh( (x_i, y_i) ):
                    self.mask[x_i][y_i] = 1
                    mask_left[x_i+1][0]=1
                    mask_right[x_i+1][-1]=1
                    self.mask_external_boundary.update({"Left Edge":mask_left})
                    self.mask_external_boundary.update({"Right Edge":mask_right})
                    
                    if self.position ==1:
                        mask_bottom[self.elements["Elements in Y"][0]][y_i+1]=1
                        contact_mask[self.elements["Elements in Y"][1]][y_i] = 1
                        self.mask_external_boundary.update({"Bottom Edge": mask_bottom})
                        self.mask_contact_interface.update({"Top Edge": contact_mask})
                    if self.position ==3:
                        mask_top[-1][y_i+1]=1
                        self.mask_external_boundary.update({"Top Edge": mask_top})
                        contact_mask[self.elements["Elements in Y"][0]][y_i] = 1
                        self.mask_contact_interface.update({"Bottom Edge": contact_mask})
                    if self.position ==2:
                        contact_mask_middle_bottom[self.elements["Elements in Y"][0]][y_i] = 1
                        contact_mask_middle_top[self.elements["Elements in Y"][1]][y_i] = 1
                        self.mask_contact_interface.update({"Bottom Edge": contact_mask_middle_bottom})
                        self.mask_contact_interface.update({"Top Edge": contact_mask_middle_top})
                        
    
    def set_corners(self, domain_name, deck):
        # import pdb; 
        position = int(deck.doc["Domains"][domain_name]["Geometry"]["Pos"])
        
        if position == 1:
             corner0 = (0, 0)
             corner1 = (float(deck.doc["Domains"][domain_name]["Geometry"]["Width (X)"]), float(deck.doc["Domains"][domain_name]["Geometry"]["Thickness (Y)"]))
        if position == 2:
            for domain_aux in deck.doc["Domains"]:
                if deck.doc["Domains"][domain_aux]["Geometry"]["Pos"] == "1":
                    aux=float(deck.doc["Domains"][domain_aux]["Geometry"]["Thickness (Y)"])
                    corner0=(0, aux)
                    corner1 = (float(deck.doc["Domains"][domain_name]["Geometry"]["Width (X)"]), aux + float(deck.doc["Domains"][domain_name]["Geometry"]["Thickness (Y)"]))
        if position == 3:
            aux=0
            for domain_aux in deck.doc["Domains"]:
                if domain_aux != domain_name:
                    aux=aux+float(deck.doc["Domains"][domain_aux]["Geometry"]["Thickness (Y)"])
            corner0 = (0, aux)
            corner1 = (float(deck.doc["Domains"][domain_name]["Geometry"]["Width (X)"]), aux + float(deck.doc["Domains"][domain_name]["Geometry"]["Thickness (Y)"]))
        
        self.corners={"X" : [float(corner0[0]), float(corner1[0])], "Y" : [float(corner0[1]),float(corner1[1])]}
        self.dimensions={}
        self.dimensions.update({"lx": float(corner1[0]) - float(corner0[0]), "ly": float(corner1[1]) - (corner0[1])})

            
    def set_mesh(self,key,deck,dimensions):
        aux={}
        mesh=deck.doc["Domains"][key]["Mesh"]
        for key in mesh.keys():
            aux[key] = int(mesh[key])
        aux.update({"dx": dimensions["lx"]/aux["Number of Elements in X"]})
        aux.update({"dy": dimensions["ly"]/aux["Number of Elements in Y"]})
        self.mesh=aux
            
            
    def set_material(self, key, deck):
        aux={}
        material=deck.doc["Domains"][key]["Material"]
        for key in material.keys():
            if isinstance(material[key],dict)==False:
                aux[key]=float(material[key])
            else:
                aux[key]={}
                for param in material[key]:
                    aux[key].update({param: float(material[key][param])})
        self.material=aux
        
        
            
    def set_IC(self, key, deck):
        aux={}
        ic = deck.doc["Domains"][key]["Initial Condition"]
        for key in ic.keys():
            aux[key]=float(ic[key])
        self.initial_conditions=aux
        


    def set_bc(self,key,deck):
        aux={}
        bc=deck.doc["Domains"][key]["Boundary Condition"]
        for location in bc:
            aux[location]={}
            for edge in bc[location]:
                aux[location][edge]={}
                for var in bc[location][edge]:
                    # import pdb; pdb.set_trace()
                    aux[location][edge].update({var:float(bc[location][edge][var])})
        self.boundary_conditions=aux
