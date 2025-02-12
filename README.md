# Memristor device simulator

This is a memristive circuits simulation platform made by Ignacio Piñeyro. This platform integrates a module for
creating `.cir` circuit files, a module for executing simulations using NGSpice, and another one that plots the
results in different manners. The platform was implemented in Python, with the help of different libraries such as
NumPy Pandas, SciPy, NetworkX and Matplotlib.


---

## TODO list:

* Test coverage for each service/template
* Web App framework (FastAPI? Django?)
* Dockerize App
* Create UI - Frontend

---

## Project structure:

- **/models:** subcircuit (.sub) files with memristor models (Pershin, Vourkas, Biolek, etc). These files have
  the dynamic parameters of the memristor.

- **/services:**
    * `circuitfileservice.py`: Circuit file (.cir) generation. Circuit file contains subcircuits dependencies,
      componentes
      instance, analysis commands and control commands. Simulation CSV file name and path are written here.
    * `subcircuitfileservice.py`: Subcircuit file (.sub) generation. Subcircuit file contains memristor model
      parameters, other
      models dependencies, sources, componentes and control commands. These files are saved in the /models directory.
    * `plotterservice.py`: Plotting service to generate I-V and State-Time curves for particular simulations,
      comparative plots
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

## Before starting

- Python3 (versions above 3.10 may have incompatibility issues with project dependencies)
- NGSpice Engine
- Install project dependencies on `requirements.txt` (Venv recommended)

---

## Getting started

* Clone the repository
* Install NGSpice and add its exec file to the PATH variable:
    - Windows: http://ngspice.sourceforge.net/download.html
    - Linux: `sudo apt-get install ngspice`
* Install the required dependencies (using a virtual environment is recommended) - `pip install -r requirements.txt`
* At the end of the `main.py` file, you can modify the `simulate` function to use one of the template simulations for a
  given model and generate the desired plots. Supported templates, models and plots are still limited but the plan is to
  add more.
    - **_Simulation templates:_
      ** `DEFAULT_TEST`, `DEFAULT_NETWORK`, `DEFAULT_NETWORK_WITH_EDGE_REMOVAL`, `DI_FRANCESCO_VARIABLE_AMPLITUDE`, `DI_FRANCESCO_VARIABLE_BETA`, `QUINTEROS_EXPERIMENTS`, `RANDOM_REGULAR`, `WATTS_STROGATZ_CIRCULAR_REGULAR`, `WATTS_STROGATZ`
    - **_Plot Types:_
      ** `IV`, `IV_OVERLAPPED`, `IV_LOG`, `IV_LOG_OVERLAPPED`, `MEMRISTIVE_STATES`, `MEMRISTIVE_STATES_OVERLAPPED`
    - **_Models:_** `PERSHIN` and `VOURKAS`
    - **_Amount Iterations:_** Any integer. Amount of times the template will be simulated. Used to compute average time
      measure of simulations.

```
if __name__ == "__main__":
    simulate(
        simulation_template=SimulationTemplate.DEFAULT_TEST,
        plot_types=[
            PlotType.IV, PlotType.IV_OVERLAPPED, PlotType.IV_LOG, PlotType.IV_LOG_OVERLAPPED,
            PlotType.MEMRISTIVE_STATES, PlotType.MEMRISTIVE_STATES_OVERLAPPED
        ],
        model=MemristorModels.PERSHIN, amount_iterations=100
    )
```

* Execute `main.py` with `python3 main.py`

---

#### Coded by Ignacio Piñeyro as part of my Electronic Eng. degree's final project for Universidad Nacional de San Martin (UNSAM). Feel free to send any questions, suggestions or comments to ignaciopineyroo@gmail.com
