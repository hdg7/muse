#!/bin/bash

function start_jupyter {
  jupyter notebook --allow-root --no-browser --port 8888 --ip=0.0.0.0
}

function start_ollama {
  OLLAMA_MODELS=${HOME}/models ollama serve &
  sleep 5
}

start_ollama

if [ "$1" == "deploy" ];
then
  echo "Deploying"
  start_jupyter
elif [ "$1" == "develop" ];
then
  echo "Developing"
  start_jupyter &
  echo "Jupyter started"
  bash
elif [ "$1" == "debug" ];
then
  echo "Debugging"
	bash
elif [ "$1" == "model" ];
then
  echo "Fetching model"
	i=1
	while [[ "$i" != "0" ]]
	do
	  echo "Pulling model: $2"
		ollama pull "$2"
		i=$?
		echo $i
	done
	echo "Model fetched"
else
	echo "Defaulting to develop"
	start_jupyter &
	echo "Jupyter started"
	bash
fi

