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
cd datasets
echo "downloading wikidata dumps..."
mkdir wikidata ; cd wikidata

echo "download wikdata labels dump: wikidata-terms.nt.gz"
wget http://tools.wmflabs.org/wikidata-exports/rdf/exports/20160801/wikidata-terms.nt.gz
echo "download wikdata simple statements dump:  wikidata-simple-statements.nt.gz "
wget http://tools.wmflabs.org/wikidata-exports/rdf/exports/20160801/wikidata-simple-statements.nt.gz

echo "make csv file out of nt"
zcat  wikidata-simple-statements.nt.gz | sed -E 's/[<>\"]//g'| sed -E 's/@.+//g' | cut -d" " -f1-3 | sed -E 's/\s/\t/g' > wikidata-triples.csv

echo "download DBpedia-Wikidata Same As links dump: wikidatawiki-20150330-sameas-all-wikis.ttl.bz2"
wget http://wikidata.dbpedia.org/downloads/20150330/wikidatawiki-20150330-sameas-all-wikis.ttl.bz2
echo "download instance of dump wikidata-instances.nt.gz"
wget http://tools.wmflabs.org/wikidata-exports/rdf/exports/20160801/wikidata-instances.nt.gz
zcat wikidata-instances.nt.gz | cut -d" " -f1,3 | sed -e 's/ /\t/' | sed -E 's/[<>\"]//g'| sed -E 's/@.+//g' > wikidata-types.csv

echo "download class heirarchy dump: wikidata-taxonomy.nt.gz"
wget http://tools.wmflabs.org/wikidata-exports/rdf/exports/20160801/wikidata-taxonomy.nt.gz

echo "creating a csv dictionary out of wikidata english labels"
zcat wikidata-terms.nt.gz | grep "@en" | cut -d" " -f1,3- | sed -e 's/ /\t/' | sed -E 's/[<>\"]//g'| sed -E 's/@.+//g' | sort | uniq > wikidata-labels-dict.csv

echo "creating a csv dictionary out of english dbpedia uris to wikidata same as links"
bzcat wikidatawiki-20150330-sameas-all-wikis.ttl.bz2 | grep "http://dbpedia.org" | awk '{ print $3 " " $1}'  | sed -e 's/wikidata\.dbpedia\.org\/resource/www.wikidata\.org\/entity/'  | sed -e 's/ /\t/' | sed -E 's/[<>\"]//g' > dbpedia-wikidata-sameas-dict.csv

cd ../..

# Downloading DBpedia:
mkdir datasets/dbpedia
cd datasets/dbpedia
echo "download dbpedia triples"
wget http://downloads.dbpedia.org/2016-04/core-i18n/en/infobox_properties_en.ttl.bz2

echo "download dbpedia ontology triples"
wget http://downloads.dbpedia.org/2016-04/core-i18n/en/instance_types_en.ttl.bz2

echo "make list of dbpedia types"
bzcat instance_types_en.ttl.bz2 | cut -d" " -f3  | grep "<http://dbpedia.org/ontology/" | sed -E 's/[<>]//g'| sort | uniq > dbpedia-classes.txt



echo "Downloading CoreNLP Library"

mkdir ./utils/corenlp
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2015-12-09.zip -O ./utils/corenlp/stanford-corenlp-full-2015-12-09.zip
unzip ./utils/corenlp/stanford-corenlp-full-2015-12-09.zip -d ./utils/corenlp/

# Set up your classpath. For example, to add all jars in the current directory tree:
cd ./utils/corenlp/stanford-corenlp-full-2015-12-09
export CLASSPATH="`find . -name '*.jar'`"
# Run the server on port 9000
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer 9000
























