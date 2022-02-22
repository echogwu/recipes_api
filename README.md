# Recipes
This is the backend for my recipe website to save my recipes for my family

# How to run it locally
## Prerequisite
- have python version >=3.7 installed

## Setup

    $ cd root_dir_of_this_repo
    $ python3 -m venv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ python app.py
  
This will bring up the local server at port 5000 by default.

## Gotchas

- Currently I use a local sqlite database file to store all the data, so make sure you remove the db file before you run `$python app.py` by running:
  
    $ rm data.db




# API Documentation
https://documenter.getpostman.com/view/2139264/UVkgzLDT
