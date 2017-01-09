#!/usr/bin/env bash
# this is a bash script to bootstart the project including downloading of datasets - setup of additional tools.

# DBpedia spotlight Installation
echo "downloading dbpedia spotlight ..."
wget http://spotlight.sztaki.hu/downloads/dbpedia-spotlight-latest.jar
wget http://spotlight.sztaki.hu/downloads/latest_models/en.tar.gz

tar xzf en.tar.gz
rm en.tar.gz
mkdir dbpedia-spotlight
mv en dbpedia-spotlight
mv dbpedia-spotlight-latest.jar dbpedia-spotlight
cd dbpedia-spotlight
# screen -S dbpedia-spotlight -dm java -Xmx6g -jar dbpedia-spotlight-latest.jar en http://localhost:2222/rest  # uncomment for running dbpedia spotlight server
cd ..

echo "installing python client for dbpedia spotlight..."
pip install pyspotlight

# Downloading Wikidata
echo "downloading wikidata dumps..."
mkdir wikidata ; cd wikidata

echo "download wikdata labels dump: wikidata-terms.nt.gz"
wget http://tools.wmflabs.org/wikidata-exports/rdf/exports/20160801/wikidata-terms.nt.gz
echo "download wikdata simple statements dump:  wikidata-simple-statements.nt.gz "
wget http://tools.wmflabs.org/wikidata-exports/rdf/exports/20160801/wikidata-simple-statements.nt.gz
echo "download DBpedia-Wikidata Same As links dump: wikidatawiki-20150330-sameas-all-wikis.ttl.bz2"
wget http://wikidata.dbpedia.org/downloads/20150330/wikidatawiki-20150330-sameas-all-wikis.ttl.bz2
echo "download instance of dump wikidata-instances.nt.gz"
wget http://tools.wmflabs.org/wikidata-exports/rdf/exports/20160801/wikidata-instances.nt.gz
echo "download class heirarchy dump: wikidata-taxonomy.nt.gz"
wget http://tools.wmflabs.org/wikidata-exports/rdf/exports/20160801/wikidata-taxonomy.nt.gz

echo "creating a csv dictionary out of wikidata english labels"
zcat wikidata-terms.nt.gz | grep "@en" | cut -d" " -f1,3- | sed -e 's/ /\t/' | sed -E 's/[<>\"]//g'| sed -E 's/@.+//g' | sort | uniq > wikidata-terms-dict.csv














