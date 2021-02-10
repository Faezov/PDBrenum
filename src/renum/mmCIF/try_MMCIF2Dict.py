from src.download.modules import *
from src.download.downloadwithThreadPool import download_with_pool, url_formation_for_pool


def try_MMCIF2Dict(default_input_path_to_mmCIF, mmCIF_name):
    mmcif_dict = 0
    for _ in range(3):
        try:
            mmcif_dict = Bio.PDB.MMCIF2Dict.MMCIF2Dict(gzip.open(Path(str(default_input_path_to_mmCIF) + "/" + mmCIF_name), 'rt'))
            break
        except EOFError:
            os.remove(Path(str(default_input_path_to_mmCIF) + "/" + mmCIF_name))
            if "assembly" in mmCIF_name:
                download_with_pool(url_formation_for_pool("mmCIF_assembly", [mmCIF_name])[0])
            else:
                download_with_pool(url_formation_for_pool("mmCIF", [mmCIF_name])[0])
        except ValueError:
            os.remove(Path(str(default_input_path_to_mmCIF) + "/" + mmCIF_name))
            if "assembly" in mmCIF_name:
                download_with_pool(url_formation_for_pool("mmCIF_assembly", [mmCIF_name])[0])
            else:
                download_with_pool(url_formation_for_pool("mmCIF", [mmCIF_name])[0])
        except OSError:
            if "assembly" in mmCIF_name:
                download_with_pool(url_formation_for_pool("mmCIF_assembly", [mmCIF_name])[0])
            else:
                download_with_pool(url_formation_for_pool("mmCIF", [mmCIF_name])[0])
    return mmcif_dict
