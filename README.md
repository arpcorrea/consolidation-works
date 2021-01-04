# The problem

This code solves a 2D transiet heat transfer problem with or without material interface between different domains. 


3 different plates with dimesions Xi and Yi are defined by the user in ["Domains"]["Plate i"]["Geometry"]["Y0"], ["Domains"]["Plate i"]["Geometry"]["X0"], ["Domains"]["Plate i"]["Geometry"]["Y1"], ["Domains"]["Plate i"]["Geometry"]["X1"] in which "i" is the plate number and [Y0, Y1] is initial and final Y location and  [X0, X1] are initial and final X location.

Each domain is orthotropic, i.e thermal conductivity in X and Y are set independently under ["Domains"]["Plate i"]["Material"]["Kx"] and ["Domains"]["Plate i"]["Material"]["Ky"]. It is important to notice that each plate can have its own properties, meaning that it supports discontinuities between domains. Since it is a transient problem, material density and heat capacity are set in ["Domains"]["Plate i"]["Material"]["rho"] and ["Domains"]["Plate i"]["Material"]["Cp"] respectively. 

In case of domains with distinct materials into contact, zero thermal contact resistance or infinite thermal contact impedance is considered, i.e perfect thermal interface contact.

Each domain has its own initial temperature, set in ["Domains"]["Plate i"]["Initial Condition"]["Temperature"].

The user also define the number of points in X and Y of each domain in ["Domains"]["Plate i"]["Mesh"]["Points in X"] and ["Domains"]["Plate i"]["Mesh"]["Points in Y"] respectivelly.

The number of steps and step time are defined in ["simulation"]["Step Time"] and ["simulation"]["Number Time Steps"] respectivelly. Notice that large step time may not converge and an error message will popup.





```yaml
Problem Type:
    Type: Heat Transfer
    Total Plates: 3
    Length: 0.001
Domains:
    Plate 1:
        Geometry:
            y0: 0
            y1: 0.004
            x0: 0
            x1: 0.1
        Material: 
            kx: 1
            ky: 1
            Density: 1500
            Cp: 1000
            Viscosity:
                A: 0.0056
                Ea: 74400
        Mesh:
            Points in X: 101
            Points in Y: 11
        Boundary Condition:
            Thermal:
                Fixed Boundary:
                    Bottom Edge:
                        Temperature: 25
                    Left Edge:
                        Temperature: 25
                    Right Edge:
                        Temperature: 25
            Mechanical:
                Intimate Contact:
                    Top Edge:
                        Horizontal asperity ratio: 4
                        Vertical asperity ratio: 4
        Initial Condition:
            Temperature: 30
    Plate 2:
        Geometry:
            y0: 0.004
            y1: 0.006
            x0: 0
            x1: 0.1           
        Material: 
            kx: 50
            ky: 27
            Density: 15000
            Cp: 1000
            Viscosity:
                A: 0.0056
                Ea: 74400
        Mesh:
            Points in X: 101
            Points in Y: 6
        Boundary Condition:  
            Thermal:
                Fixed Boundary:
                    Left Edge: 
                        Temperature: 25
                    Right Edge:
                        Temperature: 25
            Mechanical:
                Intimate Contact:
                    Top Edge:
                        Horizontal asperity ratio: 2
                        Vertical asperity ratio: 2
                    Bottom Edge:
                        Horizontal asperity ratio: 2
                        Vertical asperity ratio: 2
        Initial Condition:
            Temperature: 700
            Power Input:
                Inner: 1000 
    Plate 3:
        Geometry:
            y0: 0.006
            y1: 0.010
            x0: 0
            x1: 0.1
        Material: 
            kx: 1
            ky: 1
            Density: 1500
            Cp: 1000
            Viscosity:
                A: 0.0056
                Ea: 74400
        Mesh:
            Points in X: 101
            Points in Y: 11
        Boundary Condition:
            Thermal:
                Fixed Boundary:
                    Right Edge:
                        Temperature: 25
                    Top Edge:
                        Temperature: 25
                    Left Edge:
                        Temperature: 25
            Mechanical:
                Intimate Contact:
                    Bottom Edge:                    
                        Horizontal asperity ratio: 1
                        Vertical asperity ratio: 1
        Initial Condition: 
            Temperature: 30
Simulation:
    Step Time: 0.01
    Number of Steps: 2000

```


# Getting Started


### Deck
A class named "Deck" is created to read the information of the .yaml (shown above).
### Problem
A class named "TwoPlates" is defined to organize the data and assign values in local fields. .
### Mesh
A class named "Masher" is used to assemble each local field into a master fields. 
### Heat Transfer Model
A class named "Heat Transfer" solves the heat transfer problem by central differences.
### Solver
A class named "SolvesTwoPlates" is defined to create a forward step analysis, solving the heat transfer model.