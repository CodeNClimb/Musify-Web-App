# MUSIFY
Sun Lee (else977) and Mathias Sackey (msac463) collaborated contribution to COMPSCI 235 Assignment 2.

## Installation
```shell
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```
**PyCharm**\
When using PyCharm, set the virtual environment using 'File'->'Settings' and select your project from the left menu.
Select 'Project Interpreter', click on the gearwheel button and select 'Add'.
Click the 'Existing environment' radio button to select the virtual environment. 

## Execution
From the project directory, and within the activated virtual environment (see *venv\Scripts\activate* above):
```shell
$ flask run
```

## Testing
**PyCharm**\
After you have configured pytest as the testing tool for PyCharm (File - Settings - Tools - Python Integrated Tools - Testing),
you can then run tests from within PyCharm by right clicking the tests folder and selecting "Run pytest in tests".

### Testing Memory Repository
From a terminal in the root folder of the project: 
```shell
$ python -m pytest test_mem
```

### Testing Database Repository
From a terminal in the root folder of the project: 
```shell
$ python -m pytest test_db
```
 
## Data sources
https://freemusicarchive.org/music/ \
This application uses new data that was taken from Free Music Archive to utilise larger data (archived) and working urls.
Note that the scrape was imperfect; there are likely ID double ups of albums, artists and or genres.
