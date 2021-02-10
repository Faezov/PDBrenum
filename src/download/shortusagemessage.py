def short_usage_messenger():
    return '''
PDB.py
optional arguments:
-h, --help            show this help message and exit

-rftf text_file_with_PDB.txt, --renumber_from_text_file text_file_with_PDB.txt
This option will download and renumber specified files
usage $ python3 PDB.py -rftf text_file_with_PDB_in_it.txt -mmCIF
usage $ python3 PDB.py -rftf text_file_with_PDB_in_it.txt -PDB
usage $ python3 PDB.py -rftf text_file_with_PDB_in_it.txt -all

-rfla [6dbp 3v03 2jit ...], --renumber_from_list_of_arguments [6dbp 3v03 2jit ...]
This option will download and renumber specified files
usage $ python3 PDB.py -rfla 6dbp 3v03 2jit -mmCIF

-dftf text_file_with_PDB.txt, --download_from_text_file text_file_with_PDB.txt
This option will read given input file parse by space
or tab or comma or new line and download it example 
usage $ python3 PDB.py -dftf text_file_with_PDB_in_it.txt -mmCIF


-dfla [6dbp 3v03 2jit ...], --download_from_list_of_arguments 6dbp 3v03 2jit ...]
This option will read given list of arguments separated by space. 
Format of the list should be without any commas or quotation marks
usage $ python3 PDB.py -dfla 6dbp 3v03 2jit -mmCIF

-redb, --renumber_entire_database
This option will download and renumber entire PDB database in PDB or/and mmCIF format
usage $ python3 PDB.py -redb -mmCIF


-dall, --download_entire_database
This option will download entire mmCIF database
usage $ python3 PDB.py -dall -mmCIF


Roland Dunbrack's Lab
Fox Chase Cancer Center
Philadelphia, PA
2020
        '''
