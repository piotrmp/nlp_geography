# NLP Geography

This repository contains code and data for a study into the geography of NLP research, answering question such as: Where do the researchers carry out the work? Where do they present it? What is the environmental cost of travelling to NLP conferences? Do the events attract diverse participation? The results were described in the article *[Using NLP to quantify the environmental cost and diversity benefits of in-person NLP conferences](TODO)* presented at the ACL 2022 conference in Dublin.

## Data

In the [nlpgeo_data](nlpgeo_data) folder you will find the data used in our analysis. These files were prepared based on the [ACL Anthology datatabase](https://github.com/acl-org/acl-anthology/tree/master/data/xml) (a snapshot from 17.02.2021) through automatic extraction and refinement, followed by some manual corrections. Moreover, the contents were anonimised by replacing each author's name with a quasi-random hexadecimal number.

The following TSV files are included:
* ```papers-ref.tsv```: describes publications. Included fields: event ID, publication ID, first author name (anonimised), their e-mail domain, affiliation location and its geographic coordinates (latitude, longitude).
* ```volumes-ref.tsv```: describes places where publications are presented, e.g. a single conference session, a workshops or a journal volume. Included fields: event ID, name, year and location.
* ```venues-ref.tsv```: describes groups of events, e.g. a conference including all the sessions. Included fields: group ID, year, location and name.

Additionally, we provide:
* ```gdp.tsv```: country-wise GDP per capita in 2018 according to [Maddison Project Database](https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2020).

## Code

The code in [nlpgeo_code](nlpgeo_code) folder can be used replicate the procedure of the study. We worked through the following steps (note that you can skip steps 1-6 by using the data described above):

1. Download a snapshot of [ACL Anthology XML files](https://github.com/acl-org/acl-anthology/tree/master/data/xml),
2. Run ```extract.py``` to extract the necessary data in ```papers.tsv``` and ```volumes.tsv``` (you will need to point to the ACL XMLs in ```extract.py``` and provide a Google Maps API key in ```gMapsQuery.py```).
3. Run ```refine1.py``` to obtain the list of groups of events in ```venues.tsv```.
4. Perform manual corrections in ```venues.tsv```, writing the results in ```venues-ref.tsv```. We verified the locations of 2020 online events and filled in the missing values (marked by ```?```) by checking the conference websites.
5. Perform automatic data refinement by running ```refine2.py```. This fills in the missing locations of events by using the location of an event group and the missing affitliation location in publications with the most common location for this affiliation e-mail. The output is returned in ```volumes-ref.tsv``` and ```papers-ref.tsv```.
6. Perform manual corrections in ```volumes-ref.tsv```. Again, mostly the location of some of the online/in-person 2020 events was fixed.
7. Run ```analyse1.py``` to perform the data analysis and produce the values and plots included in the publication (part I).
8. Run ```analyse2.py``` for part II of the analysis.

Note that the scripts use the [Google Maps Geocoding API](https://developers.google.com/maps/documentation/geocoding/) through [a Python client](https://github.com/googlemaps/google-maps-services-python). This means you will need to [obtain an API key](https://developers.google.com/maps/get-started), e.g. during a free trial on [Google CLoud](https://cloud.google.com/). Moreover, the analysis scripts depend on a variety of libraries used for visualising the results.

## Licence

* The data are released under the [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) licence.
* The source code is released under the [GNU GPL 3.0](https://www.gnu.org/licenses/gpl-3.0.html) licence.

## Citation

TODO
