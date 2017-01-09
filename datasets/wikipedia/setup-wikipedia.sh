#!/usr/bin/env bash

wget http://www.polishmywriting.com/download/wikipedia2text_rsm_mods.tgz
tar zxvf wikipedia2text_rsm_mods.tgz
cd wikipedia2text

wget https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
bunzip2 enwiki-latest-pages-articles.xml.bz2

mkdir out
./xmldump2files.py enwiki-latest-pages-articles.xml out

find out -type f | grep '\.txt$' >en.files
java -jar sleep.jar into8.sl en.files

