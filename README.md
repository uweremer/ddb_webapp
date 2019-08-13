# ddb_webapp
A Django project for collecting and disseminating data on participatory procedures

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg) ![Django Version](https://img.shields.io/badge/Django-2.2-blue.svg)

## Preambel
This ist the Django root project<sup>[1](#myfootnote1)</sup> for the web application “[ddb webapp](https://github.com/uweremer/ddb_webapp)”, the online website and tools, developed in the research project “database dialogue-oriented citizen participation” (“ddb - **D**atenbank **d**ialogorientierte **B**eteiligungsverfahren”). The project was conducted from April 2017 to March 2019 at the [Institute for Social Sciences]( https://www.sowi.uni-stuttgart.de/index.html) at the University of Stuttgart. It was funded by the state government of Baden-Württemberg. A short description of the project can be found [here](https://www.sowi.uni-stuttgart.de/abteilungen/ps/forschung/dbb/) (German only). The webapp is currently running at [www.beteiligungslandschaft-bw.de](www.beteiligungslandschaft-bw.de).

<sub><sup>
<a name="myfootnote1"><sup>1</sup></a>: Please see the Django documentation for the difference between  [Project]( https://docs.djangoproject.com/en/2.2/intro/tutorial01/#creating-a-project) and [App](https://docs.djangoproject.com/en/2.2/intro/tutorial01/#creating-the-polls-app).</sup></sub>

The webapp is designed to collect and provide structured information on citizen participation / participatory procedures at the local political level, by a semi-automated web-scraping approach.
The macro workflow involves three steps: 
1. collecting the information about participatory procedures (webscraping and human coding by student assistants), 
2. validation of the identified participatory procedures by officials from local authorities
3. providing public access to the data via web-interface and scientific use file.

In order to provide a clear separation of the workflow, to maintain data integrity and availability, and to comply with internal regulations on data privacy, separate instances of the webapp and its database should run on own machines / vm’s / containers.
Therefore, this base web application “[ddb_webapp]( https://github.com/uweremer/ddb_webapp)” can take on one of the three different roles by adding different apps in a modular fashion. These extend the functions of the application to the respective role.

- ddb_scraper: App provides access to the Google “[Custom Search JSON API]( https://developers.google.com/custom-search/)” and scrapes the identified relevant web documents into a corpus.
- ddb_codingtool: App for human coding of the corpus 
- ddb_validator: App to review identified participatory procedures for internal and external validation
- ddb_showcase: App to provide public access to the data (purged of personal data and approved for release) 


## Description
This Django project contains the initial code and settings to setup the Django environment for the basic [ddb_webapp]( https://github.com/uweremer/ddb_webapp). Its initial app `app` includes static pages for the landing page (index), project description, contact, and data privacy statement (conforming to the General Data Protection Regulation, GDPR / DSGVO). In addition, the app contains models, views and admin pages for the municipalities (basic information, contact, processing status etc.).  


## Prerequisites
MariaDB >= 10
Apache httpd server


## Usage
1. Pull the latest release of the project from github: 
2. Create an virtual python 3.6 environment and install dependencies from the `requirements.txt`
3. Set role of the webapp within `settings.py`
4. Set credentials and environmental variables for `settings.py` within `.credentials`

The `settings.py` reads the information from a `.credentials` file. The structure of the file is given in the `credentials_template.txt`. The a `.credentials` must never be under version control or shared otherwise!
5. migrate and populate database
6. Check privacy statement to match scope of the webapp and its conformity to the General Data Protection Regulation (GDPR).  

All done...




# Devel and productive models

The webapp provides operational modes for two environments: development and productive. To set the mode, the second line of the `.credentials` file is used as a switch. If it states `development`, then the `settings.py` defines the settings for developmental mode. If it contains any other statement, the webapp runs in productive mode. The differences between the two modes are mainly security and debugging related issues. The differing settings listed in the table below.

variable | development | productive
---------|-------------|-----------
DEBUG | True | False
Allowed_HOSTS | 127.0.0.1, localhost, testserver | Host IP
Send E-Mail	| redirect to file backend | send regular


# Known Issues


## mysqlclient
If the `mysqlclient` for python does not install correctly (on windows machines), follow this solution: https://stackoverflow.com/a/33544958



