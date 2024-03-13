import os
import shutil
from src.download.holdingsdownloader import get_all_pdb_and_sifts
from src.download.downloadwithThreadPool import run_downloads_with_ThreadPool, url_formation_for_pool


def prepare_paths(base_dir):
    """Generates paths for different data types."""
    paths = {
        "mmCIF": {"input": f"{base_dir}/mmCIF", "output": f"{base_dir}/output_mmCIF"},
        "PDB": {"input": f"{base_dir}/PDB", "output": f"{base_dir}/output_PDB"},
        "SIFTS": {"input": f"{base_dir}/SIFTS", "output": None},
        "mmCIF_assembly": {"input": f"{base_dir}/mmCIF_assembly", "output": f"{base_dir}/output_mmCIF_assembly"},
        "PDB_assembly": {"input": f"{base_dir}/PDB_assembly", "output": f"{base_dir}/output_PDB_assembly"},
    }
    return paths


def clear_paths(paths, format_of_db):
    """Clears specified paths for a given format or all."""
    for format, path_info in paths.items():
        if format_of_db == "all" or format == format_of_db:
            for key, path in path_info.items():
                if path and os.path.exists(path):
                    shutil.rmtree(path)
                    os.makedirs(path, exist_ok=True)


def download_data_for_format(format_of_db, paths, holdings):
    """Downloads data for the specified format using provided paths."""
    formats_to_download = ["mmCIF", "PDB", "SIFTS", "mmCIF_assembly", "PDB_assembly"] if format_of_db == "all" else [format_of_db]
    left_to_download_info = []

    for format in formats_to_download:
        files = holdings.get(format, [])
        input_path = paths[format]["input"]
        try:
            left_to_download = [fn for fn in files if fn not in os.listdir(input_path)]
        except FileNotFoundError:
            left_to_download = files

        urls = url_formation_for_pool(format, left_to_download, default_path=input_path)

        run_downloads_with_ThreadPool(format, urls)
        left_to_download_info.append((format, left_to_download))

    return left_to_download_info


def supreme_download_master(format_of_db, job_type=None, default_path=os.getcwd()):
    """Master function to manage downloading and refreshing data."""
    paths = prepare_paths(default_path)
    holdings = get_all_pdb_and_sifts()

    if job_type == "refresh":
        clear_paths(paths, format_of_db)

    left_to_download_info = download_data_for_format(format_of_db, paths, holdings)
    return left_to_download_info


# Example usage
#base_directory = os.getcwd() # Or any base directory you prefer
#print(base_directory)
#downloaded_files_info = supreme_download_master("mmCIF_assembly", job_type="refresh", default_path=os.getcwd())
#downloaded_files_info = supreme_download_master("mmCIF", job_type="refresh", default_path=os.getcwd())
#downloaded_files_info = supreme_download_master("PDB_assembly", job_type="refresh", default_path=os.getcwd())
#downloaded_files_info = supreme_download_master("PDB", job_type="refresh", default_path=os.getcwd())
#downloaded_files_info = supreme_download_master("SIFTS", job_type="refresh", default_path=os.getcwd())


#print(downloaded_files_info)
