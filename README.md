# MuSE

## Installation

To install the package, you can run:

```bash
./install.bash
````

## Developing

### Docker

Build the docker image with:

```bash
docker build -t muse .
```

Run the docker image in development mode, which will start the jupyter notebook, and drop you into a shell. This can be done with:

```bash
docker run muse -p 8888:8888
```

Or you can use the develop command directly when running the docker image:

```bash
docker run muse -p 8888:8888 develop
```

You can run all the tests with:
    
```bash
docker run muse -p 8888:8888 test
```

If you want to run a shell and not the jupyter notebook, you can run:

```bash
docker run muse -p 8888:8888 debug
```

You can run the deployment mode to just run the jupyter notebook with:

```bash
docker run muse -p 8888:8888 deploy
```

Alternatively, you can use the `docker-compose` command to start the deployment mode with:

```bash
docker-compose up --build
```

Or, if you have the compose plugin:

```bash
docker compose up --build
```

This will also link the `outputs` folder to a local `outputs` folder, so you can access the outputs from the jupyter notebook.

### Notes

- It should be able to evalute what metrics can be used in different situations (find situations where metrics don't work)
- It should include Ollama ,torch, python, tensorflow (optional), python and R
- It should test different sizes of LLMs
- It should allow different structures for input data
- It should be compatible with Bengali, Hindi, Turkish, Arabic, Danish, Dutch, English, Finnish, French, German, Hungarian, Italian, Norwegian, Portuguese, Romanian, Russian, Spanish, and Swedish. It also supports word segmentation for Chinese, Thai, Japanese, and Burmese. This will be our baseline for deciding compatible languages.
- Include the languages: farsi, cantonese and mandarin.
- In terms of domains: separate between different domains (conversations, large documents, small documents), and evaluate which specific evaluation metric is bad for specific domains. 
