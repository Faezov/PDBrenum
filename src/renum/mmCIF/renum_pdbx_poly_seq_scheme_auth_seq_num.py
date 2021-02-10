from src.download.modules import *


def renum_pdbx_poly_seq_scheme_auth_seq_num(mmcif_dict, df_final_dropped_dup, default_mmCIF_num):
    try:
        _pdbx_poly_seq_scheme_pdb_seq_num = mmcif_dict["_pdbx_poly_seq_scheme.pdb_seq_num"]
        _pdbx_poly_seq_scheme_auth_seq_num = mmcif_dict["_pdbx_poly_seq_scheme.auth_seq_num"]
        _pdbx_poly_seq_scheme_pdb_mon_id = mmcif_dict["_pdbx_poly_seq_scheme.pdb_mon_id"]
        _pdbx_poly_seq_scheme_auth_mon_id = mmcif_dict["_pdbx_poly_seq_scheme.auth_mon_id"]
        _pdbx_poly_seq_scheme_pdb_strand_id = mmcif_dict["_pdbx_poly_seq_scheme.pdb_strand_id"]
        _pdbx_poly_seq_scheme_pdb_ins_code = mmcif_dict["_pdbx_poly_seq_scheme.pdb_ins_code"]
    except KeyError:
        try:
            _pdbx_poly_seq_scheme_pdb_seq_num = mmcif_dict["_pdbe_orig_poly_seq_scheme.pdb_seq_num"]
            _pdbx_poly_seq_scheme_auth_seq_num = mmcif_dict["_pdbe_orig_poly_seq_scheme.auth_seq_num"]
            _pdbx_poly_seq_scheme_pdb_mon_id = mmcif_dict["_pdbe_orig_poly_seq_scheme.pdb_mon_id"]
            _pdbx_poly_seq_scheme_auth_mon_id = mmcif_dict["_pdbe_orig_poly_seq_scheme.auth_mon_id"]
            _pdbx_poly_seq_scheme_pdb_strand_id = mmcif_dict["_pdbe_orig_poly_seq_scheme.pdb_strand_id"]
            _pdbx_poly_seq_scheme_pdb_ins_code = mmcif_dict["_pdbe_orig_poly_seq_scheme.pdb_ins_code"]
        except KeyError:
            return 0

    if type(_pdbx_poly_seq_scheme_pdb_strand_id) == str:
        _pdbx_poly_seq_scheme_pdb_seq_num = [_pdbx_poly_seq_scheme_pdb_seq_num]
        _pdbx_poly_seq_scheme_auth_seq_num = [_pdbx_poly_seq_scheme_auth_seq_num]
        _pdbx_poly_seq_scheme_pdb_mon_id = [_pdbx_poly_seq_scheme_pdb_mon_id]
        _pdbx_poly_seq_scheme_auth_mon_id = [_pdbx_poly_seq_scheme_auth_mon_id]
        _pdbx_poly_seq_scheme_pdb_strand_id = [_pdbx_poly_seq_scheme_pdb_strand_id]
        _pdbx_poly_seq_scheme_pdb_ins_code = [_pdbx_poly_seq_scheme_pdb_ins_code]

    mmCIF_pdbx_poly_seq_scheme_pdb = list(
        zip(_pdbx_poly_seq_scheme_pdb_seq_num, _pdbx_poly_seq_scheme_pdb_mon_id, _pdbx_poly_seq_scheme_pdb_strand_id))
    mmCIF_pdbx_poly_seq_scheme_auth = list(
        zip(_pdbx_poly_seq_scheme_auth_seq_num, _pdbx_poly_seq_scheme_auth_mon_id, _pdbx_poly_seq_scheme_pdb_strand_id))

    df_mmCIF_pdbx_poly_seq_scheme = pd.DataFrame(
        zip(mmCIF_pdbx_poly_seq_scheme_pdb, mmCIF_pdbx_poly_seq_scheme_auth, _pdbx_poly_seq_scheme_pdb_ins_code))
    df_mmCIF_pdbx_poly_seq_scheme = df_mmCIF_pdbx_poly_seq_scheme.rename(
        columns={0: "pdbx_poly_seq_scheme_pdb", 1: "pdbx_poly_seq_scheme_auth", 2: "pdbx_poly_seq_scheme_pdb_ins_code"})

    df_mmCIF_pdbx_poly_seq_scheme["PDBnum_with_inc_code"] = np.where(df_mmCIF_pdbx_poly_seq_scheme['pdbx_poly_seq_scheme_pdb_ins_code'] != ".",
                                                                     (df_mmCIF_pdbx_poly_seq_scheme['pdbx_poly_seq_scheme_auth'].apply(lambda x: x[0])
                                                                      + df_mmCIF_pdbx_poly_seq_scheme['pdbx_poly_seq_scheme_pdb_ins_code'].apply(
                                                                                 lambda y: y[0]) + ", "
                                                                      + df_mmCIF_pdbx_poly_seq_scheme['pdbx_poly_seq_scheme_auth'].apply(
                                                                                 lambda x: x[1]) + ", "
                                                                      + df_mmCIF_pdbx_poly_seq_scheme['pdbx_poly_seq_scheme_auth'].apply(
                                                                                 lambda x: x[2])),
                                                                     df_mmCIF_pdbx_poly_seq_scheme['pdbx_poly_seq_scheme_pdb_ins_code'])
    df_mmCIF_pdbx_poly_seq_scheme["PDBnum_with_inc_code_cor"] = np.where(df_mmCIF_pdbx_poly_seq_scheme["PDBnum_with_inc_code"] != ".",
                                                                         df_mmCIF_pdbx_poly_seq_scheme["PDBnum_with_inc_code"].apply(
                                                                             lambda x: tuple(x.split(","))),
                                                                         df_mmCIF_pdbx_poly_seq_scheme["pdbx_poly_seq_scheme_auth"])
    df_mmCIF_pdbx_poly_seq_scheme = df_mmCIF_pdbx_poly_seq_scheme.drop(columns=["PDBnum_with_inc_code"])
    df_mmCIF_pdbx_poly_seq_scheme["pdbx_poly_seq_scheme_pdb"] = df_mmCIF_pdbx_poly_seq_scheme["PDBnum_with_inc_code_cor"]
    df_mmCIF_pdbx_poly_seq_scheme = df_mmCIF_pdbx_poly_seq_scheme.drop(columns=["PDBnum_with_inc_code_cor", "pdbx_poly_seq_scheme_pdb_ins_code"])

    df_pdbx_poly_seq_scheme_auth_final = df_mmCIF_pdbx_poly_seq_scheme.merge(df_final_dropped_dup, left_on="pdbx_poly_seq_scheme_pdb",
                                                                             right_on="auth_mmCIF", how='left')
    df_pdbx_poly_seq_scheme_auth_final.loc[:, 'new_col'] = df_pdbx_poly_seq_scheme_auth_final.pdbx_poly_seq_scheme_auth.map(
        lambda x: [(x[0], x[1], x[2]), x[0], (x[0], x[1], x[2])] if x[1] == "?" or x[0] == "?" or x[2] == "?" else "OK")
    df_pdbx_poly_seq_scheme_auth_final["New_Three_Rows_CIF_Num_Uni"] = np.where(df_pdbx_poly_seq_scheme_auth_final['new_col'] != "OK",
                                                                                df_pdbx_poly_seq_scheme_auth_final['new_col'],
                                                                                df_pdbx_poly_seq_scheme_auth_final['Three_Rows_CIF_Num_Uni'])
    df_pdbx_poly_seq_scheme_auth_final = df_pdbx_poly_seq_scheme_auth_final["New_Three_Rows_CIF_Num_Uni"]

    FINAL_RES_NUM_for_df_pdbx_poly_seq_scheme_auth_final = list()
    for n in df_pdbx_poly_seq_scheme_auth_final:
        try:
            if n[0][0] != ".":
                FINAL_RES_NUM_for_df_pdbx_poly_seq_scheme_auth_final.append(str(n[1]))
            else:
                FINAL_RES_NUM_for_df_pdbx_poly_seq_scheme_auth_final.append(str((int(n[1]) + default_mmCIF_num)))
        except TypeError:
            FINAL_RES_NUM_for_df_pdbx_poly_seq_scheme_auth_final.append("?")

    try:
        mmcif_dict["_pdbx_poly_seq_scheme.auth_seq_num"]
        mmcif_dict["_pdbx_poly_seq_scheme.auth_seq_num"] = FINAL_RES_NUM_for_df_pdbx_poly_seq_scheme_auth_final
    except KeyError:
        mmcif_dict["_pdbe_orig_poly_seq_scheme.auth_seq_num"] = FINAL_RES_NUM_for_df_pdbx_poly_seq_scheme_auth_final
