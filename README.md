# The problem - 


A plate with dimensions X and Y are defined by the user in ["Geometry"]["Length X"]["Length Y"]

The plate, made of orthotropic, material is heated on the left boundary with a constant heat Q, defined by the user in ["Boundary Conditions"]["Power"]. We assumed that this material is aluminium"

The plate's initial temperature is defined by the user in ["Materials"]["Aluminium"]["Initial Temperature"]. Other material properties are also defined in ["Materials"]["Aluminium"].

The plate is inside a room, with a constant temperature is set by the user in ["Boundary Conditions"]["Room Temperature"].

The user also define the number of elements in X and Y in ["simulation"]["Number of Elements X"] and ["simulation"]["Number of Elements Y"] respectivelly.

The number of steps and step time are defined in ["simulation"]["Step Time"] and ["simulation"]["Number Time Steps"] respectivelly. Notice that large step time may not converge and an error message will popup.

Finally, the code generates Temperature plots at every interval, defined in ["Plot"]["plot interval"].



```yaml
Problem Type:
    Type: Aluminium
    
Geometry:
    Length X: 0.2
    Length Y: 0.2
 
Materials:
  Aluminium:
    Thermal Conductivity X: 237
    Thermal Conductivity Y: 237
    Density: 2700
    Cp: 1000
    Initial Temperature: 333.
    
Boundary Conditions:
    Room Temperature: 293
    Power: 500000
    convection coefficient: 25
    

Simulation:
  Time Step: 0.01
  Number Time Steps: 10001
  Number of Elements X: 100 
  Number of Elements Y: 100

Plot:
  Temp Output Folder: "./output/Temperature/"
  figure temperature name: Temperature
  Color Interpolation: 50
  Color Map: "inferno"
  plot interval: 500
  
Animation:
    name: temperature

```


# Getting Started


### Geomtry
A class named "Geometry" is difined only to store the X and Y dimensions of the problem.
### Mesh
A class named "Plate" is defined to create the mesh and assign Initial Temperature, Thermal Diffusivity in X and Thermal Diffusivity in Y in each element.
### Model
A class named "Heat Transfer" solves the heat transfer problem by central differences.
### Plot and Animation
A class named "PlotsTwoPlates" is defined to generate figures of the thermal history in spaced intervals. In the end, a .GIF is created from those figures.
### Solver
A class named "SolvesTwoPlates" is defined to create a forward step analysis, solving the heat transfer model and plotting the figures when convenient.