import pytest
from mpi4py import MPI
from pathlib import Path
import os

# Import the high-level calculator function from your library
from parallel_mpi_htp import calculator

@pytest.fixture
def rootdir():
    """A pytest fixture that returns the root directory of the test file."""
    return os.path.dirname(os.path.abspath(__file__))


# This marker tells pytest to run this test only when the 'mpi' option is used.
@pytest.mark.mpi
def test_calculator_with_data_files(tmp_path, rootdir):
    """
    An end-to-end integration test that uses pre-existing data files.
    This test will be run in parallel by pytest-mpi.
    
    Args:
        tmp_path (pathlib.Path): A pytest fixture providing a temporary directory for outputs.
        rootdir (str): A custom fixture providing the path to the tests directory.
    """
    # MPI setup to ensure only one process handles file setup/teardown.
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()

    # --- 1. Test Setup (run by only one process) ---
    if rank == 0:
        print(f"\n[Rank {rank}] Locating test data...")
        
        # Define the path to the data directory using the rootdir fixture
        data_dir = os.path.join(rootdir, "data")
        
        # Find all .xyz files in the data directory
        input_files_paths = list(Path(data_dir).glob("*.xyz"))
        
        # Convert Path objects to strings for MPI communication
        input_files = [str(p) for p in input_files_paths]
        
        # Define the output directory inside the temporary path provided by pytest
        output_dir = tmp_path / "outputs"
        output_dir.mkdir()
        
        print(f"[Rank {rank}] Found {len(input_files)} files to process.")

    else:
        # Other ranks need placeholders for the broadcast.
        input_files = None
        output_dir = None

    # Broadcast the list of file paths and output dir from rank 0 to all other processes.
    input_files = comm.bcast(input_files, root=0)
    output_dir = comm.bcast(str(output_dir), root=0)

    # --- 2. Execute the Function Under Test ---
    # All processes will participate in this call.
    tblite_params = {"method": "GFN2-xTB"}
    
    results = calculator(
        input_files=input_files,
        output_dir=output_dir,
        tblite_params=tblite_params
    )
    
    # --- 3. Assertions (run by only one process to avoid redundant checks) ---
    if rank == 0:
        print(f"[Rank {rank}] Validating results...")
        assert results is not None, "Calculator should return a list of results."
        # The number of expected results is now 3, based on the files in the data folder.
        assert len(results) == 3, "Expected 3 results for the 3 input files."

        # Check that the output files were actually created
        output_dir_path = Path(output_dir)
        created_files = list(output_dir_path.glob("*.xyz"))
        assert len(created_files) == 3, "Expected 3 relaxed XYZ files in the output directory."
        print("[Rank 0] Test passed successfully!")
