#!/usr/bin/env bash
# following the tutorial in https://blog.afterthedeadline.com/2009/12/04/generating-a-plain-text-corpus-from-wikipedia/
git clone https://github.com/bwbaugh/wikipedia-extractor
wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2

mkdir extracted

# adding execution rights to wikiextractor
sudo chmod u+x ./wikipedia-extractor/WikiExtractor.py

echo "extraction of wiki format to xml"
bzcat enwiki-latest-pages-articles.xml.bz2 | ./wikipedia-extractor/WikiExtractor.py -cb 100M -o extracted -

echo "grouping all wikipedia documents into one file "
find extracted -name '*bz2' -exec bunzip2 -c {} \; > enwiki-latest-pages-articles-text.xml
echo "removing created folders"
rm -rf extracted

echo "Done Extraction all text in wikipedia articles can be found in enwiki-latest-pages-articles-text.xml"

echo "downloading mappings between wikipedia page id and wikidata id"
curl https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-page_props.sql.gz | zcat | grep -P "(\d+,'wikibase_item','Q\d+',NULL)" -o | cut -d"," -f1,3 | sed -e "s/'//g"  > wiki_id-wikidataid.csv

