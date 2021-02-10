from src.download.modules import *
from src.renum.mmCIF.try_MMCIF2Dict import try_MMCIF2Dict


def mmCIF_parser(mmCIF_name, default_input_path_to_mmCIF, df_PDBe_PDB_UniProt_without_null_index_PDBe, default_mmCIF_num, chains_to_change):
    mmcif_dict = try_MMCIF2Dict(default_input_path_to_mmCIF, mmCIF_name)
    if mmcif_dict == 0:
        return None
    try:
        _pdbx_poly_seq_scheme_auth_seq_num_before_change = mmcif_dict["_pdbx_poly_seq_scheme.auth_seq_num"]
    except KeyError:
        _pdbx_poly_seq_scheme_auth_seq_num_before_change = mmcif_dict["_pdbe_orig_poly_seq_scheme.auth_seq_num"]
        pass

    _atom_site_label_comp_id_list = mmcif_dict["_atom_site.label_comp_id"]
    _atom_site_label_seq_id_list = mmcif_dict["_atom_site.label_seq_id"]
    _atom_site_label_asym_id = mmcif_dict["_atom_site.label_asym_id"]
    _atom_site_pdbx_PDB_ins_code = mmcif_dict["_atom_site.pdbx_PDB_ins_code"]

    _atom_site_auth_comp_id = mmcif_dict["_atom_site.auth_comp_id"]
    _atom_site_auth_seq_id = mmcif_dict["_atom_site.auth_seq_id"]
    _atom_site_auth_asym_id = mmcif_dict["_atom_site.auth_asym_id"]
    _atom_site_pdbx_formal_charge = mmcif_dict["_atom_site.pdbx_formal_charge"]

    final_mmCIF_data_list_of_tuples_just_pdb = list(zip(_atom_site_label_seq_id_list, _atom_site_label_comp_id_list, _atom_site_label_asym_id))
    final_mmCIF_data_list_of_tuples_with_auth = list(zip(_atom_site_auth_seq_id, _atom_site_auth_comp_id, _atom_site_auth_asym_id))
    final_mmCIF_data_list_of_tuples_for_df = list(
        zip(final_mmCIF_data_list_of_tuples_just_pdb, final_mmCIF_data_list_of_tuples_with_auth, _atom_site_pdbx_PDB_ins_code))

    df_mmCIF = pd.DataFrame(final_mmCIF_data_list_of_tuples_for_df)
    df_mmCIF = df_mmCIF.rename(columns={0: "mmCIF", 1: "auth_mmCIF", 2: "ins_code"})

    df_mmCIF["mmCIF_copy"] = df_mmCIF["mmCIF"]
    df_mmCIF = df_mmCIF.set_index("mmCIF")

    df_mmCIF["PDBnum_inc_code"] = np.where(df_mmCIF['ins_code'] != "?",
                                           (df_mmCIF['auth_mmCIF'].apply(lambda x: x[0]) + df_mmCIF["ins_code"].apply(lambda y: y[0]) + ", "
                                            + df_mmCIF['auth_mmCIF'].apply(lambda x: x[1]) + ", " + df_mmCIF['auth_mmCIF'].apply(lambda x: x[2])),
                                           df_mmCIF["ins_code"])
    df_mmCIF["PDBnum_inc_code_cor"] = np.where(df_mmCIF["PDBnum_inc_code"] != "?", df_mmCIF["PDBnum_inc_code"].apply(lambda x: tuple(x.split(","))),
                                               df_mmCIF["auth_mmCIF"])
    df_mmCIF = df_mmCIF.drop(columns=["PDBnum_inc_code"])
    df_mmCIF["auth_mmCIF"] = df_mmCIF["PDBnum_inc_code_cor"]
    df_mmCIF = df_mmCIF.drop(columns=["PDBnum_inc_code_cor", "ins_code"])

    df_PDBe_PDB_UniProt_without_null_index_PDBe["PDBe_copy"] = df_PDBe_PDB_UniProt_without_null_index_PDBe.index
    df_final = df_mmCIF.merge(df_PDBe_PDB_UniProt_without_null_index_PDBe, left_on="mmCIF_copy", right_on="PDBe_copy", how='left')

    df_final['Uni_moD'] = df_final['Uni_moD'].replace(np.nan, "50000")
    df_final["Uni_moD"] = np.where(df_final['Uni_moD'] != "50000", df_final['Uni_moD'], df_final["auth_mmCIF"])
    df_final.loc[:, 'new_col_Uni'] = df_final.Uni_moD.map(lambda x: x[0])
    df_final["UniProt_50k"] = df_final.new_col_Uni.apply(lambda x: (int(x) + default_mmCIF_num if x.isdigit() else x))
    df_final.loc[df_final['UniProt'] != '50000', 'UniProt_50k'] = df_final['new_col_Uni']

    Three_Rows_CIF_Num_Uni = []
    for index, rows in df_final.iterrows():
        if rows.auth_mmCIF[2].strip() in chains_to_change:
            intermediate_list = [rows.mmCIF_copy, rows.UniProt_50k, rows.Uni_moD]
        else:
            intermediate_list = [rows.mmCIF_copy, rows.auth_mmCIF[0], rows.Uni_moD]
        Three_Rows_CIF_Num_Uni.append(intermediate_list)

    df_final["Three_Rows_CIF_Num_Uni"] = Three_Rows_CIF_Num_Uni
    df_final_dropped_dup = df_final.drop_duplicates(subset="auth_mmCIF", keep='first')

    return [df_final_dropped_dup, mmcif_dict, _pdbx_poly_seq_scheme_auth_seq_num_before_change, _atom_site_label_comp_id_list]
