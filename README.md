# Memristor device simulator

This repository contains the code to generate simulation circuits files (.cir), subcircuits files (.sub), run 
simulations on NGSpice and plot the results. All features are divided in services (see services directory) in order to
consume them on demand by an interface.

## Project structure:
- **/models:** subcircuit (.sub) files with memristor models (Pershin, Pershin-Vourkas, Biolek, etc). These files have 
the dynamic parameters of the memristor.
- **/services:** 
  * circuitfileservice: Circuit file (.cir) generation. Circuit file contains subcircuits dependencies, componentes
  instance, analysis commands and control commands. Simulation CSV file name and path are written here.
  * subcircuitfileservice: Subcircuit file (.sub) generation. Subcircuit file contains memristor model parameters, other
models dependencies, sources, componentes and control commands. These files are saved in the /models directory.
  * plotterservice: Plotting service to generate I-V and State-Time curves for particular simulations, comparative plots
between all the simulations in a folder and a sub-plot figure for all simulations in folder.
- **/simulation_results:** Simulation folders with CSV files.
- **constants.py:** Python Enum objects with constants used in the project.
- **representations:** Python Dataclasses used in the project.
- **requirements.txt:** Python dependencies needed to run code.

## Requirements
- Python3
- Numpy
- Pandas
- Networkx
- Matplotlib
- NGSpice (with executable path on PATH environment variable)

## Getting started
* Clone the repository
* Install NGSpice and add its exec file to the PATH variable:
    - Windows: http://ngspice.sourceforge.net/download.html
    - Linux: ```sudo apt-get install ngspice```
* Install the required dependencies (using a virtual environment is recommended) - ```pip install -r requirements.txt```
