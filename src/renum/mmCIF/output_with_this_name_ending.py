from src.download.modules import *
from src.download.compressor import compress_output_files


def output_with_this_name_ending(name_ending, path, mmcif_dict, mmCIF_name, gzip_mode, current_directory):
    mmCIF_name = mmCIF_name[:mmCIF_name.rfind(".cif.gz")]
    os.chdir(path)
    io = MMCIFIO()
    io.set_dict(mmcif_dict)
    io.save(mmCIF_name + name_ending)
    if gzip_mode == "on":
        compress_output_files(mmCIF_name + name_ending, gzip_mode)
        os.remove(mmCIF_name + name_ending)
    os.chdir(current_directory)
