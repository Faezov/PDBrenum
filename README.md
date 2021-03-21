# **PDBrenum**

##### **Description:**

Here  we  provide PDBrenum (python=3.6 application) that fixes the PDB sequence numbering problem by replacing the  author numbering with numbering  derived  from  the  corresponding  UniProt  sequences. 
We obtain this correspondence from the SIFTS database from PDBe (https://www.ebi.ac.uk/pdbe/docs/sifts/). 
PDBrenum can take  a  list  of  PDB  entries  and provide  renumbered files  in the  mmCIF  format and  the  legacy PDB format for both asymmetric unit files and biological assembly files provided by PDB.
PDBrenum  was  heavily  tested  on  all  PDB  structure  files  in  both  formats  and  on  all  popular operating systems (Linux, Mac and Windows).

###### **Setting up PDBrenum:**
~~~~
Prerequisites anaconda should be installed: 
https://docs.anaconda.com/anaconda/install/

The following commands will set up a conda environment for running PDBrenum locally:
(base) $ git clone https://github.com/Faezov/PDBrenum.git
(base) $ cd PDBrenum
(base) $ conda create -n PDBrenum python=3.6 numpy=1.17 pandas=0.25.1 biopython=1.76 tqdm=4.36.1 ipython=7.8.0 requests=2.25.1 lxml=4.6.2 
(base) $ conda activate PDBrenum
~~~~
###### **Running PDBrenum:**
~~~~
Testing PDBrenum (please note that for Windows OS it's just python NOT python3):
(PDBrenum) $ python3 PDBrenum.py -h

Users can provide PDBids directly as a list of arguments (-rfla --renumber_from_list_of_arguments):
(PDBrenum) $ python3 PDBrenum.py -rfla 1d5t 1bxw 2vl3 5e6h -mmCIF
(PDBrenum) $ python3 PDBrenum.py -rfla 1d5t 1bxw 2vl3 5e6h -PDB
(PDBrenum) $ python3 PDBrenum.py -rfla 1d5t 1bxw 2vl3 5e6h -mmCIF_assembly
(PDBrenum) $ python3 PDBrenum.py -rfla 1d5t 1bxw 2vl3 5e6h -PDB_assembly

or put PDBids in text file (comma, space or tab delimited) (-rftf --renumber_from_text_file):
(PDBrenum) $ python3 PDBrenum.py -rftf input.txt -mmCIF
(PDBrenum) $ python3 PDBrenum.py -rftf input.txt -PDB
(PDBrenum) $ python3 PDBrenum.py -rftf input.txt -mmCIF_assembly
(PDBrenum) $ python3 PDBrenum.py -rftf input.txt -PDB_assembly

The user can renumber the entire PDB in a given format (by default in mmCIF if no format was provided):
(PDBrenum) $ python3 PDBrenum.py -redb -mmCIF 
(PDBrenum) $ python3 PDBrenum.py -redb -PDB
(PDBrenum) $ python3 PDBrenum.py -redb -mmCIF_assembly
(PDBrenum) $ python3 PDBrenum.py -redb -PDB_assembly


Note that sometimes on Windows biopython module might be installed incorrectly by conda and it will cause module error in python. 
To resolve this problem simply run: 
(PDBrenum) $ pip install biopython==1.76

PDBrenum uses multiprocessing (by default it will use all available CPUs) 
but the usercan set a limit to the numer of CPUs by providing number to -nproc flag:
"-nproc", "--set_number_of_processes"

Users can also change where input output files will go by using these self-explanatory flags (with absolute paths):
"-sipm", "--set_default_input_path_to_mmCIF"
"-sipma", "--set_default_input_path_to_mmCIF_assembly"
"-sipp", "--set_default_input_path_to_PDB"
"-sippa", "--set_default_input_path_to_PDB_assembly"
"-sips", "--set_default_input_path_to_SIFTS"
"-sopm", "--set_default_output_path_to_mmCIF"
"-sopma", "--set_default_output_path_to_mmCIF_assembly"
"-sopp", "--set_default_output_path_to_PDB"
"-soppa", "--set_default_output_path_to_PDB_assembly"

By default, files go here: 
default_input_path_to_mmCIF = current_directory + "/mmCIF"
default_input_path_to_mmCIF_assembly = current_directory + "/mmCIF_assembly"
default_input_path_to_PDB = current_directory + "/PDB"
default_input_path_to_PDB_assembly = current_directory + "/PDB_assembly"
default_input_path_to_SIFTS= current_directory + "/SIFTS"
default_output_path_to_mmCIF = current_directory + "/output_mmCIF"
default_output_path_to_mmCIF_assembly = current_directory + "/output_mmCIF_assembly"
default_output_path_to_PDB = current_directory + "/output_PDB"
default_output_path_to_PDB_assembly = current_directory + "/output_PDB_assembly"

Also, by default all files gzipped if you want to have them unzipped please use: 
"-offz" or "--set_to_off_mode_gzip"


Roland Dunbrack's Lab
Fox Chase Cancer Center
Philadelphia, PA
2020
~~~~



















