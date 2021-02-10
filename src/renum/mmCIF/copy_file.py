from src.download.modules import *


def copy_file(inpath, file_name, outpath, postfix, gzip_mode):
    mmCIF_name = file_name[:file_name.rfind(".cif.gz")]
    absolute_path_in = inpath + "/" + file_name
    absolute_path_out = outpath + "/" + mmCIF_name + postfix
    if gzip_mode == "off":
        with gzip.open(absolute_path_in, 'rb') as f_in:
            with open(absolute_path_out[:-3], 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    else:
        shutil.copyfile(absolute_path_in, absolute_path_out)
