# Demos of MuSE

## Multi-document Summarization

The data used for the following demo can be found in the `example_data/simplemulti` directory.
It is a simple multi-document source, and target pair in the form of the folder structure.

You can run it from the root of the repository with the following command:
```shell
muse -s sumy -t multi-document -d ./example_data/simplemulti -m rougemetric -l en 
```

