from src.download.modules import *


def renum_pdbx_nonpoly_scheme_auth_seq_num(mmcif_dict, df_final_dropped_dup, default_mmCIF_num):
    try:
        _pdbx_nonpoly_scheme_pdb_seq_num = mmcif_dict["_pdbx_nonpoly_scheme.pdb_seq_num"]
        _pdbx_nonpoly_scheme_auth_seq_num = mmcif_dict["_pdbx_nonpoly_scheme.auth_seq_num"]
        _pdbx_nonpoly_scheme_pdb_mon_id = mmcif_dict["_pdbx_nonpoly_scheme.pdb_mon_id"]
        _pdbx_nonpoly_scheme_auth_mon_id = mmcif_dict["_pdbx_nonpoly_scheme.auth_mon_id"]
        _pdbx_nonpoly_scheme_pdb_strand_id = mmcif_dict["_pdbx_nonpoly_scheme.pdb_strand_id"]
    except KeyError:
        try:
            _pdbx_nonpoly_scheme_pdb_seq_num = mmcif_dict["_pdbe_orig_nonpoly_scheme.pdb_seq_num"]
            _pdbx_nonpoly_scheme_auth_seq_num = mmcif_dict["_pdbe_orig_nonpoly_scheme.auth_seq_num"]
            _pdbx_nonpoly_scheme_pdb_mon_id = mmcif_dict["_pdbe_orig_nonpoly_scheme.pdb_mon_id"]
            _pdbx_nonpoly_scheme_auth_mon_id = mmcif_dict["_pdbe_orig_nonpoly_scheme.auth_mon_id"]
            _pdbx_nonpoly_scheme_pdb_strand_id = mmcif_dict["_pdbe_orig_nonpoly_scheme.pdb_strand_id"]
        except KeyError:
            return 0

    if type(_pdbx_nonpoly_scheme_pdb_strand_id) == str:
        _pdbx_nonpoly_scheme_pdb_seq_num = [_pdbx_nonpoly_scheme_pdb_seq_num]
        _pdbx_nonpoly_scheme_auth_seq_num = [_pdbx_nonpoly_scheme_auth_seq_num]
        _pdbx_nonpoly_scheme_pdb_mon_id = [_pdbx_nonpoly_scheme_pdb_mon_id]
        _pdbx_nonpoly_scheme_auth_mon_id = [_pdbx_nonpoly_scheme_auth_mon_id]
        _pdbx_nonpoly_scheme_pdb_strand_id = [_pdbx_nonpoly_scheme_pdb_strand_id]

    mmCIF_pdbx_nonpoly_scheme_pdb = list(
        zip(_pdbx_nonpoly_scheme_pdb_seq_num, _pdbx_nonpoly_scheme_pdb_mon_id, _pdbx_nonpoly_scheme_pdb_strand_id))
    mmCIF_pdbx_nonpoly_scheme_auth = list(
        zip(_pdbx_nonpoly_scheme_auth_seq_num, _pdbx_nonpoly_scheme_auth_mon_id, _pdbx_nonpoly_scheme_pdb_strand_id))

    df_mmCIF_pdbx_nonpoly_scheme = pd.DataFrame(zip(mmCIF_pdbx_nonpoly_scheme_pdb, mmCIF_pdbx_nonpoly_scheme_auth))
    df_mmCIF_pdbx_nonpoly_scheme = df_mmCIF_pdbx_nonpoly_scheme.rename(columns={0: "pdbx_nonpoly_scheme_pdb", 1: "pdbx_nonpoly_scheme_auth"})

    df_pdbx_nonpoly_scheme_auth_final = df_mmCIF_pdbx_nonpoly_scheme.merge(df_final_dropped_dup, left_on="pdbx_nonpoly_scheme_auth",
                                                                           right_on="auth_mmCIF", how='left')
    df_pdbx_nonpoly_scheme_auth_final['Three_Rows_CIF_Num_Uni'] = df_pdbx_nonpoly_scheme_auth_final['Three_Rows_CIF_Num_Uni'].replace(np.nan,
                                                                                                                                      "Not in SIFTS")
    df_pdbx_nonpoly_scheme_auth_final["Three_Rows_CIF_Num_Uni_new"] = np.where(
        df_pdbx_nonpoly_scheme_auth_final['Three_Rows_CIF_Num_Uni'] != "Not in SIFTS",
        df_pdbx_nonpoly_scheme_auth_final['Three_Rows_CIF_Num_Uni'],
        df_pdbx_nonpoly_scheme_auth_final["pdbx_nonpoly_scheme_auth"])
    df_pdbx_nonpoly_scheme_auth_final.loc[:, 'New_Three_Rows_CIF_Num_Uni'] = df_pdbx_nonpoly_scheme_auth_final.Three_Rows_CIF_Num_Uni_new.map(
        lambda x: x if type(x) == list else [x, x[0], x])

    df_pdbx_nonpoly_scheme_auth_final = df_pdbx_nonpoly_scheme_auth_final["New_Three_Rows_CIF_Num_Uni"]
    FINAL_RES_NUM_for_df_pdbx_nonpoly_scheme_auth_final = list()
    for n in df_pdbx_nonpoly_scheme_auth_final:
        try:
            if n[0] == n[2]:
                FINAL_RES_NUM_for_df_pdbx_nonpoly_scheme_auth_final.append(str((int(n[1]) + default_mmCIF_num)))
            elif n[0][0] != ".":
                FINAL_RES_NUM_for_df_pdbx_nonpoly_scheme_auth_final.append(str(n[1]))
            else:
                FINAL_RES_NUM_for_df_pdbx_nonpoly_scheme_auth_final.append(str((int(n[1]) + default_mmCIF_num)))
        except ValueError:
            FINAL_RES_NUM_for_df_pdbx_nonpoly_scheme_auth_final.append(str(int(''.join(filter(lambda i: i.isdigit(), n[1]))) + default_mmCIF_num))
    try:
        mmcif_dict["_pdbx_nonpoly_scheme.auth_seq_num"]
        mmcif_dict["_pdbx_nonpoly_scheme.auth_seq_num"] = FINAL_RES_NUM_for_df_pdbx_nonpoly_scheme_auth_final
    except KeyError:
        try:
            mmcif_dict["_pdbe_orig_nonpoly_scheme.auth_seq_num"] = FINAL_RES_NUM_for_df_pdbx_nonpoly_scheme_auth_final
        except KeyError:
            pass
