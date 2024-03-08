import os
import requests
from tqdm import tqdm
import gzip
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def extract_filenames(holdings, file_type):
    filenames = []
    for pdbid in holdings:
        # Check if the file_type entry is a list or a single path
        file_paths = holdings[pdbid].get(file_type, [])
        if isinstance(file_paths, list):
            filenames.extend([os.path.basename(fp) for fp in file_paths])
        else:
            # Assuming file_paths is a string path in this case
            filenames.append(os.path.basename(file_paths))
    return filenames


def download_holding(url, filename, holdings_dir):
    filepath = os.path.join(holdings_dir, filename)
    # Check if file exists and its age
    if os.path.exists(filepath):
        last_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
        if datetime.now() - last_modified < timedelta(days=7):
            print(f"{filename} is up-to-date. Skipping download.")
            return

    # Proceed with download if file doesn't exist or is older than a week
    try:
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte

        progress_bar = tqdm(total=total_size_in_bytes, desc=f"Downloading: {filename}", unit='iB', unit_scale=True)
        with open(filepath, 'wb') as f:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()

        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong during the download")
        else:
            print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")


def get_all_pdb_and_sifts(default_input_path=os.getcwd()):
    holdings_dir = os.path.join(default_input_path, "holdings")
    os.makedirs(holdings_dir, exist_ok=True)  # Ensure the holdings directory exists

    url = "https://files.wwpdb.org/pub/pdb/holdings/current_file_holdings.json.gz"
    filename = "pdb_holdings.json.gz"
    try:
        download_holding(url, filename, holdings_dir)
        with gzip.open(os.path.join(holdings_dir, filename), 'rt', encoding='utf-8') as f:
            holdings = json.load(f)
    except Exception as e:
        print(e)
        holdings = {}

    filename = "sifts_holdings.xml"
    try:
        download_holding("https://ftp.ebi.ac.uk/pub/databases/msd/sifts/xml", filename, holdings_dir)
    except Exception as e:
        print(e)

    try:
        with open(os.path.join(holdings_dir, filename)) as xml:
            soup = BeautifulSoup(xml.read(), 'lxml')
            sifts_files = [a['href'] for a in soup.find_all('a', href=True) if a['href'].endswith('.xml.gz')]
    except Exception as e:
        print(e)
        sifts_files = []

    return {
        "mmCIF": extract_filenames(holdings, "mmcif"),
        "PDB": extract_filenames(holdings, "pdb"),
        "mmCIF_assembly": extract_filenames(holdings, "assembly_mmcif"),
        "PDB_assembly": extract_filenames(holdings, "assembly_pdb"),
        "SIFTS": sifts_files
    }


# holdings = get_all_pdb_and_sifts()
# print(len(holdings["mmcif"]))
# print(holdings["mmcif"][:10])

