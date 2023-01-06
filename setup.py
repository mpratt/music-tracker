import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'musictracker',
    version = '0.1.0',
    author = "Michael Pratt",
    author_email = "author@michaelpratt.dev",
    description = ( "Keeps track of mp3s listened" ),
    license = "MIT",
    keywords = "",
    url = "",
    packages = find_packages(),
    package_dir = { '' : 'src' },
    long_description = read('README.md'),
    long_description_content_type="text/markdown",
    entry_points = {
        'console_scripts': [ 'music-tracker = musictracker.cli:run' ],
    },
)
