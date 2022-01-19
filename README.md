# Flashcards backend

## Presentation

This is the back-end of a personnal full-stack project I am working on.
It is written in **Python** using **Flask**.
Some of the features:
- user authentification using **JWT**
- connection to a **Postgres** database
- endpoints for the decks and the flashcards

The server is hosted on **Heroku** and is available [here](https://flashcardsbackend.herokuapp.com/).

## Installation

 If you wish to run the server locally on your computer, you must have PostgreSQL installed. Then follow these steps:
 - Clone this repository
 - Create and start a virtual environment

```bash
$ python3 -m venv venv$ 
source venv/bin/activate (linux)
.\venv\Source\activate (windows)
```
- Install dependencies

```bash
$ cd server
$ pip install -r requirements.txt
```

 - Add a .env file in the root of the project and add the following line with your correct informations:
 ```bash
DB_LINK="postgresql://USERNAME:PASSWORD@HOST:PORT/flashcards"
```
- Run the SQL script provided in this repo to create the database and all the tables.
- Inside the virtual environment, you can start the application using
```bash
$ flask run
```
## Front-end
The corresponding front-end for this server can be found [here](https://github.com/grr14/flashcards_front).
