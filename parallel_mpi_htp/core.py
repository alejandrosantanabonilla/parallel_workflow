import os
from ase.io import read, write

def create_atoms(filename):
    """Reads one or more molecular structures from an XYZ file."""
    if not os.path.exists(filename):
        print(f"Error: File not found at path '{filename}'")
        return []

    try:
        atoms_list = read(filename, index=':')
        print(f"Successfully read {len(atoms_list)} structure(s) from {filename}")
        return atoms_list
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return []


def relax_and_save(task_info):
    """
    Relaxes a structure using provided parameters, saves it, and returns its energy.
    This function is executed by Dask workers.
    """
    # These imports must be inside the worker function
    from ase.optimize import LBFGS
    from tblite.ase import TBLite

    atoms_object, output_filename, tblite_params = task_info

    try:
        atoms = atoms_object
        worker_name = os.uname().nodename
        print(f"Worker '{worker_name}': Starting task for '{output_filename}'")

        # Initialize the calculator with the passed parameters
        calculator = TBLite(**tblite_params)
        atoms.calc = calculator

        # Perform the geometry optimization
        optimizer = LBFGS(atoms)
        optimizer.run(fmax=0.05)

        # Get the final energy and save the structure
        energy = atoms.get_potential_energy()
        write(output_filename, atoms, format='xyz')
        
        print(f"Worker '{worker_name}': Finished task. Saved to '{output_filename}'. Energy: {energy:.6f} eV")
        return (energy, output_filename)

    except Exception as e:
        error_msg = f"An error occurred on worker '{os.uname().nodename}'. Error: {e}"
        print(error_msg)
        return (float('inf'), error_msg)
