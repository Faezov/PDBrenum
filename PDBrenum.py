from src.download.modules import *
from src.download.lefttorenumber import left_to_renumber_mmCIF, left_to_renumber_PDB
from src.download.inputtextfileparser import input_text_file_parser
from src.download.supremedownloader import supreme_download_master
from src.download.lookfilesinside import look_what_is_inside
from src.download.downloadwithThreadPool import run_downloads_with_ThreadPool, url_formation_for_pool

from src.renum.PDB.new_PDB import ProcessPool_run_renum_PDB
from src.renum.shared.write_log import log_writer
from src.renum.mmCIF.ProcessPool_run_renum_mmCIF import ProcessPool_run_renum_mmCIF
from src.renum.mmCIF.new_mmCIF import master_mmCIF_renumber_function

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import argparse
import os

# Centralize defaults
DEFAULT_PATH = os.getcwd()
DEFAULT_MMCIF_NUM = 50000
DEFAULT_PDB_NUM = 5000
DEFAULT_GZIP_MODE = 'on'
DEFAULT_NPROC = None
exception_AccessionIDs = ["P42212", "Q17104", "Q27903", "Q93125", "P03069", "D3DLN9", "Q96UT3", "P0ABE7", "P00192",
                          "P76805", "Q8XCE3", "P00720", "Q38170", "Q94N07", "P0AEX9", "P02928", "Q2M6S0"]

# Initialize the argument parser
argpar = argparse.ArgumentParser(description='Command line tool for PDBrenum.')

# Add argument groups for better organization
group_download = argpar.add_argument_group('Download options')
group_renumber = argpar.add_argument_group('Renumber options')
group_settings = argpar.add_argument_group('Settings')

# Populate argument groups
group_download.add_argument("--download_from_text_file", type=str, help="Download from a list provided in a text file.")
group_download.add_argument("--download_from_list_of_arguments", nargs="+", help="Download from a list of arguments provided.")

group_renumber.add_argument("--renumber_from_text_file", type=str, help="Renumber from a list provided in a text file.")
group_renumber.add_argument("--renumber_from_list_of_arguments", nargs="*", help="Renumber from a list of arguments provided.")

# Settings
group_settings.add_argument("--set_default_path", type=str, default=DEFAULT_PATH, help="Set the default path for downloads and renumbering.")
group_settings.add_argument("--set_default_mmCIF_num", type=int, default=DEFAULT_MMCIF_NUM, help="Set the default number for mmCIF.")
group_settings.add_argument("--set_default_PDB_num", type=int, default=DEFAULT_PDB_NUM, help="Set the default number for PDB.")
group_settings.add_argument("--set_number_of_processes", type=int, default=DEFAULT_NPROC, help="Set the number of processes.")
group_settings.add_argument("--gzip", dest='gzip_mode', action='store_true', help="Enable gzip mode (default).")
group_settings.add_argument("--no-gzip", dest='gzip_mode', action='store_false', help="Disable gzip mode.")

# Set defaults
argpar.set_defaults(gzip_mode=DEFAULT_GZIP_MODE)

# Parse the arguments
args = argpar.parse_args()

# Post-process and apply the arguments
nproc = args.set_number_of_processes or os.cpu_count()  # Example post-processing

# Now, args.gzip_mode will be True if --gzip is passed, False if --no-gzip is passed,
# or the default value if neither is passed.
gzip_mode = 'on' if args.gzip_mode else 'off'


if __name__ == "__main__":
    from pathlib import Path
    import gzip
    import os
    from typing import Callable, Optional, Union
    import Bio.PDB.MMCIF2Dict

    from src.download.downloadwithThreadPool import download_file
    from src.renum.mmCIF.new_mmCIF import SIFTS_tree_parser


    def download_file_general(file_type: str, file_name: str, input_path: Path) -> bool:
        """Attempts to download a given file to the specified path."""
        url_path = url_formation_for_pool(file_type,[file_name], str(input_path))[0]
        return download_file(url_path)  # Assume this function returns True on success


    def try_file_parser(default_path: Path, file_name: str,
                        parser_function: Callable[[Path], Union[Bio.PDB.MMCIF2Dict.MMCIF2Dict, Optional[any]]],
                        file_type: str) -> Union[Bio.PDB.MMCIF2Dict.MMCIF2Dict, Optional[any], None]:
        """General function to attempt loading a file into a parser, redownloading up to 3 times if necessary."""
        input_path = default_path / file_type
        input_path.mkdir(parents=True, exist_ok=True)
        file_path = input_path / file_name
        print(file_path)

        for attempt in range(3):
            try:
                with gzip.open(file_path, 'rt') as file:
                    return parser_function(file)
            except (EOFError, ValueError, OSError) as e:
                print(f"Error processing {file_name}: {e}. Attempting to redownload.")
                file_path.unlink(missing_ok=True)  # Remove potentially corrupt file
                if not download_file_general(file_type, file_name, input_path):
                    print(f"Failed to download {file_name}.")

        return None



    print("Starting PDBrenum...")
    DEFAULT_PATH = Path("mypath")
    mmCIF_files = "2aa3.cif.gz"
    SIFTS_files = "2aa3.xml.gz"

    mmcif_dict = try_file_parser(DEFAULT_PATH, mmCIF_files, Bio.PDB.MMCIF2Dict.MMCIF2Dict,
                                 file_type="mmCIF_assembly" if "assembly" in mmCIF_files else "mmCIF")

    SIFTS_data = try_file_parser(DEFAULT_PATH, SIFTS_files,SIFTS_tree_parser, file_type="SIFTS")

    #print(mmcif_dict)
    #print(SIFTS_data)


    import xml.etree.ElementTree as ET
    import gzip
    from pathlib import Path

    import xml.etree.ElementTree as ET
    import gzip


    def SIFTS_tree_parser(handle_SIFTS):
        tree = ET.parse(handle_SIFTS)
        root = tree.getroot()

        UniProt_conversion_dict = dict()

        for entity in root:
            if entity.tag.endswith("entity"):
                entity_chainID_list = list(entity.attrib.items())
                if entity_chainID_list[0][0] == "type" and entity_chainID_list[0][1] == "protein":
                    for segment in entity:
                        for listResidue in segment:
                            if listResidue.tag.endswith("listMapRegion"):
                                for mapRegion in listResidue:
                                    for db in mapRegion:
                                        dbSource_UniProt = list(db.attrib.items())
                                        if "dbSource" == dbSource_UniProt[0][0] and "UniProt" == dbSource_UniProt[0][1]:
                                            if db.text is None:
                                                UniProt = dbSource_UniProt[2][1]
                                            else:
                                                Human_readable = db.text
                                                UniProt_conversion_dict[UniProt] = Human_readable

        return UniProt_conversion_dict




    # Path to the SIFTS XML file
    sifts_file_path = Path('./mypath/SIFTS/2aa3.xml.gz')

    # Parsing the SIFTS XML file
    with gzip.open(sifts_file_path, 'rt') as file:
        uniProt_conversion_dict = SIFTS_tree_parser(file)

    # Printing the result
    print(uniProt_conversion_dict)













    # This refactoring maintains the original functionality, aiming to make the process more structured and readable.

    # DEFAULT_PATH = Path(DEFAULT_PATH)
    # mmcif_dict = try_MMCIF2Dict(DEFAULT_PATH, mmCIF_files)

    #SIFTS_data = try_SIFTS_tree_parser(DEFAULT_PATH, SIFTS_files)
    #print(mmcif_dict)

    ####################################################################################################################
    # PARTIAL DB WORK #
    ####################################################################################################################

    # RENUMBER
    # RENUMBER FROM TEXT FILE or RENUMBER FROM LIST OF ARGUMENTS
    # if args.renumber_from_text_file or args.renumber_from_list_of_arguments:
    #     if args.renumber_from_text_file:
    #         parsed_input_text = (input_text_file_parser(args.renumber_from_text_file))
    #     else:
    #         parsed_input_text = args.renumber_from_list_of_arguments
    #
    #     if args.all_formats:
    #         urls_to_target_mmCIF_files = url_formation_for_pool("mmCIF", parsed_input_text, default_path=DEFAULT_PATH)
    #         urls_to_target_mmCIF_assembly_files = url_formation_for_pool("mmCIF_assembly", parsed_input_text, default_path=DEFAULT_PATH)
    #         urls_to_target_PDB_files = url_formation_for_pool("PDB", parsed_input_text, default_path=DEFAULT_PATH)
    #         urls_to_target_SIFTS_files = url_formation_for_pool("SIFTS", parsed_input_text, default_path=DEFAULT_PATH)
    #
    #         run_downloads_with_ThreadPool("mmCIF", urls_to_target_mmCIF_files, default_path=DEFAULT_PATH)
    #         run_downloads_with_ThreadPool("mmCIF_assembly", urls_to_target_mmCIF_assembly_files,default_path=DEFAULT_PATH)
    #         run_downloads_with_ThreadPool("PDB", urls_to_target_PDB_files, default_path=DEFAULT_PATH)
    #         run_downloads_with_ThreadPool("SIFTS", urls_to_target_SIFTS_files, default_path=DEFAULT_PATH)
    #
    #         # renum PDB
    #         passed_as_arg_file_4Char_PDB = list()
    #         for file_name in parsed_input_text:
    #             passed_as_arg_file_4Char_PDB.append(file_name[:4])
    #         input_PDB_files_were_found = look_what_is_inside("PDB", default_path=DEFAULT_PATH)
    #         target_files_list_PDB = list()
    #         for file_name in input_PDB_files_were_found:
    #             if file_name[3:7] in passed_as_arg_file_4Char_PDB:
    #                 target_files_list_PDB.append(file_name)
    #         ProcessPool_run_renum_PDB("PDB", target_files_list_PDB, DEFAULT_PATH, DEFAULT_PATH, DEFAULT_PDB_NUM, gzip_mode, exception_AccessionIDs, nproc)
    #
    #         # renum mmCIF_assembly
    #         input_mmCIF_files_were_found = look_what_is_inside("mmCIF_assembly", default_path=DEFAULT_PATH)
    #         passed_as_arg_file_4Char_mmCIF = list()
    #         for file_name in parsed_input_text:
    #             passed_as_arg_file_4Char_mmCIF.append(file_name[:4])
    #         target_files_list_mmCIF = list()
    #         for file_name in input_mmCIF_files_were_found:
    #             if file_name[:4] in passed_as_arg_file_4Char_mmCIF:
    #                 target_files_list_mmCIF.append(file_name)
    #
    #         ProcessPool_run_renum_mmCIF("mmCIF_assembly", target_files_list_mmCIF, DEFAULT_PATH,
    #                                     DEFAULT_MMCIF_NUM, gzip_mode, exception_AccessionIDs, nproc)
    #
    #         # renum mmCIF
    #         input_mmCIF_files_were_found = look_what_is_inside("mmCIF", default_path=DEFAULT_PATH)
    #         passed_as_arg_file_4Char_mmCIF = list()
    #         for file_name in parsed_input_text:
    #             passed_as_arg_file_4Char_mmCIF.append(file_name[:4])
    #         target_files_list_mmCIF = list()
    #         for file_name in input_mmCIF_files_were_found:
    #             if file_name[:4] in passed_as_arg_file_4Char_mmCIF:
    #                 target_files_list_mmCIF.append(file_name)
    #         res = ProcessPool_run_renum_mmCIF("mmCIF", target_files_list_mmCIF, DEFAULT_PATH,
    #                                           DEFAULT_MMCIF_NUM, gzip_mode, exception_AccessionIDs, nproc)
    #         log_writer(res)
