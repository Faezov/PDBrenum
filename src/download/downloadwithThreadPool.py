import os
from datetime import datetime, timedelta
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


def ensure_dir(path):
    """Ensure the directory exists. Create if it does not."""
    os.makedirs(path, exist_ok=True)


def is_recent_file(file_path):
    """Check if the file is recent enough to skip downloading."""
    if not os.path.exists(file_path):
        return False
    last_modified = datetime.fromtimestamp(os.path.getmtime(file_path))
    return datetime.now() - last_modified < timedelta(days=7)


def url_formation_for_pool(format_to_download="mmCIF", list_of_file_names=(), default_input_path=os.getcwd()):
    # Old URLs base
    # base_url = {
    #     "mmCIF": "https://files.rcsb.org/pub/pdb/data/structures/all/mmCIF/",
    #     "PDB": "https://files.rcsb.org/pub/pdb/data/structures/all/pdb/",
    #     "SIFTS": "http://ftp.ebi.ac.uk/pub/databases/msd/sifts/xml/",
    #     "mmCIF_assembly": "https://www.ebi.ac.uk/pdbe/static/entry/",
    #     "PDB_assembly": "https://ftp.wwpdb.org/pub/pdb/data/biounit/PDB/all/"
    # }

    urls_to_target_files = []
    for file_name in list_of_file_names:
        if len(file_name) < 4:
            raise ValueError("File name must be at least 4 characters long.")

        url = "https://files.rcsb.org/download/" + file_name
        # Correction here to include filename in the path
        file_path = os.path.join(default_input_path, file_name)
        urls_to_target_files.append((url, file_path))

    return urls_to_target_files


def download_file(url_path_tuple):
    url, final_path = url_path_tuple
    max_attempts = 3
    attempt = 0

    if is_recent_file(final_path):
        # print(f"Skipping download; recent file exists at {final_path}")
        return

    while attempt < max_attempts:
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                os.makedirs(os.path.dirname(final_path), exist_ok=True)  # Ensure the directory exists
                with open(final_path, 'wb') as f:
                    for data in response.iter_content(chunk_size=4096):
                        f.write(data)
                # print(f"Successfully downloaded {final_path}")
                break  # Download succeeded, break out of the loop
            else:
                print(f"Failed to download {url}, Status code: {response.status_code}")
        except Exception as e:
            print(f"Failed to download {url}: {e}")

        attempt += 1
        if attempt < max_attempts:
            print(f"Retrying download for {url} (Attempt {attempt + 1} of {max_attempts})...")
        else:
            print(f"Download failed after {max_attempts} attempts for {url}")


def run_downloads_with_ThreadPool(format_to_download="mmCIF", urls_to_target=()):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(download_file, url_path) for url_path in urls_to_target]
        for _ in tqdm(as_completed(futures), total=len(futures), desc=f"Downloading {format_to_download} files"):
            pass
