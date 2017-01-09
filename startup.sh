#!/usr/bin/env bash
# this is a bash script to bootstart the project including downloading of datasets - setup of additional tools.

# DBpedia spotlight Installation

wget http://spotlight.sztaki.hu/downloads/dbpedia-spotlight-latest.jar
wget http://spotlight.sztaki.hu/downloads/latest_models/en.tar.gz
tar xzf en.tar.gz
rm en.tar.gz
mkdir dbpedia-spotlight
mv en dbpedia-spotlight
mv dbpedia-spotlight-latest.jar dbpedia-spotlight
cd dbpedia-spotlight
# java -Xmx6g -jar dbpedia-spotlight-latest.jar en http://localhost:2222/rest  # uncomment for running dbpedia spotlight server
cd ..

pip install pyspotlight










