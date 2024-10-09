#!/bin/bash

# If the first argument is not provided, use the default path
if [ -z $1 ]
then
	xlsum_path="/home/ubuntu/dataMount/dataHector/XLSum_input/individual/english"
else
	xlsum_path=$1
fi


mkdir -p $xlsum_path/docs
cat $xlsum_path/train.source | head -n 100 > $xlsum_path/docs/train.source 
cat $xlsum_path/train.target | head -n 100 > $xlsum_path/docs/train.target
muse -s sumy -t document -d $xlsum_path/docs/ -e metrics -m "rouge" -l "en" > $xlsum_path/docs/sumy_rouge.txt
muse -s mT5 -t document -d $xlsum_path/docs/ -e metrics -m "rouge" -l "en" > $xlsum_path/docs/mT5_rouge.txt

