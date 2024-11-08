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
docker run --gpus all muse -p 8888:8888
```

Or you can use the develop command directly when running the docker image:

```bash
docker run --gpus all  muse -p 8888:8888 develop
```

You can run all the tests with:
    
```bash
docker run --gpus all  muse -p 8888:8888 test
```

If you want to run a shell and not the jupyter notebook, you can run:

```bash
docker run --gpus all muse -p 8888:8888 debug
```

You can run the deployment mode to just run the jupyter notebook with:

```bash
docker run --gpus all muse -p 8888:8888 deploy
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

