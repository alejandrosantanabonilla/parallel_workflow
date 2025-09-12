import os
import argparse
# The CLI now only needs to import the high-level calculator function
from .core import calculator

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

    # --- 1. Prepare Parameters ---
    final_tblite_params = {"method": args.method, "verbosity": 0}
    
    os.makedirs(args.output_dir, exist_ok=True)

    # --- 2. Run the Calculation by Calling the Library Function ---
    results = calculator(
        input_files=args.files,
        output_dir=args.output_dir,
        tblite_params=final_tblite_params
    )

    # --- 3. Print the Final Report ---
    print("\n--- Command-Line Job Complete ---")
    if results:
        for i, (energy, saved_file) in enumerate(results):
            if isinstance(energy, float) and energy != float('inf'):
                print(f"  Task {i+1}: Structure saved to '{saved_file}' with final energy: {energy:.6f} eV")
            else:
                print(f"  Task {i+1}: FAILED. Reason: {saved_file}")
    print("---------------------------------")


if __name__ == '__main__':
    main()
