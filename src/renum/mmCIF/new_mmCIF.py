from src.download.modules import *

from src.renum.shared.handling_chain_numbering_clashes import handling_chain_numbering_clashes
from src.renum.shared.renumbered_count_in_chains import renumbered_count_in_chains
from src.renum.shared.try_SIFTS_tree_parser import try_SIFTS_tree_parser
from src.renum.mmCIF.mmCIF_parser import mmCIF_parser

from src.renum.mmCIF.SIFTS_data_parser_for_mmCIF import SIFTS_data_parser_for_mmCIF
from src.renum.mmCIF.copy_file import copy_file
from src.renum.mmCIF.if_no_SIFTS_data_log import if_no_SIFTS_data_log
from src.renum.mmCIF.output_with_this_name_ending import output_with_this_name_ending
from src.renum.mmCIF.try_MMCIF2Dict import try_MMCIF2Dict

from src.renum.mmCIF.renum_pdbx_unobs_or_zero_occ_residues_auth_seq_id import renum_pdbx_unobs_or_zero_occ_residues_auth_seq_id
from src.renum.mmCIF.renum_pdbx_poly_seq_scheme_auth_seq_num import renum_pdbx_poly_seq_scheme_auth_seq_num
from src.renum.mmCIF.renum_pdbx_nonpoly_scheme_auth_seq_num import renum_pdbx_nonpoly_scheme_auth_seq_num
from src.renum.mmCIF.renum_struct_ref_seq_pdbx_auth_seq_align import renum_struct_ref_seq_pdbx_auth_seq_align
from src.renum.mmCIF.renumber_tables import renumber_tables
from src.renum.mmCIF.column_formation import column_formation


def master_mmCIF_renumber_function(input_mmCIF_files_were_found, default_input_path_to_mmCIF,
                                   default_input_path_to_SIFTS, default_output_path_to_mmCIF,
                                   default_mmCIF_num, gzip_mode, exception_AccessionIDs):
    input_mmCIF_assembly_files_were_found_list = list()
    input_mmCIF_assembly_files_were_found_list.append(input_mmCIF_files_were_found)

    for mmCIF_name in input_mmCIF_assembly_files_were_found_list:
        log_message = list()
        SIFTS_name = mmCIF_name[:4] + ".xml.gz"

        # for no SIFTS _no_SIFTS_out.cif.gz
        try:
            gzip.open(Path(str(default_input_path_to_SIFTS) + "/" + SIFTS_name), 'rt')
        except FileNotFoundError:
            mmcif_dict = try_MMCIF2Dict(default_input_path_to_mmCIF, mmCIF_name)
            if mmcif_dict == 0:
                continue
            copy_file(default_input_path_to_mmCIF, mmCIF_name, default_output_path_to_mmCIF, ".cif.gz", gzip_mode)
            log_message = if_no_SIFTS_data_log(mmCIF_name, mmcif_dict, log_message)
            return log_message

        # for zerobyte SIFTS _zerobyte_SIFTS_out.cif.gz
        if os.path.getsize(Path(str(default_input_path_to_SIFTS) + "/" + SIFTS_name)) == 0:
            mmcif_dict = try_MMCIF2Dict(default_input_path_to_mmCIF, mmCIF_name)
            if mmcif_dict == 0:
                continue
            copy_file(default_input_path_to_mmCIF, mmCIF_name, default_output_path_to_mmCIF, ".cif.gz", gzip_mode)
            log_message = if_no_SIFTS_data_log(mmCIF_name, mmcif_dict, log_message)
            return log_message

        # SIFTS files parsed here
        product_tree_SIFTS = try_SIFTS_tree_parser(default_input_path_to_SIFTS, SIFTS_name)
        if product_tree_SIFTS == 0:
            continue
        tuple_PDBe_for_PDB_and_tuple_PDB = product_tree_SIFTS[0]
        tuple_PDBe_for_UniProt_and_tuple_UniProt = product_tree_SIFTS[1]
        UniProt_conversion_dict = product_tree_SIFTS[2]

        # _no UniProt in SIFTS _no_UniProt_in_SIFTS_out.cif.gz
        if tuple_PDBe_for_UniProt_and_tuple_UniProt == list():
            mmcif_dict = try_MMCIF2Dict(default_input_path_to_mmCIF, mmCIF_name)
            if mmcif_dict == 0:
                continue
            copy_file(default_input_path_to_mmCIF, mmCIF_name, default_output_path_to_mmCIF, ".cif.gz", gzip_mode)
            log_message = if_no_SIFTS_data_log(mmCIF_name, mmcif_dict, log_message)
            return log_message

        product_of_SIFTS_data_parser = SIFTS_data_parser_for_mmCIF(tuple_PDBe_for_PDB_and_tuple_PDB,
                                                                   tuple_PDBe_for_UniProt_and_tuple_UniProt,
                                                                   default_mmCIF_num, 'all')
        df_PDBe_PDB_UniProt = product_of_SIFTS_data_parser[1]

        # count numbering changes for log_file
        handling_chain_numbering = handling_chain_numbering_clashes(df_PDBe_PDB_UniProt, exception_AccessionIDs)
        chains_to_change = handling_chain_numbering[0]
        combined_tuple_PDBe_UniProt_AccessionID = handling_chain_numbering[1]
        longest_AccessionID_list = handling_chain_numbering[3]
        chains_to_change_one_to_end = handling_chain_numbering[4]

        product_of_SIFTS_data_parser = SIFTS_data_parser_for_mmCIF(tuple_PDBe_for_PDB_and_tuple_PDB,
                                                                   combined_tuple_PDBe_UniProt_AccessionID,
                                                                   default_mmCIF_num, chains_to_change)
        df_PDBe_PDB_UniProt_without_null_index_PDBe = product_of_SIFTS_data_parser[0]
        df_PDBe_PDB_UniProt = product_of_SIFTS_data_parser[1]

        renumbered_count = renumbered_count_in_chains(chains_to_change_one_to_end, df_PDBe_PDB_UniProt_without_null_index_PDBe,
                                                      mmCIF_name, UniProt_conversion_dict, longest_AccessionID_list)
        chain_total_renum = renumbered_count[0]
        nothing_changed = renumbered_count[1]
        chain_total_renum.append(nothing_changed)
        mod_log_message = chain_total_renum

        # for no change needed _no_change_out.cif.gz
        if nothing_changed == 0:
            copy_file(default_input_path_to_mmCIF, mmCIF_name, default_output_path_to_mmCIF, ".cif.gz", gzip_mode)
            return mod_log_message

        # mmCIF files parsed here
        product_of_mmCIF_parser = mmCIF_parser(mmCIF_name, default_input_path_to_mmCIF, df_PDBe_PDB_UniProt_without_null_index_PDBe,
                                               default_mmCIF_num, chains_to_change)
        df_final_dropped_dup = product_of_mmCIF_parser[0]
        mmcif_dict = product_of_mmCIF_parser[1]

        # for debug only
        # _pdbx_poly_seq_scheme_auth_seq_num_before_change = product_of_mmCIF_parser[2]
        # _atom_site_label_comp_id_list = product_of_mmCIF_parser[3]

        formed_columns = column_formation(mmcif_dict)
        for n in formed_columns:
            auth_comp_id = 0
            auth_seq_id = n[0]
            auth_asym_id = n[1]
            try:
                PDB_ins_code = n[2]
                if "ins_code" not in PDB_ins_code:
                    auth_comp_id = PDB_ins_code
                    PDB_ins_code = 0
            except IndexError:
                PDB_ins_code = 0
            try:
                if auth_comp_id == 0:
                    auth_comp_id = n[3]
            except IndexError:
                auth_comp_id = 0
            renumber_tables(auth_seq_id, auth_asym_id, auth_comp_id, PDB_ins_code, mmcif_dict,
                            df_final_dropped_dup, default_mmCIF_num, chains_to_change)

        # special case tables
        renum_pdbx_unobs_or_zero_occ_residues_auth_seq_id(mmcif_dict, df_PDBe_PDB_UniProt, default_mmCIF_num)
        renum_pdbx_poly_seq_scheme_auth_seq_num(mmcif_dict, df_final_dropped_dup, default_mmCIF_num)
        renum_pdbx_nonpoly_scheme_auth_seq_num(mmcif_dict, df_final_dropped_dup, default_mmCIF_num)
        renum_struct_ref_seq_pdbx_auth_seq_align(mmcif_dict)

        # just out out.cif
        output_with_this_name_ending(".cif", default_output_path_to_mmCIF, mmcif_dict, mmCIF_name=mmCIF_name,
                                     gzip_mode=gzip_mode, current_directory=current_directory)

        return mod_log_message
