# RE-NLG-Dataset
A Large Dataset for relation extraction and natural language generation from structured data. 


### Setup 

Run `startup.sh` 

to run DBpedia spotlight server on port 2222 run in a separate session
```
cd dbpedia-spotlight
# dbpedia spotlight server needs at least 6gb of ram
java -Xmx6g -jar dbpedia-spotlight-latest.jar en http://localhost:2222/rest 
```
# Dumps 

## Wikdata dumps

Wikdata provides a [tool for exporting RDF dumps](http://tools.wmflabs.org/wikidata-exports/rdf/index.html)
 
Simple RDF dumps were used in which each statement is represented in a triple and statements with qualifiers are omitted
[Wikidata RDF dumps 20160801](http://tools.wmflabs.org/wikidata-exports/rdf/exports/20160801/dump_download.html)

Sameas links between Wikidata and DBpedia are already extracted and can be found on [wikidata.dbpedia.org](http://wikidata.dbpedia.org/)

The latest available version in this project is [Available on the extraction page from 20150330](http://wikidata.dbpedia.org/downloads/20150330/)
the downloaded dump is available from here [20150330-sameas-all-wikis.ttl.bz2](http://wikidata.dbpedia.org/downloads/20150330/wikidatawiki-20150330-sameas-all-wikis.ttl.bz2)

## Text Dumps

### Wikipedia dumps

download the [latest wikipedia dump enwiki-latest-pages-articles.xml.bz2](https://dumps.wikimedia.org/enwiki/) and extract text documents from wikipedia articles.
 
see more `./datasets/Wikipedia/`



## Feautres  

| feature name                 | description                                                                      |
|------------------------------|----------------------------------------------------------------------------------|
