## Creating a Python virtual environment
`py -m venv venv`
## Activate environment
`./venv/Scripts/activate`

## installing packages
`pip3 install -r requirements.txt`

## Start
* `py ./src/main.py`

**or**

* `py ./src/main.py --reload`

## Config parameters
| Name                                          | Type            | Requred | Default            |Description                                                                                    |
| --------------------------------------------- | --------------- | :------: | :------: | ---------------------------------------------------------------------------------------------- |
| **APP_HOST**                                  | string      | ❌ |  "0.0.0.0" | Bind socket to this host
| **APP_PORT**                                  | int         | ❌ |    8000    | Bind socket to this port


## Treble shooting
#### Windows 10+
after install python need add permissions for running scripts from terminal

- run powershell as administrator
- `Set-ExecutionPolicy RemoteSigned`

# Restful docs
* [http://localhost:8000/docs](http://localhost:8000/docs)

# Testing
  `pytest -v`