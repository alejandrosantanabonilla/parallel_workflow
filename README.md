# parallel_workflow
This new library utilizes an MPI workflow to perform high-throughput calculations, making it ideal for creating massive databases.
This document provides detailed instructions on how to set up the necessary environment and dependencies to run this project. The core requirement is a functional MPI (Message Passing Interface) implementation, specifically OpenMPI, that can be used by Python packages like mpi4py.

We present two common, robust methods for achieving this setup.

**Option 1:** For users on High-Performance Computing (HPC) clusters or systems that use environment modules. This method combines the system-provided OpenMPI with a standard Python virtual environment.

**Option 2:** For users on local machines (desktops, laptops) or systems where Conda is the preferred package manager. This method creates a self-contained environment with all dependencies, including OpenMPI, managed by Conda.

# Installation and Setup

Please choose one of the following two options to configure your environment.

# Option 1: Using System Modules and a Python Virtual Environment

This approach is ideal for HPC clusters where optimized libraries like OpenMPI are provided through a module system. The mpi4py package is smart enough to be compiled against the version of MPI that is currently loaded in your shell environment.

## Step-by-step instructions:

### Load the OpenMPI Module:
    
First, you need to load the OpenMPI compiler and runtime libraries into your environment. The exact name might differ slightly       based on your system's configuration (openmpi/4.1.1, gnu-openmpi, etc.). Use module avail to see available modules.

### Load the OpenMPI module

```
module load openmpi
```

### Verify MPI is Loaded:
    
Check that the MPI commands are available in your PATH.

```
which mpirun
```
    
**Expected output: /path/to/your/cluster/openmpi/bin/mpirun**

### Create a Python Virtual Environment:
    
It is best practice to isolate project dependencies. Create a virtual environment in your project directory.

**Create a virtual environment named 'venv'**

```
python3 -m venv venv
```

**Activate the Virtual Environment:**
    
Before installing packages, you must "enter" the environment.

### Activate the environment

```
source venv/bin/activate
```

Your shell prompt should now be prefixed with (venv).

**Install Python Dependencies with Pip:**
    
With OpenMPI loaded and the virtual environment active, install mpi4py and any other required packages. Pip will invoke the MPI      compiler (mpicc) during the installation of mpi4py.

**Ensure pip is up to date**

```
pip install --upgrade pip
```

**Install parallel_workflow**


First, download the source code from GitHub using git clone and navigate into the project directory.

```
git clone https://github.com/alejandrosantanabonilla/parallel_workflow.git
cd parallel_workflow
```

Now, install the parallel_mpi_htp package in "editable" mode:

- The -e flag links the installation to your source code, so any changes you make are immediately available.

- The .[mpi] part tells pip to install the optional MPI-related Python libraries (mpi4py, dask-mpi) defined in the pyproject.toml.

```
pip install -e .[mpi]
```

**Ready to Go!**

Your environment is now set up. To run a script, use the mpirun command provided by the module.

**Run your script on 4 processes**

```
mpirun -n 4 python your_script.py
```

### Deactivating the Environment:

When you are finished, you can leave the virtual environment.

```
deactivate
```

# Option 2: Using a Conda Environment

Conda is an excellent package and environment manager that can handle non-Python dependencies like OpenMPI. This method creates a completely isolated and portable environment, which is great for reproducibility on local machines or servers where you have Conda installed.

## Step-by-step instructions:

### Create a Conda Environment:

Create a new environment, specifying the Python version you need. We will name it mpi-env.

### Create a new environment named 'mpi-env' with Python 3.9

```
conda create --name mpi-env python=3.9
```

### Activate the Conda Environment:

You must activate the environment before installing packages into it.

### Activate the environment

```
conda activate mpi-env
```

Your shell prompt should now be prefixed with (mpi-env).

### Install OpenMPI and Other Dependencies:
    
Using Conda, install OpenMPI, mpi4py, and all other libraries from a channel like conda-forge, which has a wide selection of        compatible packages. Conda will ensure that the mpi4py it installs is correctly linked to the OpenMPI version it also installs.

### Install openmpi, mpi4py, and other libraries from the conda-forge channel

First, download the source code from GitHub using git clone and navigate into the project directory.

```
git clone https://github.com/alejandrosantanabonilla/parallel_workflow.git
cd parallel_workflow
```
Now, install the parallel_mpi_htp package in "editable" mode:

- The -e flag links the installation to your source code, so any changes you make are immediately available.
- The .[mpi] part tells pip to install the optional MPI-related Python libraries (mpi4py, dask-mpi) defined in the pyproject.toml.

```
pip install -e .[mpi]
```

### Verify the Installation:
    
The mpirun command should now point to the one installed inside your Conda environment.

```
which mpirun
```

**Expected output:** /path/to/your/conda/envs/mpi-env/bin/mpirun

Ready to Go!

Your self-contained Conda environment is ready. Use the mpirun command from within the environment to execute your scripts.

### Run your script on 4 processes

```
mpirun -n 4 python your_script.py
```

### Deactivating the Environment:

When you are finished, you can deactivate the Conda environment.

```
conda deactivate
```
