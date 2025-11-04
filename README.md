# Memristor Device Simulator

Memristive circuits simulation App made by Ignacio Piñeyro. This platform creates `.cir` circuit files and runs the simulation of said circuit using NGSpice. The platform was implemented in Python and includes a web interface that allows the user to configure and simulate memristive networks.

---

## Quick Start with Docker

The easiest way to run the application is using Docker. This method works on any PC with Docker installed.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running the Application

1. **Clone the repository:**
```bash
git clone <repository-url>
cd memristor_simulation
```

2. **Start the application:**
```bash
make up-build # First time start
make up # If already built
```

3. **Access the application:**
- **Web Interface:** http://localhost:8000

4. **Stop the application:**
```bash
make down # Or CTRL+C
```

### Docker Features
- **Ubuntu 22.04 LTS** with Python 3.10
- **NGSpice Engine** pre-installed
- **All Python dependencies** from requirements.txt
- **Django web interface** ready to use

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

- **`constants.py`:** Enum objects with constants used in the project.
- **`representations.py`:** Dataclasses representations used in the project.
- **`requirements.txt`:** Dependencies needed to run code.

---

## Manual Installation (Alternative)

If you prefer to install manually without Docker:

### Prerequisites
- Python 3.10 (versions above 3.10 may have incompatibility issues with project dependencies)
- NGSpice Engine
- Virtual environment (recommended)

### Installation Steps

1. **Clone the repository:**
```bash
git clone <repository-url>
cd memristor_simulation
```

2. **Install NGSpice:**
   - **Windows:** Download from http://ngspice.sourceforge.net/download.html
   - **Linux:** `sudo apt-get install ngspice`
   - **macOS:** `brew install ngspice`

3. **Create and activate virtual environment:**
```bash
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

5. **Set up Django:**
```bash
python manage.py migrate
python manage.py collectstatic
```

6. **Run the development server:**
```bash
python manage.py runserver
```

7. **Access the application at:** http://localhost:8000

---

## Web Interface Usage

The Django web interface provides an easy-to-use form for configuring and running memristor simulations:

1. **Model Configuration:** Select memristor model (Pershin or Vourkas). Parameters will depend on the chosen model (Pershin and Vourkas have the same set of params)
2. **Input Parameters:** Source name and connection nodes
3. **Waveform Configuration:** Configure voltage waveforms (SIN, PULSE, PWL)
4. **Simulation Parameters:** Set simulation type, time steps, voltages, and device parameters
5. **Export Parameters:** Folder and file name and magnitudes to export
6. **Network Configuration:** Choose between single device or network topology. Parameters will depend on the chosen network type
7. **Plotter:** Select plot types. Some plots will depend on the chosen network type
8. **Execute Simulation:** Click "Run Simulation" to execute and download results as ZIP

### Simulation Results
- Simulation execution time scales with complexity of the circuit (amount of devices)
- Results are automatically packaged as ZIP files
- Include CSV data files, generated plots, and simulation logs
- Persistent storage maintains simulation history

---
---

#### Coded by Ignacio Piñeyro as part of my Electronic Eng. degree's final project for Universidad Nacional de San Martin (UNSAM). Feel free to send any questions, suggestions or comments to ignaciopineyroo@gmail.com
