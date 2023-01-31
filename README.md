# Memristor device simulator

This repository contains the code to generate simulation circuits files (.cir), subcircuits files (.sub), run 
simulations on NGSpice and plot the results. All features are divided in services (see services directory) in order to
consume them on demand by an interface.

---

## TODO list:
* Generate .cir and .sub files in simulation_results dir instead of a unique file
* Generate examples dir with default .sub and .cir files
* Implement Heaviside terms plot method
* Implement animated I-V plot method
* Create TimeMeasure tables from log files
* Improve plots (curves visibility, labels, etc)
* Add more models (Biolek, between others)
* Create UI - Frontend

---

## Project structure:
- **/models:** subcircuit (.sub) files with memristor models (Pershin, Pershin-Vourkas, Biolek, etc). These files have 
the dynamic parameters of the memristor.

- **/services:** 
  * `circuitfileservice.py`: Circuit file (.cir) generation. Circuit file contains subcircuits dependencies, componentes
  instance, analysis commands and control commands. Simulation CSV file name and path are written here.
  * `subcircuitfileservice.py`: Subcircuit file (.sub) generation. Subcircuit file contains memristor model parameters, other
models dependencies, sources, componentes and control commands. These files are saved in the /models directory.
  * `plotterservice.py`: Plotting service to generate I-V and State-Time curves for particular simulations, comparative plots
between all the simulations in a folder and a sub-plot figure for all simulations in folder.
  * `directoriesmanagementservice.py`: Paths finding and folders creation.
  * `ngspiceservice.py`: Wrapper for NGSpice simulation with time measure acquisition commands.
  * `timemeasureservice.py`: Time measure of simulations logic.

- **/simulation_results:**
  * /<model_name>_simulations
    * /<simulation_template_name>
      * /figures: Simulation plots.
      * /logs: Simulation logs with NGSpice output and time measures.
      * Simulation results (csv files)

- **`main.py`:** Main program file.
- **`constants.py`:** Enum objects with constants used in the project.
- **`representations.py`:** Dataclasses representations used in the project.
- **`requirements.txt`:** Dependencies needed to run code.

---

## Requirements
- Python3
- Numpy
- Pandas
- Networkx
- Matplotlib
- NGSpice (with executable path on PATH environment variable)

---

## Getting started
* Clone the repository
* Install NGSpice and add its exec file to the PATH variable:
    - Windows: http://ngspice.sourceforge.net/download.html
    - Linux: `sudo apt-get install ngspice`
* Install the required dependencies (using a virtual environment is recommended) - `pip install -r requirements.txt`
* Execute `main.py` with `python3 main.py`

---

#### Coded by Ignacio Piñeyro as part of my Electronic Eng. degree's final project for Universidad Nacional de San Martin (UNSAM). Feel free to send any questions, suggestions or comments to ignaciopineyroo@gmail.com