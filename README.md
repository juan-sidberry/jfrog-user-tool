# jfrog-user-tool
python tool that utilizes the jFrog API

User must create a `config.py` file that contains 2 pieces of credentials:
```
apitoken = "eyJ2ZXI...JWCw7HQ"
login_name = "juan.sidberry"
```

You must get the API Token for your user from jFrog initially.

Also, should create a virtual environment for running python.
```
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

TODO: put details on how to get that here.