from src.download.modules import *
from src.download.lookfilesinside import look_what_is_inside


def check_assemblies(mmCIF_assembly, default_output_path_to_mmCIF_assembly):
    input_PDB_files_were_found_list = list()
    input_PDB_files_were_found_list.append(mmCIF_assembly)
    for name in input_PDB_files_were_found_list:

        not_gzip = 1

        try:
            file_gz = gzip.open(Path(str(default_output_path_to_mmCIF_assembly) + "/" + name), 'rt')
            list_of_lines_from_assembly_file = file_gz.readlines()
        except OSError:
            file_gz = open(Path(str(default_output_path_to_mmCIF_assembly) + "/" + name), 'rt')
            list_of_lines_from_assembly_file = file_gz.readlines()
            not_gzip = 0
        except EOFError:
            os.remove(Path(str(default_output_path_to_mmCIF_assembly) + "/" + name))
            # print("Warning!", "Compressed file ended before the end-of-stream marker was reached", name)
            continue
        try:
            if "_atom_site" in list_of_lines_from_assembly_file[3] and "loop_" in list_of_lines_from_assembly_file[2]:
                pass
            else:
                continue
        except IndexError:
            os.remove(Path(str(default_output_path_to_mmCIF_assembly) + "/" + name))
            # print("Warning!", "Empty or incomplete file", name)
            continue

        new_order_for_assembly_file = list()
        for n in list_of_lines_from_assembly_file:
            if "#\n" in n:
                if list_of_lines_from_assembly_file.index(n) == 1:
                    for x in list_of_lines_from_assembly_file[:1]:
                        new_order_for_assembly_file.append(x)
                    for y in list_of_lines_from_assembly_file[list_of_lines_from_assembly_file.index(n, 2):]:
                        new_order_for_assembly_file.append(y)
                    for z in list_of_lines_from_assembly_file[2:list_of_lines_from_assembly_file.index(n, 2)]:
                        new_order_for_assembly_file.append(z)
                    new_order_for_assembly_file.append("#\n")

                    if not_gzip != 0:
                        with gzip.open(name, "wt") as gzip_out:
                            for listitem in new_order_for_assembly_file:
                                gzip_out.write(listitem)
                    else:
                        with open(name, "wt") as file_out:
                            for listitem in new_order_for_assembly_file:
                                file_out.write(listitem)
                    break


def ProcessPool_run_reform_assembly(default_output_path_to_mmCIF_assembly, current_directory):
    output_mmCIF_assembly = look_what_is_inside('output_mmCIF_assembly', default_output_path_to_mmCIF_assembly=default_output_path_to_mmCIF_assembly)
    assembly_list = list()
    for assembly in output_mmCIF_assembly:
        if "assembly" in assembly:
            assembly_list.append(assembly)
    output_mmCIF_assembly = assembly_list

    os.chdir(default_output_path_to_mmCIF_assembly)
    resulting = list()
    executor = ProcessPoolExecutor()
    partial_reform_assembly = partial(check_assemblies, default_output_path_to_mmCIF_assembly=default_output_path_to_mmCIF_assembly)

    jobs = [executor.submit(partial_reform_assembly, assembly_files) for assembly_files in output_mmCIF_assembly]
    for job in tqdm.tqdm(as_completed(jobs), total=len(jobs), position=0, leave=True, desc="Checking assembly files"):
        resultus = job.result()
        resulting.append(resultus)

    os.chdir(current_directory)
    return resulting

