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
    name='sfb1158-metadata-gui',
    version='0.1.3',
    description='Web graphical user interface for SFB1158 metadata handling.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Luiz Tauffer, Vinicius Camozzato Vaz and Ben Dichter',
    author_email='ben.dichter@gmail.com',
    url='https://github.com/catalystneuro/sfb1158-metadata-gui',
    packages=find_packages(),
    package_data={'sfb1158_metadata_gui': [
        'examples/*.yml',
        'examples/*.json',
        '*.ini',
        'assets/*.png',
        'assets/*.css'
    ]},
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['sfb1158-metadata-gui=sfb1158_metadata_gui.cmd_line:cmd_line_shortcut'],
    }
)
