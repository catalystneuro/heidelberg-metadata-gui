# heidelberg-metadata-gui

This project has been funded by SFB 1158 (https://www.sfb1158.de/ , Project identifier (German Research Foundation (DFG) - project number 255156212)

Metadata standardization GUI. Makes it easy to edit metadata related to neurophysiological experiments.

[![PyPI version](https://badge.fury.io/py/heidelberg-metadata-gui.svg)](https://badge.fury.io/py/heidelberg-metadata-gui)
![Full Tests](https://github.com/catalystneuro/heidelberg-metadata-gui/actions/workflows/python-app.yml/badge.svg)


# Install
It is recommended that you install `heidelberg-metadata-gui` in a clean environment, for example with conda:
```
$ conda create -n env_heidelberg python=3.7 pip
```

In your clean environment, just pip install:
```
$ pip install heidelberg-metadata-gui
```

To install from the repository:
```
$ pip install git+https://github.com/catalystneuro/heidelberg-metadata-gui
```

# Usage

Navigate to the directory where your dataset is stored, then run from command line:
```
$ metadata-gui
```

On your browser, navigate to `localhost:5000`.

You can run metadata-gui with optional arguments, for example, to start it with a specific schema file and run the server on a specific port:
```
$ metadata-gui --schema_path /home/user/my_schema.json --port XXXX
```

# Running on docker

- Build docker with:  
```
docker build -t heidelberg:latest .
```

- run the docker with (this will reference a local folder to docker):  
```
docker run -it -p 5000:5000 -v /host/path/to/filesFolder:/usr/src/heidelberg_metadata_gui/files <image_id>
```

Your referenced local folder will be in the files folder of the docker
