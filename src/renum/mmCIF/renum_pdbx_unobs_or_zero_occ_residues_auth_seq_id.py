from src.download.modules import *


def renum_pdbx_unobs_or_zero_occ_residues_auth_seq_id(mmcif_dict, df_PDBe_PDB_UniProt, default_mmCIF_num):
    try:
        _pdbx_unobs_or_zero_occ_residues_auth_asym_id = mmcif_dict["_pdbx_unobs_or_zero_occ_residues.auth_asym_id"]
        _pdbx_unobs_or_zero_occ_residues_auth_comp_id = mmcif_dict["_pdbx_unobs_or_zero_occ_residues.auth_comp_id"]
        _pdbx_unobs_or_zero_occ_residues_auth_seq_id = mmcif_dict["_pdbx_unobs_or_zero_occ_residues.auth_seq_id"]
        if type(_pdbx_unobs_or_zero_occ_residues_auth_asym_id) == str:
            _pdbx_unobs_or_zero_occ_residues_auth_asym_id = [_pdbx_unobs_or_zero_occ_residues_auth_asym_id]
            _pdbx_unobs_or_zero_occ_residues_auth_comp_id = [_pdbx_unobs_or_zero_occ_residues_auth_comp_id]
            _pdbx_unobs_or_zero_occ_residues_auth_seq_id = [_pdbx_unobs_or_zero_occ_residues_auth_seq_id]

        _pdbx_unobs_or_zero_occ_residues_label_asym_id = mmcif_dict["_pdbx_unobs_or_zero_occ_residues.label_asym_id"]
        _pdbx_unobs_or_zero_occ_residues_label_comp_id = mmcif_dict["_pdbx_unobs_or_zero_occ_residues.label_comp_id"]
        _pdbx_unobs_or_zero_occ_residues_label_seq_id = mmcif_dict["_pdbx_unobs_or_zero_occ_residues.label_seq_id"]
        if type(_pdbx_unobs_or_zero_occ_residues_label_asym_id) == str:
            _pdbx_unobs_or_zero_occ_residues_label_asym_id = [_pdbx_unobs_or_zero_occ_residues_label_asym_id]
            _pdbx_unobs_or_zero_occ_residues_label_comp_id = [_pdbx_unobs_or_zero_occ_residues_label_comp_id]
            _pdbx_unobs_or_zero_occ_residues_label_seq_id = [_pdbx_unobs_or_zero_occ_residues_label_seq_id]

        _pdbx_unobs_or_zero_occ_residues_auth = list(zip(_pdbx_unobs_or_zero_occ_residues_auth_seq_id,
                                                         _pdbx_unobs_or_zero_occ_residues_auth_comp_id,
                                                         _pdbx_unobs_or_zero_occ_residues_auth_asym_id))
        _pdbx_unobs_or_zero_occ_residues_label = list(zip(_pdbx_unobs_or_zero_occ_residues_label_seq_id,
                                                          _pdbx_unobs_or_zero_occ_residues_label_comp_id,
                                                          _pdbx_unobs_or_zero_occ_residues_label_asym_id))

        df_mmCIF_pdbx_unobs_or_zero_occ_residues_auth = pd.DataFrame(zip(_pdbx_unobs_or_zero_occ_residues_label,
                                                                         _pdbx_unobs_or_zero_occ_residues_auth))
        df_mmCIF_pdbx_unobs_or_zero_occ_residues_auth = df_mmCIF_pdbx_unobs_or_zero_occ_residues_auth.rename(
            columns={0: "_pdbx_unobs_or_zero_occ_residues_label", 1: "_pdbx_unobs_or_zero_occ_residues_auth"})

        df_pdbx_unobs_or_zero_occ_residues_auth_final = df_mmCIF_pdbx_unobs_or_zero_occ_residues_auth.merge(
            df_PDBe_PDB_UniProt, left_on="_pdbx_unobs_or_zero_occ_residues_label", right_on="PDBe", how='left')
        df_pdbx_unobs_or_zero_occ_residues_auth_final = df_pdbx_unobs_or_zero_occ_residues_auth_final["Three_Rows_CIF_Num_Uni"]

        FINAL_RES_NUM_for_df_pdbx_unobs_or_zero_occ_residues_auth_final = list()

        for n in df_pdbx_unobs_or_zero_occ_residues_auth_final:
            try:
                if n[0][0] != ".":
                    FINAL_RES_NUM_for_df_pdbx_unobs_or_zero_occ_residues_auth_final.append(str(n[1]))
                else:
                    FINAL_RES_NUM_for_df_pdbx_unobs_or_zero_occ_residues_auth_final.append(str((int(n[1]) + default_mmCIF_num)))
            except TypeError:
                FINAL_RES_NUM_for_df_pdbx_unobs_or_zero_occ_residues_auth_final.append("?")

        mmcif_dict["_pdbx_unobs_or_zero_occ_residues.auth_seq_id"] = FINAL_RES_NUM_for_df_pdbx_unobs_or_zero_occ_residues_auth_final

    except KeyError:
        pass
