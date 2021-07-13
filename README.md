# **PDBrenum**

Renumber Protein Data Bank files according to their UniProt sequences.

[![badge](https://img.shields.io/badge/Launch%20a%20PDBrenum%20demo%20in%20your%20browser-via%20MyBinder-579ACA.svg?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFkAAABZCAMAAABi1XidAAAB8lBMVEX///9XmsrmZYH1olJXmsr1olJXmsrmZYH1olJXmsr1olJXmsrmZYH1olL1olJXmsr1olJXmsrmZYH1olL1olJXmsrmZYH1olJXmsr1olL1olJXmsrmZYH1olL1olJXmsrmZYH1olL1olL0nFf1olJXmsrmZYH1olJXmsq8dZb1olJXmsrmZYH1olJXmspXmspXmsr1olL1olJXmsrmZYH1olJXmsr1olL1olJXmsrmZYH1olL1olLeaIVXmsrmZYH1olL1olL1olJXmsrmZYH1olLna31Xmsr1olJXmsr1olJXmsrmZYH1olLqoVr1olJXmsr1olJXmsrmZYH1olL1olKkfaPobXvviGabgadXmsqThKuofKHmZ4Dobnr1olJXmsr1olJXmspXmsr1olJXmsrfZ4TuhWn1olL1olJXmsqBi7X1olJXmspZmslbmMhbmsdemsVfl8ZgmsNim8Jpk8F0m7R4m7F5nLB6jbh7jbiDirOEibOGnKaMhq+PnaCVg6qWg6qegKaff6WhnpKofKGtnomxeZy3noG6dZi+n3vCcpPDcpPGn3bLb4/Mb47UbIrVa4rYoGjdaIbeaIXhoWHmZYHobXvpcHjqdHXreHLroVrsfG/uhGnuh2bwj2Hxk17yl1vzmljzm1j0nlX1olL3AJXWAAAAbXRSTlMAEBAQHx8gICAuLjAwMDw9PUBAQEpQUFBXV1hgYGBkcHBwcXl8gICAgoiIkJCQlJicnJ2goKCmqK+wsLC4usDAwMjP0NDQ1NbW3Nzg4ODi5+3v8PDw8/T09PX29vb39/f5+fr7+/z8/Pz9/v7+zczCxgAABC5JREFUeAHN1ul3k0UUBvCb1CTVpmpaitAGSLSpSuKCLWpbTKNJFGlcSMAFF63iUmRccNG6gLbuxkXU66JAUef/9LSpmXnyLr3T5AO/rzl5zj137p136BISy44fKJXuGN/d19PUfYeO67Znqtf2KH33Id1psXoFdW30sPZ1sMvs2D060AHqws4FHeJojLZqnw53cmfvg+XR8mC0OEjuxrXEkX5ydeVJLVIlV0e10PXk5k7dYeHu7Cj1j+49uKg7uLU61tGLw1lq27ugQYlclHC4bgv7VQ+TAyj5Zc/UjsPvs1sd5cWryWObtvWT2EPa4rtnWW3JkpjggEpbOsPr7F7EyNewtpBIslA7p43HCsnwooXTEc3UmPmCNn5lrqTJxy6nRmcavGZVt/3Da2pD5NHvsOHJCrdc1G2r3DITpU7yic7w/7Rxnjc0kt5GC4djiv2Sz3Fb2iEZg41/ddsFDoyuYrIkmFehz0HR2thPgQqMyQYb2OtB0WxsZ3BeG3+wpRb1vzl2UYBog8FfGhttFKjtAclnZYrRo9ryG9uG/FZQU4AEg8ZE9LjGMzTmqKXPLnlWVnIlQQTvxJf8ip7VgjZjyVPrjw1te5otM7RmP7xm+sK2Gv9I8Gi++BRbEkR9EBw8zRUcKxwp73xkaLiqQb+kGduJTNHG72zcW9LoJgqQxpP3/Tj//c3yB0tqzaml05/+orHLksVO+95kX7/7qgJvnjlrfr2Ggsyx0eoy9uPzN5SPd86aXggOsEKW2Prz7du3VID3/tzs/sSRs2w7ovVHKtjrX2pd7ZMlTxAYfBAL9jiDwfLkq55Tm7ifhMlTGPyCAs7RFRhn47JnlcB9RM5T97ASuZXIcVNuUDIndpDbdsfrqsOppeXl5Y+XVKdjFCTh+zGaVuj0d9zy05PPK3QzBamxdwtTCrzyg/2Rvf2EstUjordGwa/kx9mSJLr8mLLtCW8HHGJc2R5hS219IiF6PnTusOqcMl57gm0Z8kanKMAQg0qSyuZfn7zItsbGyO9QlnxY0eCuD1XL2ys/MsrQhltE7Ug0uFOzufJFE2PxBo/YAx8XPPdDwWN0MrDRYIZF0mSMKCNHgaIVFoBbNoLJ7tEQDKxGF0kcLQimojCZopv0OkNOyWCCg9XMVAi7ARJzQdM2QUh0gmBozjc3Skg6dSBRqDGYSUOu66Zg+I2fNZs/M3/f/Grl/XnyF1Gw3VKCez0PN5IUfFLqvgUN4C0qNqYs5YhPL+aVZYDE4IpUk57oSFnJm4FyCqqOE0jhY2SMyLFoo56zyo6becOS5UVDdj7Vih0zp+tcMhwRpBeLyqtIjlJKAIZSbI8SGSF3k0pA3mR5tHuwPFoa7N7reoq2bqCsAk1HqCu5uvI1n6JuRXI+S1Mco54YmYTwcn6Aeic+kssXi8XpXC4V3t7/ADuTNKaQJdScAAAAAElFTkSuQmCC)](https://mybinder.org/v2/gh/fomightez/PDBrenum/HEAD?filepath=demo.ipynb)

Take a demonstration tour of using the script by clicking the above badge to launch a Jupyter session in your browswer.

For those who only have a few structures/sequences to process, you can find a webserver to do the renumbering [here](http://dunbrack3.fccc.edu/PDBrenum/).


-------


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


## Attributions

Users of PDBrenum should cite:

- [PDBrenum: A webserver and program providing Protein Data Bank files renumbered according to their UniProt sequences. Faezov B, Dunbrack RL Jr.PLoS One. 2021 Jul 6;16(7):e0253411. doi: 10.1371/journal.pone.0253411. eCollection 2021. PMID: 34228733](https://pubmed.ncbi.nlm.nih.gov/34228733/)

***Clarifying Software Attribution: I, Wayne, am not involved in the PDBrenum software at all. Those in [the lab of Roland Dunbrack](http://dunbrack.fccc.edu/) are the developers and source of PDBrenum. See their materials, such as [the original repo](https://github.com/Faezov/PDBrenum) and [accompany article](https://pubmed.ncbi.nlm.nih.gov/34228733/). I simply set up this repository to make the software useable on the command line without installation headaches and in a full-featured, browser-based computational environment.***

I, Wayne, borrrowed the highligthed introductory text about notebooks at the top of the included notebook from Tim Sherratt's notebook here](https://github.com/GLAM-Workbench/te-papa-api/blob/master/Exploring-the-Te-Papa-collection-API.ipynb).


-------------

### Demonstration of PDBrenum

Click the launch badge below to launch a Jupyter notebook that steps through a demonstration of several of above commands.

No installations are needed as everything is already installed. The computing is privided by MyBinder.org.

After demonstrating it, substitute in PDB ids of interest to you and then run.  
If you make anything useful download it to your local computer, as these sessions are ephemeral.

[![badge](https://img.shields.io/badge/Launch%20a%20PDBrenum%20demo%20in%20your%20browser-via%20MyBinder-579ACA.svg?logo=data:image/png;base64,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)](https://mybinder.org/v2/gh/fomightez/PDBrenum/HEAD?filepath=demo.ipynb)


















