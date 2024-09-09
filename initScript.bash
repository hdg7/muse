#!/bin/bash

LOG_FILE="/var/log/muse.log"

function start_jupyter {
  jupyter notebook --allow-root --no-browser --port 8888 --ip=0.0.0.0
}

function start_ollama {
  echo "Starting Ollama, any logs will be written to ${LOG_FILE}"
  OLLAMA_MODELS=${HOME}/models ollama serve > ${LOG_FILE} 2>&1 &
  while true; do
    if curl -s http://localhost:11434 > /dev/null; then
      break
    fi
    sleep 5
  done
}

cd "${MUSE_HOME}" || exit 1

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
elif [ "$1" == "test" ];
then
  echo "Testing"
  hatch run test
  if [ $? -ne 0 ]; then
    echo "Tests failed"
    exit 1
  fi
  echo "Tests passed"
  exit 0
else
	echo "Defaulting to develop"
	start_jupyter &
	echo "Jupyter started"
	bash
fi

