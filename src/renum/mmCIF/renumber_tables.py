from src.download.modules import *


def renumber_tables(auth_seq_id, auth_asym_id, auth_comp_id, PDB_ins_code, mmcif_dict, df_final_dropped_dup, default_mmCIF_num, chains_to_change):
    len(auth_comp_id)
    try:
        PDB_ins_code_list = list()
        # auth_comp_id_list = mmcif_dict[auth_comp_id] for debug only
        auth_seq_id_list = mmcif_dict[auth_seq_id]
        auth_asym_id_list = mmcif_dict[auth_asym_id]

        if PDB_ins_code == 0:
            for _ in range(len(auth_seq_id_list)):
                PDB_ins_code_list.append("?")
        else:
            PDB_ins_code_list = mmcif_dict[PDB_ins_code]

        if type(auth_asym_id_list) == str:
            # auth_comp_id_list = [auth_comp_id_list] for debug only
            auth_seq_id_list = [auth_seq_id_list]
            auth_asym_id_list = [auth_asym_id_list]

            if PDB_ins_code == 0:
                PDB_ins_code_list = ["?"]
            else:
                PDB_ins_code_list = [PDB_ins_code]

        auth_seq_id_list_zip = list(zip(auth_seq_id_list, auth_asym_id_list))
        df_mmCIF_auth_seq_id_list_zip = pd.DataFrame(zip(auth_seq_id_list_zip, PDB_ins_code_list))
        df_mmCIF_auth_seq_id_list_zip = df_mmCIF_auth_seq_id_list_zip.rename(columns={0: "auth_seq_id_list_zip", 1: "ins_code"})

        df_mmCIF_auth_seq_id_list_zip["PDB_with_ins_code"] = np.where(df_mmCIF_auth_seq_id_list_zip['ins_code'] != "?",
                                                                      (df_mmCIF_auth_seq_id_list_zip['auth_seq_id_list_zip'].apply(lambda x: x[0])
                                                                       + df_mmCIF_auth_seq_id_list_zip['ins_code'].apply(lambda y: y[0]) + ", "
                                                                       + df_mmCIF_auth_seq_id_list_zip['auth_seq_id_list_zip'].apply(lambda x: x[1])),
                                                                      df_mmCIF_auth_seq_id_list_zip['ins_code'])

        df_mmCIF_auth_seq_id_list_zip["PDB_with_ins_code_cor"] = np.where(df_mmCIF_auth_seq_id_list_zip['PDB_with_ins_code'] != "?",
                                                                          df_mmCIF_auth_seq_id_list_zip["PDB_with_ins_code"].apply(
                                                                              lambda x: tuple(x.split(","))),
                                                                          df_mmCIF_auth_seq_id_list_zip["auth_seq_id_list_zip"])

        df_mmCIF_auth_seq_id_list_zip["auth_seq_id_list_zip"] = df_mmCIF_auth_seq_id_list_zip["PDB_with_ins_code_cor"]
        df_mmCIF_auth_seq_id_list_zip = df_mmCIF_auth_seq_id_list_zip.drop(columns=["PDB_with_ins_code_cor", "ins_code", "PDB_with_ins_code"])
        df_final_dropped_dup["auth_num_chain"] = df_final_dropped_dup["auth_mmCIF"].apply(lambda x: (x[0], x[2]))

        # drop_duplicates auth_num_chain column
        df_final_dropped_dup = df_final_dropped_dup.drop_duplicates(subset="auth_num_chain", keep='first')

        # merging
        df_auth_seq_id_list_zip_final = df_mmCIF_auth_seq_id_list_zip.merge(df_final_dropped_dup, left_on="auth_seq_id_list_zip",
                                                                            right_on="auth_num_chain", how='left')

        # masterpiece function
        df_auth_seq_id_list_zip_final["final"] = np.where(df_auth_seq_id_list_zip_final["Three_Rows_CIF_Num_Uni"].apply(lambda x: x is np.nan),
                                                          df_auth_seq_id_list_zip_final["auth_seq_id_list_zip"].apply(
                                                              lambda x: "?" if x[0] == "?"
                                                              else ("." if x[0] == "."
                                                                    else (str(int(''.join(filter(str.isdigit, str(x[0])))) + default_mmCIF_num)
                                                                          if x[1] in chains_to_change
                                                                          else (''.join(filter(str.isdigit, str(x[0]))))))),
                                                          df_auth_seq_id_list_zip_final["Three_Rows_CIF_Num_Uni"].apply(
                                                              lambda x: (str(int(''.join(filter(str.isdigit, x[1]))) + default_mmCIF_num + 10000)
                                                                         if (x[0][0] == "." and x[2][2].strip() in chains_to_change)
                                                                         else ''.join(filter(str.isdigit, str(x[1])))) if x is not np.nan else x))

        df_auth_seq_id_list_zip_final = df_auth_seq_id_list_zip_final["final"]
        final_list = list()
        for value in df_auth_seq_id_list_zip_final:
            final_list.append(value)

        # actual replacing auth_num with UniProt_num and of ins_code with '?'
        PDB_ins_code_list = list()
        if PDB_ins_code != 0:
            if "." in mmcif_dict[PDB_ins_code]:
                for _ in range(len(final_list)):
                    PDB_ins_code_list.append(".")
            else:
                for _ in range(len(final_list)):
                    PDB_ins_code_list.append("?")
            mmcif_dict[PDB_ins_code] = PDB_ins_code_list
        mmcif_dict[auth_seq_id] = final_list

    except KeyError:
        pass
