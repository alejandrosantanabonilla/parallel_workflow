import os
import time
import argparse
import dask_mpi as dm
from dask.distributed import Client
from .core import create_atoms, relax_and_save

def main():
    """Main command-line interface function."""
    parser = argparse.ArgumentParser(
        description="Run parallel geometry relaxations using Dask-MPI and TBLite."
    )
    parser.add_argument(
        "files",
        metavar="FILE",
        type=str,
        nargs='+',
        help="One or more XYZ files to process."
    )
    parser.add_argument(
        "--method",
        type=str,
        default="GFN2-xTB",
        help="xTB method to use for the calculation (e.g., GFN2-xTB, GFN1-xTB)."
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=".",
        help="Directory to save the relaxed structure files."
    )
    args = parser.parse_args()

    start_time = time.time()

    # --- 1. Prepare TBLite Parameters ---
    final_tblite_params = {"method": args.method, "verbosity": 0}
    print("--- Configuration ---")
    print(f"Output directory: {args.output_dir}")
    print(f"Using TBLite parameters: {final_tblite_params}")
    print("---------------------\n")
    
    os.makedirs(args.output_dir, exist_ok=True)

    # --- 2. Prepare Tasks for Dask ---
    tasks_to_process = []
    print("--- Reading Input Files (Serial) ---")
    for xyz_file in args.files:
        base, ext = os.path.splitext(os.path.basename(xyz_file))
        output_name = f"{base}_relaxed{ext}"
        output_path = os.path.join(args.output_dir, output_name)
        
        structures = create_atoms(xyz_file)
        for atoms_obj in structures:
            tasks_to_process.append((atoms_obj, output_path, final_tblite_params))
    print("------------------------------------\n")

    # --- 3. Run Parallel Computation ---
    if tasks_to_process:
        print("Data loaded. Initializing Dask-MPI cluster...")
        dm.initialize()

        with Client() as client:
            print(f"Cluster ready. Distributing {len(tasks_to_process)} tasks to workers...")
            futures = client.map(relax_and_save, tasks_to_process)
            results = client.gather(futures)
            
            print("\n--- All Calculations Complete ---")
            for i, (energy, saved_file) in enumerate(results):
                if isinstance(energy, float) and energy != float('inf'):
                    print(f"  Task {i+1}: Structure saved to '{saved_file}' with final energy: {energy:.6f} eV")
                else:
                    print(f"  Task {i+1}: FAILED. Reason: {saved_file}")
            print("---------------------------------")
    else:
        print("\nFATAL ERROR: No structures were read from the input files.")
            
    end_time = time.time()
    total_time = end_time - start_time
    print(f'\nTotal time for parallel calculations: {total_time:.2f} seconds')

if __name__ == '__main__':
    main()
