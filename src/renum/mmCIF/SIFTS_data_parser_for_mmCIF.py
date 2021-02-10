from src.download.modules import *


def SIFTS_data_parser_for_mmCIF(tuple_PDBe_for_PDB_and_tuple_PDB, tuple_PDBe_for_UniProt_and_tuple_UniProt,
                                default_mmCIF_num, chains_to_change="all"):
    df_PDBe_UniProt = pd.DataFrame(tuple_PDBe_for_UniProt_and_tuple_UniProt, columns=['PDBe', 'UniProt', "AccessionID"])
    df_PDBe_UniProt = df_PDBe_UniProt.drop_duplicates(subset="PDBe", keep='first')
    df_PDBe_PDB = pd.DataFrame(tuple_PDBe_for_PDB_and_tuple_PDB, columns=['PDBe', 'PDB'])
    df_PDBe_PDB = df_PDBe_PDB.drop_duplicates(subset="PDBe", keep='first')

    df_PDBe_PDB_UniProt = df_PDBe_PDB.merge(df_PDBe_UniProt, left_on="PDBe", right_on="PDBe", how='left')
    df_PDBe_PDB_UniProt['UniProt'] = df_PDBe_PDB_UniProt['UniProt'].replace(np.nan, "50000")
    df_PDBe_PDB_UniProt["Uni_moD"] = np.where(df_PDBe_PDB_UniProt['UniProt'] != "50000", df_PDBe_PDB_UniProt['UniProt'], df_PDBe_PDB_UniProt["PDBe"])
    df_PDBe_PDB_UniProt.loc[:, 'new_col_Uni'] = df_PDBe_PDB_UniProt.Uni_moD.map(lambda x: x[0])
    df_PDBe_PDB_UniProt["UniProt_50k"] = df_PDBe_PDB_UniProt.new_col_Uni.apply(lambda x: (int(x) + default_mmCIF_num if type(x) == str else x))
    df_PDBe_PDB_UniProt.loc[df_PDBe_PDB_UniProt['UniProt'] != '50000', 'UniProt_50k'] = df_PDBe_PDB_UniProt['new_col_Uni']

    Three_Rows_CIF_Num_Uni = []
    if chains_to_change == "all":
        for index, rows in df_PDBe_PDB_UniProt.iterrows():
            intermediate_list = [rows.PDBe, rows.UniProt_50k, rows.Uni_moD, rows.PDB, rows.AccessionID]
            Three_Rows_CIF_Num_Uni.append(intermediate_list)

    else:
        for index, rows in df_PDBe_PDB_UniProt.iterrows():
            if rows.PDB[2].strip() in chains_to_change:
                intermediate_list = [rows.PDBe, rows.UniProt_50k, rows.Uni_moD, rows.PDB, rows.AccessionID]
            else:
                intermediate_list = [rows.PDBe, rows.PDB[0], rows.Uni_moD, rows.PDB, rows.AccessionID]
            Three_Rows_CIF_Num_Uni.append(intermediate_list)

    df_PDBe_PDB_UniProt["Three_Rows_CIF_Num_Uni"] = Three_Rows_CIF_Num_Uni
    df_PDBe_PDB_UniProt_without_null = df_PDBe_PDB_UniProt[df_PDBe_PDB_UniProt.PDB.map(lambda x: x[0]) != "null"]
    df_PDBe_PDB_UniProt_without_null_index_PDBe = df_PDBe_PDB_UniProt_without_null.set_index("PDBe")

    return [df_PDBe_PDB_UniProt_without_null_index_PDBe, df_PDBe_PDB_UniProt]
