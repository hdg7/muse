#!/bin/bash

language=$1
output_dir=$2
metric=$3
model=$4
data_dir=$5

# If the first argument is not provided, use the default path
if [ -z $data_dir ]
then
	data_dir="/home/ubuntu/dataMount/dataHector/XLSum_input/individual/english"
fi


mkdir -p $data_dir/docs
cat $data_dir/train.source | head -n 1000 > $data_dir/docs/train.source 
cat $data_dir/train.target | head -n 1000 > $data_dir/docs/train.target
# Check if the output directory exists
mkdir -p $output_dir/$language/$model/$metric

muse -s $model -t document -d $data_dir/docs/ -e metrics -m $metric -l $language -o $output_dir/$language/$model/$metric/



