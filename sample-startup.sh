#!/usr/bin/env bash
# this is a bash script to bootstart the project including downloading of datasets - setup of additional tools.

echo "installing python client for dbpedia spotlight..."
pip install pyspotlight

# Downloading Wikidata
cd datasets
echo "downloading wikidata dumps..."
mkdir wikidata ; cd wikidata

echo "make csv file out of nt"
curl http://tools.wmflabs.org/wikidata-exports/rdf/exports/20160801/wikidata-simple-statements.nt.gz | sed -E 's/[<>\"]//g'| sed -E 's/@.+//g' | cut -d" " -f1-3 | sed -E 's/\s/\t/g' > wikidata-triples.csv

echo "creating a csv dictionary out of english dbpedia uris to wikidata same as links"
bzcat wikidatawiki-20150330-sameas-all-wikis.ttl.bz2 | grep "http://dbpedia.org" | awk '{ print $3 " " $1}'  | sed -e 's/wikidata\.dbpedia\.org\/resource/www.wikidata\.org\/entity/'  | sed -e 's/ /\t/' | sed -E 's/[<>\"]//g' > dbpedia-wikidata-sameas-dict.csv











