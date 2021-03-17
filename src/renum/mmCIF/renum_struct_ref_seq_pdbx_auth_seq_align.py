def renum_struct_ref_seq_pdbx_auth_seq_align(mmcif_dict):
    try:
        _struct_ref_seq_pdbx_strand_id = mmcif_dict["_struct_ref_seq.pdbx_strand_id"]

        _struct_ref_seq_pdbx_seq_align_beg_ins_code = mmcif_dict["_struct_ref_seq.pdbx_seq_align_beg_ins_code"]
        _struct_ref_seq_pdbx_auth_seq_align_beg = mmcif_dict["_struct_ref_seq.pdbx_auth_seq_align_beg"]
        _struct_ref_seq_db_align_beg = mmcif_dict["_struct_ref_seq.db_align_beg"]
        mmcif_dict["_struct_ref_seq.pdbx_auth_seq_align_beg"] = mmcif_dict["_struct_ref_seq.db_align_beg"]

        _struct_ref_seq_pdbx_seq_align_end_ins_code = mmcif_dict["_struct_ref_seq.pdbx_seq_align_end_ins_code"]
        _struct_ref_seq_pdbx_auth_seq_align_end = mmcif_dict["_struct_ref_seq.pdbx_auth_seq_align_end"]
        _struct_ref_seq_db_align_end = mmcif_dict["_struct_ref_seq.db_align_end"]
        mmcif_dict["_struct_ref_seq.pdbx_auth_seq_align_end"] = mmcif_dict["_struct_ref_seq.db_align_end"]

        if type(_struct_ref_seq_pdbx_seq_align_beg_ins_code) == str:
            if "." in _struct_ref_seq_pdbx_seq_align_beg_ins_code:
                mmcif_dict["_struct_ref_seq.pdbx_seq_align_beg_ins_code"] = "."
            else:
                mmcif_dict["_struct_ref_seq.pdbx_seq_align_beg_ins_code"] = "?"
        if type(_struct_ref_seq_pdbx_seq_align_end_ins_code) == str:
            if "." in _struct_ref_seq_pdbx_seq_align_end_ins_code:
                mmcif_dict["_struct_ref_seq.pdbx_seq_align_end_ins_code"] = "."
            else:
                mmcif_dict["_struct_ref_seq.pdbx_seq_align_end_ins_code"] = "?"

        PDB_ins_code_list = list()
        if type(_struct_ref_seq_pdbx_seq_align_beg_ins_code) != str:
            if "." in _struct_ref_seq_pdbx_seq_align_beg_ins_code:
                for _ in range(len(_struct_ref_seq_pdbx_seq_align_beg_ins_code)):
                    PDB_ins_code_list.append(".")
            else:
                for _ in range(len(_struct_ref_seq_pdbx_seq_align_beg_ins_code)):
                    PDB_ins_code_list.append("?")
            mmcif_dict["_struct_ref_seq.pdbx_seq_align_beg_ins_code"] = PDB_ins_code_list
            mmcif_dict["_struct_ref_seq.pdbx_seq_align_end_ins_code"] = PDB_ins_code_list

    except KeyError:
        pass
