#!/usr/bin/env bash


echo "download DBpedia-Wikidata Same As links dump: wikidatawiki-20150330-sameas-all-wikis.ttl.bz2"
#wget http://wikidata.dbpedia.org/downloads/20150330/wikidatawiki-20150330-sameas-all-wikis.ttl.bz2

echo "creating a csv dictionary out of english dbpedia uris to wikidata same as links"

cat sample-dbpedia-abstracts.csv | cut -d$'\t' -f1 > dbpedia-links.txt

patterns="dbpedia-links.txt"
grep -f <(tr ',' '\n' < "${patterns}") "${search}"

bzcat wikidatawiki-20150330-sameas-all-wikis.ttl.bz2 | grep -f <(tr '\t' '\n' < "${patterns}") | awk '{ print $3 " " $1}' | sed -e 's/wikidata\.dbpedia\.org\/resource/www.wikidata\.org\/entity/'  | sed -e 's/ /\t/' | sed -E 's/[<>\"]//g' > sample-dbpedia-wikidata-sameas-dict.csv


#grep < awk '{ print $1 }' sample-dbpedia-abstracts.csv | awk '{ print $3 " " $1}'  | sed -e 's/wikidata\.dbpedia\.org\/resource/www.wikidata\.org\/entity/'  | sed -e 's/ /\t/' | sed -E 's/[<>\"]//g' > sample-dbpedia-wikidata-sameas-dict.csv
