![Build Status](https://github.com/EgorDikanskiy/Sparq/actions/workflows/python-package.yml/badge.svg)


Dependecies install
We use poetry as dependecies manager. First install poetry using
1. `pip install poetry`
Than acitvate venv:
2. `poetry shell`
Than install all dependecies:
3. `poetry install`
To add new dependecies use:
`poetry add <dep_name>`

---

Run dev serever:
Run in src/
`fastapi dev main.py`

### Running the app using docker-compose

1. install `Docker`

2. create `.env` file in the project root folder with the database credentials, for example:

```.env
POSTGRES_USER=user
POSTGRES_DB=dbname
POSTGRES_PASSWORD=password
```

3. execute command in the project root folder:

```bash
docker-compose up
```