#!/bin/bash
mkdir Wikipedia\ Abstracts; cd Wikipedia\ Abstracts; mkdir Data
wget http://downloads.dbpedia.org/2016-04/core-i18n/en/long_abstracts_en.tql.bz2
bzip2 -d long_abstracts_en.tql.bz2
