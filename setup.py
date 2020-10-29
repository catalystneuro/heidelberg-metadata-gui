from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path


# Get the long description from the README file
here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

# Get requirements
with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name='heidelberg-metadata-gui',
    version='0.1.0',
    description='Web graphical user interface for Metadata fetching and editing',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Luiz Tauffer and Vinicius Camozzato Vaz',
    author_email='luiz@taufferconsulting.com',
    url='https://github.com/catalystneuro/heidelberg-metadata-gui',
    packages=find_packages(),
    package_data={'': ['']},
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['metadata-gui=heidelberg_metadata_gui.cmd_line:cmd_line_shortcut'],
    }
)
