import os

from src.download.modules import *
from src.download import lefttodownload, catalogdownloader_bak, lookfilesinside, latestcatreader
from src.download.downloadwithThreadPool import run_downloads_with_ThreadPool, url_formation_for_pool, download_pdb_assemblies_list_with_lxml
from src.download.holdingsdownloader import get_all_pdb_and_sifts


# default_input_path_to_mmCIF = current_directory + "/mmCIF"
# default_input_path_to_PDB = current_directory + "/PDB"
# default_input_path_to_SIFTS = current_directory + "/SIFTS"
# default_output_path_to_mmCIF = current_directory + "/output_mmCIF"
# default_output_path_to_PDB = current_directory + "/output_PDB"
#
# default_input_path_to_mmCIF_assemblies = current_directory + "/mmCIF_assembly"
# default_input_path_to_PDB_assemblies = current_directory + "/PDB_assembly"
# default_output_path_to_mmCIF_assemblies = current_directory + "/output_mmCIF_assembly"
# default_output_path_to_PDB_assemblies = current_directory + "/output_PDB_assembly"


# def supreme_download_master(format_of_db, job_type=None,
#                             default_input_path_to_mmCIF=current_directory + "/mmCIF",
#                             default_input_path_to_PDB=current_directory + "/PDB",
#                             default_input_path_to_SIFTS=current_directory + "/SIFTS",
#                             default_input_path_to_mmCIF_assembly=current_directory + "/mmCIF_assembly",
#                             default_input_path_to_PDB_assembly=current_directory + "/PDB_assembly",
#
#                             default_output_path_to_mmCIF=current_directory + "/output_mmCIF",
#                             default_output_path_to_PDB=current_directory + "/output_PDB",
#                             default_output_path_to_mmCIF_assemblies=current_directory + "/output_mmCIF_assembly",
#                             default_output_path_to_PDB_assemblies=current_directory + "/output_PDB_assembly"):
#
#
#
#     if job_type == "refresh":
#         if os.path.exists(default_input_path_to_SIFTS):
#             shutil.rmtree(default_input_path_to_SIFTS)
#         if format_of_db == "mmCIF":
#             if os.path.exists(default_input_path_to_mmCIF):
#                 shutil.rmtree(default_input_path_to_mmCIF)
#             if os.path.exists(default_output_path_to_mmCIF):
#                 shutil.rmtree(default_output_path_to_mmCIF)
#
#         if format_of_db == "mmCIF_assembly":
#             if os.path.exists(default_input_path_to_mmCIF_assembly):
#                 shutil.rmtree(default_input_path_to_mmCIF_assembly)
#             if os.path.exists(default_output_path_to_mmCIF_assemblies):
#                 shutil.rmtree(default_output_path_to_mmCIF_assemblies)
#
#         if format_of_db == "PDB":
#             if os.path.exists(default_input_path_to_PDB):
#                 shutil.rmtree(default_input_path_to_PDB)
#             if os.path.exists(default_output_path_to_PDB):
#                 shutil.rmtree(default_output_path_to_PDB)
#
#         if format_of_db == "PDB_assembly":
#             if os.path.exists(default_input_path_to_PDB_assembly):
#                 shutil.rmtree(default_input_path_to_PDB_assembly)
#             if os.path.exists(default_output_path_to_PDB_assemblies):
#                 shutil.rmtree(default_output_path_to_PDB_assemblies)
#
#         if format_of_db == "all":
#             if os.path.exists(default_input_path_to_PDB):
#                 shutil.rmtree(default_input_path_to_PDB)
#             if os.path.exists(default_input_path_to_mmCIF):
#                 shutil.rmtree(default_input_path_to_mmCIF)
#             if os.path.exists(default_input_path_to_PDB_assembly):
#                 shutil.rmtree(default_input_path_to_PDB_assembly)
#             if os.path.exists(default_input_path_to_mmCIF_assembly):
#                 shutil.rmtree(default_input_path_to_mmCIF_assembly)
#
#             if os.path.exists(default_output_path_to_mmCIF):
#                 shutil.rmtree(default_output_path_to_mmCIF)
#             if os.path.exists(default_output_path_to_mmCIF_assemblies):
#                 shutil.rmtree(default_output_path_to_mmCIF_assemblies)
#             if os.path.exists(default_output_path_to_PDB):
#                 shutil.rmtree(default_output_path_to_PDB)
#             if os.path.exists(default_output_path_to_PDB_assemblies):
#                 shutil.rmtree(default_output_path_to_PDB_assemblies)
#
#     if format_of_db == "mmCIF":
#         holding = get_all_pdb_and_sifts()
#         all_mmcif_files = holding["mmcif"]
#         all_sifts_files = holding["sifts"]
#
#         try:
#             lefttodownload_mmcif = [fn for fn in all_mmcif_files if fn not in os.listdir(default_input_path_to_mmCIF)]
#             lefttodownload_sifts = [fn for fn in all_sifts_files if fn not in os.listdir(default_input_path_to_SIFTS)]
#         except FileNotFoundError:
#             lefttodownload_mmcif = all_mmcif_files
#             lefttodownload_sifts = all_sifts_files
#
#         urls_to_target_mmCIF_files = url_formation_for_pool("mmCIF", lefttodownload_mmcif, default_input_path_to_mmCIF=default_input_path_to_mmCIF)
#         urls_to_target_SIFTS_files = url_formation_for_pool("SIFTS", lefttodownload_sifts, default_input_path_to_SIFTS=default_input_path_to_SIFTS)
#
#         run_downloads_with_ThreadPool("mmCIF", urls_to_target_mmCIF_files, default_input_path_to_mmCIF=default_input_path_to_mmCIF)
#         run_downloads_with_ThreadPool("SIFTS", urls_to_target_SIFTS_files, default_input_path_to_SIFTS=default_input_path_to_SIFTS)
#
#         return lefttodownload_mmcif
#
#     if format_of_db == "mmCIF_assembly":
#         holding = get_all_pdb_and_sifts()
#         all_mmcif_assembly_files = holding["mmcif_assembly"]
#         all_sifts_files = holding["sifts"]
#
#         try:
#             lefttodownload_mmcif_assembly = [fn for fn in all_mmcif_assembly_files if fn not in os.listdir(default_input_path_to_mmCIF_assembly)]
#             lefttodownload_sifts = [fn for fn in all_sifts_files if fn not in os.listdir(default_input_path_to_SIFTS)]
#         except FileNotFoundError:
#             lefttodownload_mmcif_assembly = all_mmcif_assembly_files
#             lefttodownload_sifts = all_sifts_files
#
#         urls_to_target_mmCIF_assembly_files = url_formation_for_pool("mmCIF_assembly", lefttodownload_mmcif_assembly, default_input_path_to_mmCIF_assembly=default_input_path_to_mmCIF_assembly)
#         urls_to_target_SIFTS_files = url_formation_for_pool("SIFTS", lefttodownload_sifts, default_input_path_to_SIFTS=default_input_path_to_SIFTS)
#
#         run_downloads_with_ThreadPool("mmCIF_assembly", urls_to_target_mmCIF_assembly_files, default_input_path_to_mmCIF_assembly=default_input_path_to_mmCIF_assembly)
#         run_downloads_with_ThreadPool("SIFTS", urls_to_target_SIFTS_files, default_input_path_to_SIFTS=default_input_path_to_SIFTS)
#
#         return lefttodownload_mmcif_assembly
#
#     if format_of_db == "PDB":
#         holding = get_all_pdb_and_sifts()
#         all_pdb_files = holding["pdb"]
#         all_sifts_files = holding["sifts"]
#
#         try:
#             lefttodownload_pdb = [fn for fn in all_pdb_files if fn not in os.listdir(default_input_path_to_PDB)]
#             lefttodownload_sifts = [fn for fn in all_sifts_files if fn not in os.listdir(default_input_path_to_SIFTS)]
#         except FileNotFoundError:
#             lefttodownload_pdb = all_pdb_files
#             lefttodownload_sifts = all_sifts_files
#
#         urls_to_target_PDB_files = url_formation_for_pool("PDB", lefttodownload_pdb, default_input_path_to_PDB=default_input_path_to_PDB)
#         urls_to_target_SIFTS_files = url_formation_for_pool("SIFTS", lefttodownload_sifts, default_input_path_to_SIFTS=default_input_path_to_SIFTS)
#
#         run_downloads_with_ThreadPool("PDB", urls_to_target_PDB_files, default_input_path_to_PDB=default_input_path_to_PDB)
#         run_downloads_with_ThreadPool("SIFTS", urls_to_target_SIFTS_files, default_input_path_to_SIFTS=default_input_path_to_SIFTS)
#
#         return lefttodownload_pdb
#
#     if format_of_db == "PDB_assembly":
#         holding = get_all_pdb_and_sifts()
#         all_pdb_assemblies_files = holding["pdb_assembly"]
#         all_sifts_files = holding["sifts"]
#
#         try:
#             lefttodownload_pdb_assembly = [fn for fn in all_pdb_assemblies_files if fn not in os.listdir(default_input_path_to_PDB_assembly)]
#             lefttodownload_sifts = [fn for fn in all_sifts_files if fn not in os.listdir(default_input_path_to_SIFTS)]
#         except FileNotFoundError:
#             lefttodownload_pdb_assembly = all_pdb_assemblies_files
#             lefttodownload_sifts = all_sifts_files
#
#         urls_to_target_PDB_assembly_files = url_formation_for_pool("PDB_assembly", lefttodownload_pdb_assembly, default_input_path_to_PDB_assembly=default_input_path_to_PDB_assembly)
#         urls_to_target_SIFTS_files = url_formation_for_pool("SIFTS", lefttodownload_sifts, default_input_path_to_SIFTS=default_input_path_to_SIFTS)
#
#         run_downloads_with_ThreadPool("PDB_assembly", urls_to_target_PDB_assembly_files, default_input_path_to_PDB_assembly=default_input_path_to_PDB_assembly)
#         run_downloads_with_ThreadPool("SIFTS", urls_to_target_SIFTS_files, default_input_path_to_SIFTS=default_input_path_to_SIFTS)
#
#         return lefttodownload_pdb_assembly
#
#     if format_of_db == "all":
#         holding = get_all_pdb_and_sifts()
#         all_mmcif_files = holding["mmcif"]
#         all_mmcif_assembly_files = holding["mmcif_assembly"]
#         all_pdb_files = holding["pdb"]
#         all_pdb_assemblies_files = holding["pdb_assembly"]
#         all_sifts_files = holding["sifts"]
#
#         try:
#             lefttodownload_mmcif = [fn for fn in all_mmcif_files if fn not in os.listdir(default_input_path_to_mmCIF)]
#             lefttodownload_mmcif_assembly = [fn for fn in all_mmcif_assembly_files if fn not in os.listdir(default_input_path_to_mmCIF_assembly)]
#             lefttodownload_pdb = [fn for fn in all_pdb_files if fn not in os.listdir(default_input_path_to_PDB)]
#             lefttodownload_pdb_assembly = [fn for fn in all_pdb_assemblies_files if fn not in os.listdir(default_input_path_to_PDB_assembly)]
#             lefttodownload_sifts = [fn for fn in all_sifts_files if fn not in os.listdir(default_input_path_to_SIFTS)]
#         except FileNotFoundError:
#             lefttodownload_mmcif = all_mmcif_files
#             lefttodownload_mmcif_assembly = all_mmcif_assembly_files
#             lefttodownload_pdb = all_pdb_files
#             lefttodownload_pdb_assembly = all_pdb_assemblies_files
#             lefttodownload_sifts = all_sifts_files
#
#         urls_to_target_mmCIF_files = url_formation_for_pool("mmCIF", lefttodownload_mmcif, default_input_path_to_mmCIF=default_input_path_to_mmCIF)
#         urls_to_target_PDB_files = url_formation_for_pool("PDB", lefttodownload_pdb, default_input_path_to_PDB=default_input_path_to_PDB)
#
#         urls_to_target_mmCIF_assembly_files = url_formation_for_pool("mmCIF_assembly", lefttodownload_mmcif_assembly, default_input_path_to_mmCIF_assembly=default_input_path_to_mmCIF_assembly)
#         urls_to_target_PDB_assembly_files = url_formation_for_pool("PDB_assembly", lefttodownload_pdb_assembly, default_input_path_to_PDB_assembly=default_input_path_to_PDB_assembly)
#         urls_to_target_SIFTS_files = url_formation_for_pool("SIFTS", lefttodownload_sifts, default_input_path_to_SIFTS=default_input_path_to_SIFTS)
#
#         run_downloads_with_ThreadPool("mmCIF", urls_to_target_mmCIF_files, default_input_path_to_mmCIF=default_input_path_to_mmCIF)
#         run_downloads_with_ThreadPool("PDB", urls_to_target_PDB_files, default_input_path_to_PDB=default_input_path_to_PDB)
#
#         run_downloads_with_ThreadPool("mmCIF_assembly", urls_to_target_mmCIF_assembly_files, default_input_path_to_mmCIF_assembly=default_input_path_to_mmCIF_assembly)
#         run_downloads_with_ThreadPool("PDB_assembly", urls_to_target_PDB_assembly_files, default_input_path_to_PDB_assembly=default_input_path_to_PDB_assembly)
#
#         run_downloads_with_ThreadPool("SIFTS", urls_to_target_SIFTS_files, default_input_path_to_SIFTS=default_input_path_to_SIFTS)
#
#         return [lefttodownload_mmcif, lefttodownload_pdb, lefttodownload_mmcif_assembly, lefttodownload_pdb_assembly]


