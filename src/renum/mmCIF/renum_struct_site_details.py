from src.download.modules import *


def renum_struct_site_details(mmcif_dict, _atom_site_label_comp_id_list, df_final_dropped_dup, default_mmCIF_num):
    try:
        FINAL_RES_NUM_for_df_struct_site_details_final = list()
        _struct_site_details_auth = list()

        _struct_site_details = mmcif_dict["_struct_site.details"]
        if type(_struct_site_details) == str:
            _struct_site_details = [_struct_site_details]

        uniq_comp_id = np.unique(_atom_site_label_comp_id_list)
        uniq_comp_id_list = list(uniq_comp_id)

        for detail_line in _struct_site_details:
            n_split = detail_line.split()
            if len(n_split) > 2:
                if n_split[-3] in uniq_comp_id_list:
                    _struct_site_details_auth.append(tuple((n_split[-1], n_split[-3], n_split[-2])))

        try:
            _struct_site_details_auth_zip_list = list(zip(_struct_site_details_auth, _struct_site_details_auth))

            df_mmCIF_struct_site_details_auth = pd.DataFrame(_struct_site_details_auth_zip_list)
            df_mmCIF_struct_site_details_auth = df_mmCIF_struct_site_details_auth.rename(
                columns={0: "_struct_site_details_auth_1", 1: "_struct_site_details_auth_2"})

            df_struct_site_details_final = df_mmCIF_struct_site_details_auth.merge(
                df_final_dropped_dup, left_on="_struct_site_details_auth_1", right_on="auth_mmCIF", how='left')
            df_struct_site_details_final = df_struct_site_details_final["Three_Rows_CIF_Num_Uni"]

            for n in df_struct_site_details_final:
                if n[0][0] != ".":
                    FINAL_RES_NUM_for_df_struct_site_details_final.append(str(n[1]))
                else:
                    FINAL_RES_NUM_for_df_struct_site_details_final.append(str((int(n[1]) + default_mmCIF_num)))

        except KeyError:
            pass
        except TypeError:
            pass

        FINAL_RES_NUM_struct_site_details = list()
        count_for_struct_site_details = 0
        separator = ' '

        for detail_line in _struct_site_details:
            n_split = detail_line.split()
            if len(n_split) == 1:
                for z in n_split:
                    FINAL_RES_NUM_struct_site_details.append(z)
            else:
                try:
                    if n_split[-3] in uniq_comp_id_list:
                        FINAL_RES_NUM_struct_site_details.append(
                            separator.join(n_split[:-1] + [FINAL_RES_NUM_for_df_struct_site_details_final[count_for_struct_site_details]]))
                        count_for_struct_site_details = count_for_struct_site_details + 1
                    else:
                        FINAL_RES_NUM_struct_site_details.append(separator.join(n_split))
                except IndexError:
                    FINAL_RES_NUM_struct_site_details.append(n)

        mmcif_dict["_struct_site.details"] = FINAL_RES_NUM_struct_site_details

    except KeyError:
        pass
