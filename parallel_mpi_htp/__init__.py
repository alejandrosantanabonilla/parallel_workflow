# File: parallel_mpi_htp/__init__.py

"""
parallel_mpi_htp: A Dask-MPI tool for high-throughput parallel relaxation of atomic structures.
"""

# Import key functions to make them directly accessible from the package
from .core import create_atoms, relax_and_save

# (Optional but good practice) Define a version number
__version__ = "0.1.0"

# (Optional but good practice) Define the public API of the package
# This controls what `from parallel_mpi_htp import *` will import
__all__ = [
    'create_atoms',
    'relax_and_save',
    '__version__',
]
