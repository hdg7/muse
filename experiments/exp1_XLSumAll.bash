#!/bin/bash

# If the first argument is not provided, use the default path
if [ -z $1 ]
then
	xlsum_path="/home/ubuntu/dataMount/dataHector/XLSum_input/individual/"
else
	xlsum_path=$1
fi

for element in $(ls $xlsum_path)
do
    echo "bash /home/ubuntu/dataMount/dataHector/muse/experiments/exp1_XLSum.bash $element ./outputs rouge sumy $xlsum_path/$element"
    echo "bash /home/ubuntu/dataMount/dataHector/muse/experiments/exp1_XLSum.bash $element ./outputs rouge mT5 $xlsum_path/$element"
done
