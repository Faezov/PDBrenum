def log_writer(resulting):
    with open('log_corrected.txt', 'w') as f:
        comp_uni_human_uni_PDBid = list()
        pdb_id_set = set()
        formatted_item = (format("SP", "<3") + format("PDB_id", "<7") + format("chain_PDB", "<12") +
                          format("chain_auth", "<12") + format("comp_uni", "<20") + format("human_uni", "<20") +
                          format("prot_len", ">10") + format("uni_len", ">10") + format("chain_len", ">10") +
                          format("renum", ">10") + format("5k_or_50k", ">10"))
        f.write("%s\n" % formatted_item)

        for n in resulting:
            for z in n:
                if type(z) == int:
                    continue
                try:
                    if z[0][-1] == "*":
                        formatted_item = (format("*", "<3") + format(z[0][:4], "<7") + format(z[1], "<12") + format(z[2], "<12") +
                                          format(z[3], "<20") + format(z[4], "<20") + format(z[5], ">10") + format(z[6], ">10") +
                                          format(z[7], ">10") + format(z[8], ">10") + format(z[9], ">10"))
                        pdb_id_set.add(z[0][:4])
                        comp_uni_human_uni_PDBid.append((z[3], z[4], z[0][:4]))
                    else:
                        formatted_item = (format("+", "<3") + format(z[0], "<7") + format(z[1], "<12") + format(z[2], "<12") +
                                          format(z[3], "<20") + format(z[4], "<20") + format(z[5], ">10") + format(z[6], ">10") +
                                          format(z[7], ">10") + format(z[8], ">10") + format(z[9], ">10"))
                        pdb_id_set.add(z[0])
                        comp_uni_human_uni_PDBid.append((z[3], z[4], z[0][:4]))
                    f.write("%s\n" % formatted_item)

                    # print(formatted_item)
                except IndexError:
                    pass
                except TypeError:
                    pass

    comp_uni_human_uni_PDBid_translation = set()
    for n in comp_uni_human_uni_PDBid:
        if n[0] == "-":
            continue
        comp_uni_human_uni_PDBid_translation.add(n)

    with open('log_translator.txt', 'w') as file_handle:
        for list_item in comp_uni_human_uni_PDBid_translation:
            file_handle.write(list_item[0] + " " + list_item[1] + " " + list_item[2] + "\n")
