from src.download.modules import *
from src.renum.mmCIF.new_mmCIF import master_mmCIF_renumber_function


def ProcessPool_run_renum(format_to_download, input_mmCIF_files_were_found,
                          default_input_path_to_mmCIF,
                          default_input_path_to_SIFTS,
                          default_output_path_to_mmCIF,
                          default_mmCIF_num, gzip_mode,
                          exception_AccessionIDs, nproc):

    if not os.path.exists(default_output_path_to_mmCIF):
        os.makedirs(default_output_path_to_mmCIF)
    resulting = list()
    executor = ProcessPoolExecutor(max_workers=nproc)
    partial_master_mmCIF_renumber_function = partial(master_mmCIF_renumber_function,
                                                     default_input_path_to_mmCIF=default_input_path_to_mmCIF,
                                                     default_input_path_to_SIFTS=default_input_path_to_SIFTS,
                                                     default_output_path_to_mmCIF=default_output_path_to_mmCIF,
                                                     default_mmCIF_num=default_mmCIF_num, gzip_mode=gzip_mode,
                                                     exception_AccessionIDs=exception_AccessionIDs)

    jobs = [executor.submit(partial_master_mmCIF_renumber_function, mmCIF_files) for mmCIF_files in input_mmCIF_files_were_found]
    for job in tqdm.tqdm(as_completed(jobs), total=len(jobs), position=0, leave=True, desc="Renumbering " + format_to_download + " files"):
        result = job.result()
        resulting.append(result)

    return resulting
