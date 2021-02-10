
def if_no_SIFTS_data_log(mmCIF_name, mmcif_dict, log_message):
    strand_id_set = set()
    try:
        pull_chains_for_chains_count = mmcif_dict["_pdbx_poly_seq_scheme.pdb_strand_id"]
    except KeyError:
        try:
            pull_chains_for_chains_count = mmcif_dict["_pdbe_orig_poly_seq_scheme.pdb_strand_id"]
        except KeyError:
            pull_chains_for_chains_count = mmcif_dict["_atom_site.auth_asym_id"]

    for strand in pull_chains_for_chains_count:
        strand_id_set.add(strand)
    strand_id_set = list(strand_id_set)
    strand_id_set.sort()
    for strand in strand_id_set:
        count_elements_in_strand = 0
        for chain_id in pull_chains_for_chains_count:
            if chain_id == strand:
                count_elements_in_strand += 1
        log_message.append([mmCIF_name[:4], strand, "-", "-", len(pull_chains_for_chains_count), "-", count_elements_in_strand, "0", "0"])
    return log_message
