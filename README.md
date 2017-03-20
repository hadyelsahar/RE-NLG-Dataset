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

## Feautres :
All of the modules in the pipeline take the a single json file [as descriped below]
 and outputs the same file after filling in some of it's attributes.
```
  {
        "doc"id:                       Document id     -- Wikipedia document id when dealing with wikipedia dump
        "title":                    title of the wikipedia document
        "uri":                      URI of the item containing the main page
        "text":                     The whole text of the document
        "sentences_boundaries":                start and end offsets of sentences
                                    [(start,end),(start,end)] start/ end are character indices
        "words_boundaries":                                      # list of tuples (start, end) of each word in Wikipedia Article, start/ end are character indices
        "entities":                                             # list of Entities   (Class Entity)
                                    [
                                    {
                                    "uri":
                                    "boundaries": (start,end)   # tuple containing the of the surface form of the entity
                                    "surface-form": ""
                                    "annotator" : ""            # the annotator name used to detect this entity [NER,DBpediaspotlight,coref]
                                    }
                                    ]
        "triples":                  list of triples that occur in the document
                                    We opt of having them exclusive of other fields so they can be self contained and easy to process
                                    [
                                    {
                                    "subject":          class Entity
                                    "predicate":        class Entity
                                    "object":           class Entity
                                    "dependency_path": "lexicalized dependency path between sub and obj if exists" or None (if not existing)
                                    "confidence":      # confidence of annotation if possible
                                    "annotator":       # annotator used to annotate this triple with the sentence
                                    "sentence_id":     # integer shows which sentence does this triple lie in
                                    }
                                    ]
    }
```

