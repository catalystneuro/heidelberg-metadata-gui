# SFB1158 Metadata GUI
Metadata standardization GUI. Makes it easy to edit metadata related to neurophysiological experiments.

[![PyPI version](https://badge.fury.io/py/sfb1158-metadata-gui.svg)](https://badge.fury.io/py/sfb1158-metadata-gui)
![Full Tests](https://github.com/catalystneuro/sfb1158-metadata-gui/actions/workflows/python-app.yml/badge.svg)
[![License](https://img.shields.io/pypi/l/pynwb.svg)](https://github.com/catalystneuro/sfb1158-metadata-gui/license.txt)


# Install
It is recommended that you install `sfb1158-metadata-gui` in a clean environment, for example with conda:
```
$ conda create -n env_sfb1158_metadata_gui python=3.7 pip
```

In your clean environment, just pip install:
```
$ pip install heidelberg-metadata-gui
```

To install from the repository:
```
$ pip install git+https://github.com/catalystneuro/sfb1158-metadata-gui
```

# Usage

Navigate to the directory where your dataset is stored, then run from command line:
```
$ metadata-gui
```

On your browser, navigate to `localhost:5000`.

You can run metadata-gui with optional arguments, for example, to start it with a specific schema file and run the server on a specific port:
```
$ sfb1158-metadata-gui --schema_path /home/user/my_schema.json --port XXXX
```
