# jfrog-user-tool
A command-line tool written in Python that utilizes the jFrog API
Use to ADD and DELETE users for a specific use case.

#Usage:

You must create a `config.py` file that contains 2 pieces of credentials:
```
apitoken = "eyJ2ZXI...JWCw7HQ"
login_name = "juan.sidberry"
```

You must get the API Token for your user from jFrog initially.

Also, should create a virtual environment (.venv) for running Python and installing libraries.
```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

