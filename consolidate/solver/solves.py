# -*- coding: utf-8 -*-
import numpy as np



class SolvesTwoPlates:
    
    def __init__(self, problem,model_HT,mesh):
        for field_dir in mesh.fields:
            if field_dir.name =="Temperature":
                Told = field_dir.value.copy()
                self.Tnew = field_dir.value.copy()
                self.Tnodes = np.zeros((np.shape(self.Tnew)[0]-1, np.shape(self.Tnew)[1]-1))
            if field_dir.name == "Equivalent External Temperature":
                self.dir_Tout = field_dir
            if field_dir.name == "Viscosity":
                self.dir_Visc = field_dir
                
        # self.T=
        self.do_solver(problem, model_HT,mesh, Told)
        
    def do_solver(self,problem, model_HT,mesh, Told):
        
        for m in range(int(problem.SimulationParameters["Number of Steps"])):

                self.Tnew, self.Tnodes = model_HT.do_timestep_cond_conv( self.Tnew.copy(), Told.copy(), self.Tnodes.copy())
                Told = self.Tnew.copy()

            # self.dir_Visc.value = model_visc.do_timestep(self.dir_Visc.value, self.dir_T.value)

# # -------------- CALCULATE VISCOSITY FOR EACH STEP INCREMENT----------             
#             self.meshes.Visc=self.model_IC.viscosity_timestep(self.meshes.Visc, self.meshes.T)
# # -------------- CALCULATE Dic FOR EACH STEP INCREMENT----------             
#             self.meshes.Dic=self.model_IC.dic_timestep(self.meshes.Dic, self.meshes.Dic0, self.meshes.Visc, float(self.deck.doc["Simulation"]["Time Step"]))
# # -------------- UPDATE THE INTEGRAL----------             
#             self.model_IC.aux=self.model_IC.update_aux( float(self.deck.doc["Simulation"]["Time Step"]), self.meshes.Visc)
# # -------------- UPDATE Dic----------             
#             self.meshes.Dic=np.clip(self.meshes.Dic,0,1)
# # -------------- DO PLOT ACCORDING TO THE SELECTED INTERVAL----------             
#             if m in self.plots.mfig:
#                 self.plots.update_Dic(self.meshes.Dic)
#                 self.plots.update_T(self.meshes.T)       
#                 self.plots.do_plots(m)    
#         self.plots.do_animation()
#         self.model_IC.calculate_average_dic()
            