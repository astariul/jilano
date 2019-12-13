<h1 align="center">
  Jilano
</h1>

<p align="center">
  <img src="./assets/img/logo.png?raw=true" width=255" height="256" alt="Jilano's logo"/>
</p>

![](https://github.com/astariul/jilano/workflows/tests/badge.svg)

Jilano is a website where people can share a specific type of japanese poem : [Haiku](https://en.wikipedia.org/wiki/Haiku).

The website's features : 
* 🔍 **Explore section** : basic search functionality among haikus that are in database.
* ✏️ **Submit section** : write your own haiku and save it to the database !
* ⚖️ **Judge section** : pick one haiku out of 2 in order to ease the search of best haiku for others.

## Get started

### Installing

This code is running on **Python 3.5+**.

Clone the repo :
```
git clone https://github.com/astariul/jilano.git
cd jilano
```

---

Install requirements :
```
pip install -r requirements.txt
```

### Running tests

Run tests :
```
pytest
```

### Deployment

Start the application in debug mode :
```
python app.py
```

Or, start the application in production mode :
```
python -O app.py
```

and visit the local website at `http://127.0.0.1:8050/`.