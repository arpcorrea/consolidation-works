class RectangularDomain:


    def __init__(self, name, corner0, corner1, material, initial_temperature, number_of_elements_X, number_of_elements_Y,Power_Input_Density, Initial_Dic ):

        self.x0 = float(corner0[0])
        self.y0 = float(corner0[1])
        self.x1 = float(corner1[0])
        self.y1 = float(corner1[1])
        self.Lx = self.x1 - self.x0
        self.Ly = self.y1 - self.y0
        self.Number_of_Elements_in_X = number_of_elements_X
        self.Number_of_Elements_in_Y = number_of_elements_Y
        self.corner_element_0 = element_order_X
        self.corner_element_1 = element_order_Y
        self.ele_x0 = float(self.corner_element_0[0])
        self.ele_y0 = float(self.corner_element_0[1])  
        self.ele_x1 = float(self.corner_element_1[0])
        self.ele_y1 = float(self.corner_element_1[1])    
        self.material = material
        self.name = name

        self.initial_temperature=initial_temperature
        self.Power_Input_Density=Power_Input_Density
        self.Dic = Initial_Dic
        self.initial_fields = {"Temperature": float(initial_temperature)}

    def test_metric(self, point):
        if point[0] > self.x0 and point[0] < self.x1 and point[1] > self.y0 and point[1] < self.y1:

            return True
        else:
            return False
        
    def set_field_init_value(self, field_dict):
        for key, value in field_dict.items():
            self.initial_fields[key] = float(value)