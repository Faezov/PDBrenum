def column_formation(mmcif_dict):
    mmcif_dict_keys = mmcif_dict.keys()
    aut_seq_all_splitted = list()
    for key in mmcif_dict_keys:
        key_dot_splitted = key.split(".")
        for tab_name_col_name in key_dot_splitted:
            if "auth_seq" in tab_name_col_name:
                if "auth_seq_id" in key:
                    aut_seq_all_splitted.append(key_dot_splitted[:1]+key_dot_splitted[1].split("auth_seq_id"))
                if "auth_seq_num" in key:
                    aut_seq_all_splitted.append(key_dot_splitted[:1]+key_dot_splitted[1].split("auth_seq_num"))

    totaling_combinations = list()
    for table_name_prefix_suffix in aut_seq_all_splitted:
        combinations = list()
        for key in mmcif_dict_keys:
            if table_name_prefix_suffix[0] == key.split(".")[0]:
                # res_num auth_seq_id or auth_seq_num
                if table_name_prefix_suffix[1] in key and table_name_prefix_suffix[2] in key \
                        and "auth_seq_id" in key or "auth_seq_num" in key:
                    combinations.append(key)
                # chain auth_asym_id or strand_id
                if table_name_prefix_suffix[1] in key and table_name_prefix_suffix[2] in key \
                        and "auth_asym_id" in key or "strand_id" in key:
                    combinations.append(key)
                # ins_code
                if table_name_prefix_suffix[1] in key and table_name_prefix_suffix[2] in key \
                        and "ins_code" in key:
                    combinations.append(key)
                # monomer_type or auth_comp_id or auth_mon_id or mon_id for _struct_ref_seq_dif
                if table_name_prefix_suffix[1] in key and table_name_prefix_suffix[2] in key \
                        and "auth_comp_id" in key or "auth_mon_id" in key:
                    combinations.append(key)
                elif table_name_prefix_suffix[0] == "_struct_ref_seq_dif" \
                        and "mon_id" in key and "db_mon_id" not in key:
                    combinations.append(key)

        # work assuming all the elements in right order
        # and they are not crossing each other
        if len(combinations) > 4:
            combinations = combinations[:4]

        ordered_combination = list()
        for name in combinations:
            if "auth_seq" in name:
                ordered_combination.insert(0, name)
        for name in combinations:
            if "auth_asym_id" in name or "strand_id" in name:
                ordered_combination.insert(1, name)
        for name in combinations:
            if "ins_code" in name:
                ordered_combination.insert(2, name)
        for name in combinations:
            if "auth_comp_id" in name or "mon_id" in name:
                ordered_combination.insert(3, name)

        # exceptions
        if ("pdbx_unobs_or_zero_occ_residues" not in ordered_combination[0]
                and "nonpoly_scheme" not in ordered_combination[0]
                and "poly_seq_scheme" not in ordered_combination[0]
                and "ndb_struct_na_base" not in ordered_combination[0]):
            totaling_combinations.append(ordered_combination)

    return totaling_combinations

