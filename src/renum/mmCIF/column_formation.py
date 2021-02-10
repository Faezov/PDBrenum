def column_formation(mmcif_dict_keys):
    auth_comp_id_keylist = list()
    auth_asym_id_keylist = list()
    auth_seq_id_keylist = list()
    PDB_ins_code_keylist = list()

    for key in mmcif_dict_keys:
        if "auth_seq_id" in key:
            auth_seq_id_keylist.append(key)
        if "auth_asym_id" in key:
            auth_asym_id_keylist.append(key)
        if "auth_comp_id" in key:
            auth_comp_id_keylist.append(key)
        if "ins_code" in key:
            PDB_ins_code_keylist.append(key)

    initial_replacement_1 = {n.replace('auth_seq_id', 'HERE_SHOULD_BE_IT') for n in auth_seq_id_keylist}
    reverse_replacement_1 = {(n.replace('HERE_SHOULD_BE_IT', 'auth_seq_id'),
                              n.replace('HERE_SHOULD_BE_IT', 'auth_comp_id'),
                              n.replace('HERE_SHOULD_BE_IT', 'auth_asym_id'),
                              n.replace("HERE_SHOULD_BE_IT", "pdbx_PDB_ins_code")) for n in initial_replacement_1}
    reverse_replacement_2 = {(n.replace('HERE_SHOULD_BE_IT', 'auth_seq_id'),
                              n.replace('HERE_SHOULD_BE_IT', 'auth_comp_id'),
                              n.replace('HERE_SHOULD_BE_IT', 'auth_asym_id'),
                              n.replace("HERE_SHOULD_BE_IT", "PDB_ins_code")) for n in initial_replacement_1}
    reverse_replacement_3 = {(n.replace('HERE_SHOULD_BE_IT', 'auth_seq_id'),
                              n.replace('HERE_SHOULD_BE_IT', 'auth_comp_id'),
                              n.replace('HERE_SHOULD_BE_IT', 'auth_asym_id'),
                              n.replace("HERE_SHOULD_BE_IT", "pdbx_auth_ins_code")) for n in initial_replacement_1}

    initial_replacement_2 = {n.replace("pdbx_pdb_ins_code", 'HERE_SHOULD_BE_IT') for n in PDB_ins_code_keylist}
    reverse_replacement_4 = {(n.replace('HERE_SHOULD_BE_IT', 'pdbx_auth_seq_num'),
                              n.replace('HERE_SHOULD_BE_IT', 'mon_id'),
                              n.replace('HERE_SHOULD_BE_IT', 'pdbx_pdb_strand_id'),
                              n.replace("HERE_SHOULD_BE_IT", "pdbx_pdb_ins_code")) for n in initial_replacement_2}

    uniq_PDB_ins_code_keylist = list()
    for n in PDB_ins_code_keylist:
        nsplit = n.split(".")
        if nsplit[1][0:4] == "pdbx":
            nstrip = nsplit[1].strip("pdbx")
            lstrip = nstrip.lstrip("_")
        else:
            lstrip = nsplit[1]
        if lstrip not in uniq_PDB_ins_code_keylist:
            uniq_PDB_ins_code_keylist.append((nsplit[0] + "." + lstrip))

    initial_replacement_4 = {n.replace("PDB_ins_code", 'HERE_SHOULD_BE_IT') for n in uniq_PDB_ins_code_keylist}
    reverse_replacement_5 = {(n.replace('HERE_SHOULD_BE_IT', 'auth_seq_id'),
                              n.replace('HERE_SHOULD_BE_IT', 'auth_comp_id'),
                              n.replace('HERE_SHOULD_BE_IT', 'auth_asym_id'),
                              n.replace("HERE_SHOULD_BE_IT", "PDB_ins_code")) for n in initial_replacement_4}

    initial_replacement_5 = {n.replace("pdb_ins_code", 'HERE_SHOULD_BE_IT') for n in uniq_PDB_ins_code_keylist}
    reverse_replacement_6 = {(n.replace('HERE_SHOULD_BE_IT', 'auth_seq_id'),
                              n.replace('HERE_SHOULD_BE_IT', 'auth_comp_id'),
                              n.replace('HERE_SHOULD_BE_IT', 'auth_asym_id'),
                              n.replace("HERE_SHOULD_BE_IT", "pdb_ins_code")) for n in initial_replacement_5}

    reverse_replacement_7 = list()
    for n in reverse_replacement_5:
        nsplit_3 = n[3].split(".")
        pdbx_nsplit_3 = nsplit_3[0] + ".pdbx_" + nsplit_3[1]
        reverse_replacement_7.append((n[0], n[1], n[2], pdbx_nsplit_3))

    all_replacement_sets = list()
    all_replacement_sets.extend(reverse_replacement_1)
    all_replacement_sets.extend(reverse_replacement_2)
    all_replacement_sets.extend(reverse_replacement_3)
    all_replacement_sets.extend(reverse_replacement_4)
    all_replacement_sets.extend(reverse_replacement_5)
    all_replacement_sets.extend(reverse_replacement_6)
    all_replacement_sets.extend(reverse_replacement_7)

    final_set_of_replacements = list()
    for n in all_replacement_sets:
        if n not in final_set_of_replacements:
            if n[0] != n[1]:
                if "_pdbx_poly_seq_scheme" or "_pdbx_nonpoly_scheme" or "_pdbx_unobs_or_zero_occ_residues" not in n[0]:
                    final_set_of_replacements.append(n)

    return final_set_of_replacements
