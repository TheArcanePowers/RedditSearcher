from setuptools import setup, find_packages
from io import open
from os import path

import pathlib
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# automatically captured required modules for install_requires in requirements.txt
with open(path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if ('git+' not in x) and (
    not x.startswith('#')) and (not x.startswith('-'))]
dependency_links = [x.strip().replace('git+', '') for x in all_reqs \
                    if 'git+' not in x]

setup (name = 'redditsearcher',
    description = 'A simple commandline app for generating csv files to see the most mentioned and highest scoring US tickers in reddit subreddits.',
    version = '1.0.0',
    packages = find_packages(), # list of all packages
    install_requires = install_requires,
    python_requires='>=3.7',
    author="Leonardo Coppi",
    keyword="stocks, tickers, csv, reddit, scraper",
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/thearcanepowers/redditseacher',
    author_email='leonardocoppi@outlook.com',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: Free To Use But Restricted",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
    include_package_data=True,
    zip_safe=False
)

print("DONT FORGET TO CREATE A PRAW.INI FILE!")