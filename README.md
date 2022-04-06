# NLP Geography

This repository contains code and data for a study into the geography of NLP research, answering question such as: Where do the researchers carry out the work? Where do they present it? What is the environmental cost of travelling to NLP conferences? Do the events attract diverse participation? The results were described in the article *[Using NLP to quantify the environmental cost and diversity benefits of in-person NLP conferences](TODO)* presented at the ACL 2022 conference in Dublin.

## Data

In the [nlpgeo_data](nlpgeo_data) folder you will find the data used in our analysis. These files were prepared based on the [ACL Anthology datatabase](https://github.com/acl-org/acl-anthology/tree/master/data/xml) (a snapshot from 17.02.2021) through automatic extraction and refinement, followed by some manual corrections. Moreover, the contents were anonimised by replacing each author's name with a quasi-random hexadecimal number.

The following TSV files are included:
* ```papers-ref.tsv```: describes publications. Included fields: event ID, publication ID, first author name (anonimised), their e-mail domain and affiliation location.
* ```volumes-ref.tsv```: describes places where publications are presented, e.g. a single conference session, a workshops or a journal volume. Included fields: event ID, name, year and location.
* ```venues-ref.tsv```: describes groups of events, e.g. a conference including all the sessions. Included fields: group ID, year, location and name.

## Code

TODO

## Licence

* The data are released under the [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) licence.
* The source code is released under the [GNU GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.html) licence.

## Citation

TODO
