#!/usr/bin/env bash
echo "Downloading dbpedia abstracts"
wget http://downloads.dbpedia.org/2016-04/core-i18n/en/long_abstracts_en.ttl.bz2
echo "unzipping .."
bzip2 -dk long_abstracts_en.ttl.bz2  #unzip keep original
echo "changing ttl to csv.."
python prep_wiki_abstracts.py -i long_abstracts_en.ttl  -o dbpedia-abstracts.csv
rm long_abstracts_en.ttl
echo "Done!"




