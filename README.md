# Maintaining the repository

Consists of updating the `.rdf` file in `RePEc/usf/wpaper`. RePEc automatically retrieves information from this file every night. Useful resources:

https://econpapers.repec.org/archiveFAQ.htm#DirStructure

https://econpapers.repec.org/scripts/redifcheck.pl

http://openlib.org/acmes/root/docu/redif_1.html

# Production

When receiving a paper for inclusion in the repository, populate the template in `production` then copy and paste the data into the `RePEc\usf\usfpaper.rdf` file. 

Save the `.pdf` file as `submission.pdf` in the production folder. Edit the `1_create_frontpage.tex` file and then run it. Then, run `2_merge_frontpage.py` to create the production output. Make sure to activate the environment before doing so:

`conda activate .\.conda\`
`python .\production\2_merge_frontpage.py`

 Rename the output file according to the convention: "year-number.pdf", where "number" indicates how many papers are in the repository. For example, if this is the 3rd paper of 2023, the file name should be "2023-03.pdf".

Move the production output to the papers_backup folder. Also, save it on the economics department website. This is going to be the main source. Save it into `documents/wpaper`. The URL to the file must be 

`https://www.usf.edu/arts-sciences/departments/economics/documents/wpaper/year-number.pdf`