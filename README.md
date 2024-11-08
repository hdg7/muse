# MuSE

Multilingual Summarization Evaluation (MuSE) is a tool for evaluating summarization systems across multiple languages.
MuSE supports multiple domains, including single document, multi-document, and conversations.

## Usage

Muse can be used as a command line tool or as a python library, examples of this can be found in the [tutorial](./tutorial/README.md) folder.

Muse supports natively the following summarization systems:
- crossSum
- falconsAI
- mT5
- spacy
- sumy

And the following evaluation metrics:
- bertScore
- bleu
- meteor
- rouge
- ollama (our own metric utilising llms via ollama)

We also provide a notebook server through the docker interface.

## Example of CLI

The following command will evaluate the sumy summarization system on the document domain using the rouge metric and the english language:

```bash
muse -s sumy -t document -d ./examples/ -m rougemetric -l en
````

## Pre-requisites

In order to use MuSE, you will need ollama installed. You can find the instructions for installing ollama [here](https://ollama.com/install.sh).

You can then clone the repository with:

```bash
git clone git@github.com:hdg7/muse.git
```

and you can then install the requirements with:

```bash
pip install -r requirements.txt
```

You can also optionally install the development requirements with:

```bash
pip install -r optional-requirements.txt
```

## Installation

To install the package, once you have cloned the repository, you can run the install script with:

```bash
./install.bash
````

_TODO: Add instructions for installing the package from pypi._

## Docker

Build the docker image with:

```bash
docker build -t muse .
```

Run the docker image in development mode with:

```bash
docker run --gpus all muse -p 8888:8888
```

Alternatively, you can use the `docker compose` command to start the deployment mode with:

Or, if you have the compose plugin:

```bash
docker compose up --build
```

This will also link the `outputs` folder to a local `outputs` folder, so you can access the outputs from the jupyter notebook.

