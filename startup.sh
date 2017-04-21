#!/usr/bin/env bash
# this is a bash script to bootstart the project including downloading of datasets - setup of additional tools.

#################################
# DBpedia spotlight Installation#
#################################
echo "downloading dbpedia spotlight ..."

mkdir resources
cd resources
wget http://spotlight.sztaki.hu/downloads/dbpedia-spotlight-latest.jar
wget http://spotlight.sztaki.hu/downloads/latest_models/en.tar.gz
tar xzf en.tar.gz ; rm en.tar.gz
mkdir dbpedia-spotlight
mv en dbpedia-spotlight
mv dbpedia-spotlight-latest.jar dbpedia-spotlight
cd dbpedia-spotlight
# screen -S dbpedia-spotlight -dm java -Xmx6g -jar dbpedia-spotlight-latest.jar en http://localhost:2222/rest  # uncomment for running dbpedia spotlight server
cd ..

echo "installing python client for dbpedia spotlight..."
pip install pyspotlight

######################
# SUtime Installation#
######################
echo "downloading SU time"
pip install sutime
mkdir sutime
cd sutime
wget wget https://www.dropbox.com/s/smayhjqgzlhxpwc/jars.zip?dl=0
unzip jars.zip?dl=0
rm jars.zip?dl=0
cd ../..

################################
# Downloading Wikidata Triples #
################################
echo "downloading wikidata dumps..."
cd datasets
mkdir wikidata
cd wikidata

# triples
echo "download wikidata facts triples statements from wikidata truthy dump .."
wget https://dumps.wikimedia.org/wikidatawiki/entities/20170418/wikidata-20170418-truthy-BETA.nt.bz2
echo "make csv file out of nt .."
## skipping labels and meta information and keep only wikidata props
bzcat  wikidata-20170418-truthy-BETA.nt.bz2 | grep "/prop/direct/P" | sed -E 's/[<>"]//g'| sed -E 's/@.+//g' | cut -d" " -f1-3 | sed -E 's/\s/\t/g' > wikidata-triples.csv

# DBpedia -Wikidata Sameas
echo "download DBpedia-Wikidata Same As links dump: wikidatawiki-20150330-sameas-all-wikis.ttl.bz2"
wget http://wikidata.dbpedia.org/downloads/20150330/wikidatawiki-20150330-sameas-all-wikis.ttl.bz2
echo "creating a csv dictionary out of english dbpedia uris to wikidata same as links"
bzcat wikidatawiki-20150330-sameas-all-wikis.ttl.bz2 | grep "http://dbpedia.org" | awk '{ print $3 " " $1}'  | sed -e 's/wikidata\.dbpedia\.org\/resource/www.wikidata\.org\/entity/'  | sed -e 's/ /\t/' | sed -E 's/[<>\"]//g' > dbpedia-wikidata-sameas-dict.csv

# Wikidata properties labels
echo "download wikidata properties labels"
wget http://tools.wmflabs.org/wikidata-exports/rdf/exports/20160801/wikidata-properties.nt.gz
zcat wikidata-properties.nt| grep "http://www.w3.org/2000/01/rdf-schema#label\|http://www.w3.org/2004/02/skos/core#altLabel" | grep "@en " | sed 's/^<//' | sed 's/.\{5\}$//' | sed 's/> </\t/g' | sed 's/> "/\t"/g'  > wikidata-properties.csv
rm wikidata-properties.nt.gz

cd ../..
























