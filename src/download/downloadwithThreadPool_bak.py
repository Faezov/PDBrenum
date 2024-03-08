import os

from src.download.modules import *
from src.download.lookfilesinside import look_what_is_inside
# IMPORTANT!!! Check your network connection: Wi-Fi or Wired Ethernet

# from src.download.catalogdownloader import catalog_downloader
# from src.download.latestcatreader import latest_catalog_reader
# from src.download.lookfilesinside import look_what_is_inside

# default_input_path_to_mmCIF = current_directory + "/mmCIF"
# default_input_path_to_mmCIF_assembly = current_directory + "/mmCIF_assembly"
# default_input_path_to_PDB = current_directory + "/PDB"
# default_input_path_to_PDB_assembly = current_directory + "/PDB_assembly"
# default_input_path_to_SIFTS = current_directory + "/SIFTS"
# default_output_path_to_mmCIF = current_directory + "/output_mmCIF"
# default_output_path_to_mmCIF_assembly = current_directory + "/output_mmCIF_assembly"
# default_output_path_to_PDB = current_directory + "/output_PDB"
# default_output_path_to_PDB_assembly = current_directory + "/output_PDB_assembly"


def download_pdb_assemblies_list_with_lxml():
    for _ in range(5):
        session = requests.Session()
        # rcsb = "https://files.rcsb.org/pub/pdb/data/biounit/PDB/all/"
        wwpdb = "https://ftp.wwpdb.org/pub/pdb/data/biounit/PDB/all/"
        links = set()
        try:
            with session.get(wwpdb, stream=True, timeout=600) as r:
                dom = html.fromstring(r.content)
                for link in dom.xpath('//a/@href'):
                    if ".gz" in link:
                        links.add(wwpdb + link)
            return links

        except requests.exceptions.RequestException as err:
            print(err)
            print("Will try again in 5 seconds...")
            time.sleep(5)


def url_formation_for_pool(format_to_download="mmCIF", list_of_file_names=(), default_input_path=os.getcwd()):
    urls_to_target_files = list()
    for file_name in list_of_file_names:
        if len(file_name) >= 4:
            if format_to_download == "mmCIF" or format_to_download == "all":
                if not os.path.exists(default_input_path):
                    os.makedirs(default_input_path)
                if "ent" in file_name and file_name.startswith('pdb'):
                    target_name = file_name[3:7] + ".cif.gz"
                else:
                    target_name = file_name[0:4] + ".cif.gz"
                urls_to_target_files.append("https://files.rcsb.org/pub/pdb/data/structures/all/mmCIF/" + target_name)

            if format_to_download == "PDB" or format_to_download == "all":
                if not os.path.exists(default_input_path):
                    os.makedirs(default_input_path)
                if "ent" in file_name and file_name.startswith('pdb'):
                    target_name = "pdb" + file_name[3:7] + ".ent.gz"
                else:
                    target_name = "pdb" + file_name[0:4] + ".ent.gz"
                urls_to_target_files.append("https://files.rcsb.org/pub/pdb/data/structures/all/pdb/" + target_name)

            if format_to_download == "SIFTS" or format_to_download == "all":
                if not os.path.exists(default_input_path):
                    os.makedirs(default_input_path)
                if "ent" in file_name and file_name.startswith('pdb'):
                    target_name = file_name[3:7] + ".xml.gz"
                else:
                    target_name = file_name[0:4] + ".xml.gz"
                urls_to_target_files.append("http://ftp.ebi.ac.uk/pub/databases/msd/sifts/xml/" + target_name)

            if format_to_download == "mmCIF_assembly" or format_to_download == "all":
                if not os.path.exists(default_input_path):
                    os.makedirs(default_input_path)
                if "ent" in file_name and file_name.startswith('pdb'):
                    target_name = file_name[3:7] + ".cif.gz"
                else:
                    target_name = file_name[0:4] + ".cif.gz"
                urls_to_target_files.append("https://www.ebi.ac.uk/pdbe/static/entry/" + target_name[:4] + "-assembly.xml")

            if format_to_download == "PDB_assembly":
                default_input_path = default_input_path+f"/{format_to_download}"
                if not os.path.exists(default_input_path):
                    os.makedirs(default_input_path)
                urls_to_target_files.append("https://ftp.wwpdb.org/pub/pdb/data/biounit/PDB/all/" + file_name)

        else:
            raise ValueError("Input file names list is not correct!!! It cannot be less than 4 characters")

    return urls_to_target_files


def download_with_pool(urls_to_target_files=(), default_input_path=os.getcwd()):
    for _ in range(3):
        try:
            file_name_start_pos = urls_to_target_files.rfind("/") + 1
            format_start_pos = file_name_start_pos - 4
            file_name = urls_to_target_files[file_name_start_pos:]
            format_of_db = urls_to_target_files[format_start_pos:format_start_pos + 3]

            r = requests.get(urls_to_target_files, stream=True, timeout=10)

            if format_of_db == "CIF":
                if r.status_code == requests.codes.ok:
                    with open(default_input_path + "/" + file_name, 'wb') as f:
                        for data in r:
                            f.write(data)

            if format_of_db == "pdb":
                if r.status_code == requests.codes.ok:
                    with open(default_input_path + "/" + file_name, 'wb') as f:
                        for data in r:
                            f.write(data)

            if format_of_db == "xml":
                if r.status_code == requests.codes.ok:
                    with open(default_input_path + "/" + file_name, 'wb') as f:
                        for data in r:
                            f.write(data)

            if format_of_db == "all":
                if r.status_code == requests.codes.ok:
                    with open(default_input_path + "/" + file_name, 'wb') as f:
                        for data in r:
                            f.write(data)

            if format_of_db == "try":
                if r.status_code == requests.codes.ok:
                    root = ET.fromstring(r.text)
                    for n in root:
                        compos_ID_list = list(n.attrib.items())
                        if compos_ID_list[1][0] == "id":
                            req_child = requests.get(
                                "https://www.ebi.ac.uk/pdbe/static/entry/" + file_name[0:4] + "-assembly-" + compos_ID_list[1][1] + ".cif.gz",
                                stream=True)
                            if req_child.status_code == requests.codes.ok:
                                with open(default_input_path_to_mmCIF_assembly + "/" + file_name[0:4] + "-assembly-" + compos_ID_list[1][1] + ".cif.gz",
                                          'wb') as f:
                                    for data in req_child:
                                        f.write(data)

        except requests.exceptions.RequestException as err:
            print(err)
            time.sleep(5)
            continue

        break


def run_downloads_with_ThreadPool(format_to_download="mmCIF", urls_to_target=(), default_input_path=os.getcwd()):
    for i in range(3):
        executor = ThreadPoolExecutor()
        partial_download_with_pool = partial(download_with_pool, default_input_path=default_input_path)

        jobs = [executor.submit(partial_download_with_pool, url) for url in urls_to_target]

        for _ in tqdm.tqdm(as_completed(jobs), total=len(jobs), miniters=1, position=0,
                           leave=True, desc="Downloading " + format_to_download + " files"):
            pass

        files_targeted = list()
        format_of_db = 0
        for url in urls_to_target:
            file_name_start_pos = url.rfind("/") + 1
            file_name = url[file_name_start_pos:]
            files_targeted.append(file_name)
            format_start_pos = file_name_start_pos - 4
            format_of_db = url[format_start_pos:format_start_pos + 3]

        if format_of_db == "CIF":
            input_files = look_what_is_inside("mmCIF",  default_input_path=os.getcwd())
        elif format_of_db == "pdb":
            input_files = look_what_is_inside('PDB', default_input_path=os.getcwd())
        elif format_of_db == "xml":
            input_files = look_what_is_inside('SIFTS', default_input_path=os.getcwd())
        elif format_of_db == "all":
            input_files = look_what_is_inside('PDB_assembly', default_input_path=os.getcwd())
        elif format_of_db == "try":
            input_files = look_what_is_inside('mmCIF_assembly', default_input_path=os.getcwd())
        else:
            input_files = set()

        output_4char = set()
        for n in input_files:
            output_4char.add(n[:4])

        new_round_files_targeted = set()
        for n in files_targeted:
            if n[:4] in output_4char:
                continue
            else:
                new_round_files_targeted.add(n)
        files_targeted = new_round_files_targeted

        if len(files_targeted) == 0:
            break


# if __name__ == '__main__':
#     start = time.time()
