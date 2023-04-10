# CPSC-449-Flask-RESTful-API-

## team members

Guang Chen kp82611@csu.fullerton.edu
Sami Bajwa samibajwa@csu.fullerton.edu

## Setup

1. create a virtual environment  
   `python -m venv venv`

2. enter virtual environment  
   windows: `venv\Scripts\activate.bat`  
   linux: `venv/bin/activate`

3. install requirements  
   `pip install -r requirements.txt`

4. run the setup.sql in my sql server to create table for this API

5. change database config in app.py file

```
conn = pymysql.connect(
    host='hostname',
    user='username',
    password="password",
    db='449_db',
)
```

6. run the main file  
   windows: `python app.py`  
   linux: `python3 app.py`
