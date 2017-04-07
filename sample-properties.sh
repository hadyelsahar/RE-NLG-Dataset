#!/usr/bin/env bash

cd datasets/wikidata
wget http://tools.wmflabs.org/wikidata-exports/rdf/exports/20160801/wikidata-properties.nt.gz

zcat wikidata-properties.nt | grep "<http://www.w3.org/2000/01/rdf-schema#label>" | grep "@en " | sed 's/.\{5\}$//' | sed 's/> </>\t</g' | sed 's/> "/>\t"/g' > wikidata-properties.csv
rm wikidata-properties.nt.gz
