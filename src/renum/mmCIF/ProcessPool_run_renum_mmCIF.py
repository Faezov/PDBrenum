from src.download.modules import *
from src.download.lookfilesinside import look_what_is_inside
from src.renum.mmCIF.new_mmCIF import master_mmCIF_renumber_function


def check_assemblies(mmCIF_assembly, default_output_path_to_mmCIF_assembly):
    output_mmCIF_assembly_files_were_found_list = list()
    output_mmCIF_assembly_files_were_found_list.append(mmCIF_assembly)
    for name in output_mmCIF_assembly_files_were_found_list:
        not_gzip = 1
        try:
            list_of_lines_from_assembly_file = gzip.open(
                Path(str(default_output_path_to_mmCIF_assembly) + "/" + name), 'rt').readlines()
        except OSError:
            # maybe not archived
            try:
                list_of_lines_from_assembly_file = open(
                    Path(str(default_output_path_to_mmCIF_assembly) + "/" + name), 'rt').readlines()
                not_gzip = 0
            except Exception:
                # broken archive
                os.remove(Path(str(default_output_path_to_mmCIF_assembly) + "/" + name))
                continue
        except Exception:
            # broken archive
            os.remove(Path(str(default_output_path_to_mmCIF_assembly) + "/" + name))
            continue

        # check if file startswith "_atom_site" table at the beginning
        try:
            if "_atom_site" in list_of_lines_from_assembly_file[3] and "loop_" in list_of_lines_from_assembly_file[2]:
                pass
            else:
                continue
        except IndexError:
            # empty file
            os.remove(Path(str(default_output_path_to_mmCIF_assembly) + "/" + name))
            continue

        try:
            new_order_for_assembly_file = (list_of_lines_from_assembly_file[:1]
                                           + list_of_lines_from_assembly_file[list_of_lines_from_assembly_file.index("#\n", 2):]
                                           + list_of_lines_from_assembly_file[2:list_of_lines_from_assembly_file.index("#\n", 2)]
                                           + ["#\n"])

            if not_gzip != 0:
                with gzip.open(Path(str(default_output_path_to_mmCIF_assembly) + "/" + name), "wt") as gzip_out:
                    for listitem in new_order_for_assembly_file:
                        gzip_out.write(listitem)
            else:
                with open(Path(str(default_output_path_to_mmCIF_assembly) + "/" + name), "wt") as file_out:
                    for listitem in new_order_for_assembly_file:
                        file_out.write(listitem)

        except ValueError:
            # file isn't complete
            os.remove(Path(str(default_output_path_to_mmCIF_assembly) + "/" + name))


def ProcessPool_run_renum_mmCIF(format_mmCIF, mmCIF_to_renumber, default_input_path_to_mmCIF,
                                default_input_path_to_SIFTS, default_output_path_to_mmCIF, default_mmCIF_num,
                                gzip_mode, exception_AccessionIDs, nproc):
    first_res = 0

    for i in range(3):
        if not os.path.exists(default_output_path_to_mmCIF):
            os.makedirs(default_output_path_to_mmCIF)

        # renumber loop
        resulting = list()
        executor = ProcessPoolExecutor(max_workers=nproc)
        partial_master_mmCIF_renumber_function = partial(master_mmCIF_renumber_function,
                                                         default_input_path_to_mmCIF=default_input_path_to_mmCIF,
                                                         default_input_path_to_SIFTS=default_input_path_to_SIFTS,
                                                         default_output_path_to_mmCIF=default_output_path_to_mmCIF,
                                                         default_mmCIF_num=default_mmCIF_num, gzip_mode=gzip_mode,
                                                         exception_AccessionIDs=exception_AccessionIDs)
        jobs = [executor.submit(partial_master_mmCIF_renumber_function, mmCIF_files) for mmCIF_files in mmCIF_to_renumber]
        for job in tqdm.tqdm(as_completed(jobs), total=len(jobs), miniters=1, position=0,
                             leave=True, desc="Renumbering " + format_mmCIF + " files"):
            result = job.result()
            resulting.append(result)

        if i == 0:
            first_res = resulting

        if format_mmCIF == "mmCIF_assembly":
            output_mmCIF = look_what_is_inside('output_mmCIF_assembly', default_output_path_to_mmCIF_assembly=default_output_path_to_mmCIF)
        else:
            output_mmCIF = look_what_is_inside('output_mmCIF', default_output_path_to_mmCIF=default_output_path_to_mmCIF)

        # checker loop
        check_list = list()
        executor = ProcessPoolExecutor(max_workers=nproc)
        partial_reform_assembly = partial(check_assemblies, default_output_path_to_mmCIF_assembly=default_output_path_to_mmCIF)
        jobs = [executor.submit(partial_reform_assembly, assembly_files) for assembly_files in output_mmCIF]
        for job in tqdm.tqdm(as_completed(jobs), total=len(jobs), miniters=1, position=0,
                             leave=True, desc="Checking " + format_mmCIF + " files"):
            resultus = job.result()
            check_list.append(resultus)

        if format_mmCIF == "mmCIF_assembly":
            output_mmCIF = look_what_is_inside('output_mmCIF_assembly', default_output_path_to_mmCIF_assembly=default_output_path_to_mmCIF)
        else:
            output_mmCIF = look_what_is_inside('output_mmCIF', default_output_path_to_mmCIF=default_output_path_to_mmCIF)

        if len(check_list) == len(output_mmCIF):
            break
        else:
            mmCIF_to_renumber = list(set(mmCIF_to_renumber) - set(output_mmCIF))

    return first_res
