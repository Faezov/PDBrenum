from src.download.modules import *


def renumber_small_tables(auth_comp_id, auth_asym_id, auth_seq_id, PDB_ins_code, mmcif_dict, df_final_dropped_dup, default_mmCIF_num):
    try:
        auth_comp_id_list = mmcif_dict[auth_comp_id]
        auth_asym_id_list = mmcif_dict[auth_asym_id]
        auth_seq_id_list = mmcif_dict[auth_seq_id]
        PDB_ins_code = mmcif_dict[PDB_ins_code]

        if type(auth_asym_id_list) == str:
            auth_comp_id_list = [auth_comp_id_list]
            auth_asym_id_list = [auth_asym_id_list]
            auth_seq_id_list = [auth_seq_id_list]
            PDB_ins_code = [PDB_ins_code]

        auth_seq_id_list_zip = list(zip(auth_seq_id_list, auth_comp_id_list, auth_asym_id_list))

        df_mmCIF_auth_seq_id_list_zip = pd.DataFrame(zip(auth_seq_id_list_zip, PDB_ins_code))
        df_mmCIF_auth_seq_id_list_zip = df_mmCIF_auth_seq_id_list_zip.rename(columns={0: "auth_seq_id_list_zip", 1: "ins_code"})

        df_mmCIF_auth_seq_id_list_zip["PDB_with_ins_code"] = np.where(df_mmCIF_auth_seq_id_list_zip['ins_code'] != "?",
                                                                      (df_mmCIF_auth_seq_id_list_zip['auth_seq_id_list_zip'].apply(lambda x: x[0])
                                                                       + df_mmCIF_auth_seq_id_list_zip['ins_code'].apply(lambda y: y[0]) + ", "
                                                                       + df_mmCIF_auth_seq_id_list_zip['auth_seq_id_list_zip'].apply(
                                                                                  lambda x: x[1]) + ", "
                                                                       + df_mmCIF_auth_seq_id_list_zip['auth_seq_id_list_zip'].apply(lambda x: x[2])),
                                                                      df_mmCIF_auth_seq_id_list_zip['ins_code'])

        df_mmCIF_auth_seq_id_list_zip["PDB_with_ins_code_cor"] = np.where(df_mmCIF_auth_seq_id_list_zip['PDB_with_ins_code'] != "?",
                                                                          df_mmCIF_auth_seq_id_list_zip["PDB_with_ins_code"].apply(
                                                                              lambda x: tuple(x.split(","))),
                                                                          df_mmCIF_auth_seq_id_list_zip["auth_seq_id_list_zip"])

        df_mmCIF_auth_seq_id_list_zip = df_mmCIF_auth_seq_id_list_zip.drop(columns=["PDB_with_ins_code"])
        df_mmCIF_auth_seq_id_list_zip["auth_seq_id_list_zip"] = df_mmCIF_auth_seq_id_list_zip["PDB_with_ins_code_cor"]
        df_mmCIF_auth_seq_id_list_zip = df_mmCIF_auth_seq_id_list_zip.drop(columns=["PDB_with_ins_code_cor", "ins_code"])

        df_auth_seq_id_list_zip_final = df_mmCIF_auth_seq_id_list_zip.merge(df_final_dropped_dup, left_on="auth_seq_id_list_zip",
                                                                            right_on="auth_mmCIF", how='left')
        df_auth_seq_id_list_zip_final = df_auth_seq_id_list_zip_final["Three_Rows_CIF_Num_Uni"]
        FINAL_RES_NUM_for_df_auth_seq_id_list_zip_final = list()

        for n in df_auth_seq_id_list_zip_final:
            try:
                if n[0][0] != ".":
                    FINAL_RES_NUM_for_df_auth_seq_id_list_zip_final.append(str(n[1]))
                else:
                    try:
                        FINAL_RES_NUM_for_df_auth_seq_id_list_zip_final.append(str((int(n[1]) + default_mmCIF_num)))
                    except ValueError:
                        FINAL_RES_NUM_for_df_auth_seq_id_list_zip_final.append(
                            str(int(''.join(filter(lambda i: i.isdigit(), n[1]) + str(default_mmCIF_num)))))

            except TypeError:
                FINAL_RES_NUM_for_df_auth_seq_id_list_zip_final.append("?")

        mmcif_dict[auth_seq_id] = FINAL_RES_NUM_for_df_auth_seq_id_list_zip_final

    except KeyError:
        pass
