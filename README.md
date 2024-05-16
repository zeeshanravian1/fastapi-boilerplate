# FastAPI Boiler Plate Project with MySQL

## Name

FastAPI Boiler Plate Project

## Description

This project is built in [FastAPI](https://fastapi.tiangolo.com/) using [Python](https://www.python.org/) 3.12.3 with [Pyenv](https://realpython.com/intro-to-pyenv/) and [Poetry](https://python-poetry.org/) for dependency management. This project uses [MySQL](https://www.mysql.com/) database for storing data.
You can also use [Alembic](https://alembic.sqlalchemy.org/en/latest/) for database migrations for this project.

## Installing Dependencies

### [Pyenv](https://realpython.com/intro-to-pyenv/)

- This project uses Pyenv for python version management. You can follow this [tutorial](https://realpython.com/intro-to-pyenv/) to configure pyenv. Or you can follow below steps to configure pyenv.z

- Install pyenv build dependencies:

```bash
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev \
libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl
```

- Using pyenv-installer:

```bash
curl https://pyenv.run | bash
```

- Load pyenv automatically by adding
the following to ~/.bashrc:

```bash
echo -e '\n\nexport PYENV_ROOT="$HOME/.pyenv"\ncommand -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"\neval "$(pyenv init -)"' >> ~/.bashrc
```

- Restart your shell so the path changes take effect:

```bash
exec "$SHELL" # Or just restart your terminal
```

- Verify that pyenv is installed properly by using this command:

```bash
pyenv --version
```

### [MySQL](https://www.mysql.com/)

- This project uses MySQL database for storing data. You can install MySQL on your system by follow below steps.
- Install mysql dependencies:

```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
```

- Install MySQL on Ubuntu:

```bash
sudo apt install mysql-server
```

- Verify that MySQL is installed properly by using this command:

```bash
mysql --version
```

- Start MySQL server by this command:

```bash
sudo systemctl start mysql
```

- Run MySQL shell by this command:

```bash
sudo mysql
```

- Change root password by this command:

```bash
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Password@123';
```

- Create database by this command:

```bash
CREATE DATABASE IF NOT EXISTS <database_name>;
```

> **_NOTE:_** Change **< database_name >** with your database name.

- Login to MySQL shell after setting password:

```bash
mysql -u root -p
```

### [Python](https://www.python.org/)

To run project, you must have python 3.12.3 installed on your system.
If python 3.12.3 is not installed on your system, you can follow this [tutorial](https://realpython.com/intro-to-pyenv/) to install it on your system. Or you can follow below steps to install python 3.12.3 on your system.

- List all available python versions:

```bash
pyenv install --list
```

- List specific python versions:

```bash
pyenv install --list | grep " 3\.12"
```

- Install specific python version:

```bash
pyenv install -v 3.12.3
```

- List all installed python versions:

```bash
pyenv versions
```

- List specific installed python versions:

```bash
pyenv versions | grep " 3\.12"
```

- Change Global Python Version **(Optional)**:

```bash
pyenv global 3.12.3
```

- Change Local Python Version **(Optional)**:

```bash
pyenv local 3.12.3
```

- Verify that python is installed properly by using this command:

```bash
python --version
```

### [Poetry](https://python-poetry.org/)

- This project uses Poetry for dependency management. You can follow this [tutorial](https://python-poetry.org/docs/#installation) to install Poetry on your system. Or you can follow below steps to install Poetry on your system.

```bash
pip install poetry
```

- Enable tab completion:

```bash
poetry completions bash >> ~/.bash_completion
```

- Restart your shell so the path changes take effect:

```bash
source ~/.bashrc
```

- Verify that poetry is installed properly by using this command:

```bash
poetry --version
```

- Update poetry version **(Optional)**:

```bash
poetry self update
```

- Create Virtual Environment:
Go to project directory and type following command in terminal.

```bash
poetry init
```

> **_NOTE:_** This command will ask you some questions, you can skip them by pressing enter key.

- Activate Virtual Environment:
To activate virtual environment type following command in terminal.

```bash
poetry shell
```

- Install Dependencies:
To install dependencies type following command in terminal.

```bash
poetry install
```

- Install Specific Dependency:
To install specific dependency type following command in terminal.

```bash
poetry add <dependency_name>
```

> **_NOTE:_** Replace **< dependency_name >** with your dependency name.

- Verify your environment dependencies by running:

```bash
poetry show
```

- Remove Dependency:
To remove dependency type following command in terminal.

```bash
poetry remove <dependency_name>
```

- Listing the environments associated with the project:
To show all virtual environments type following command in terminal.

```bash
poetry env list
```

- Remove Virtual Environment:
To remove virtual environment type following command in terminal.

```bash
poetry env remove <virtual_environment_name>
```

> **_NOTE:_** Replace **< virtual_environment_name >** with your virtual environment name.

- Update Dependencies:
To update dependencies type following command in terminal.

```bash
poetry update
```

- Deactivate Virtual Environment:
To deactivate virtual environment type following command in terminal.

```bash
exit
```

### [Alembic](https://alembic.sqlalchemy.org/en/latest/)

- This project uses Alembic for database migrations. You can follow this [tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html) to install Alembic on your system. Or you can follow below steps to install Alembic on your system.

- Install Alembic:

```bash
poetry add alembic
```

- Initialize Alembic:

```bash
alembic init -t async migrations
```

> **_NOTE:_** We have already added migrations folder to project, you can skip above step.

- Edit env.py in migrations folder to set path for your database:

```python
# set path for your database
SQLALCHEMY_DATABASE_URL = "mysql://<user_name>:<user_password>@<host>:<port>/<database_name>"

# set metadata
target_metadata = Base.metadata

```

> **_NOTE:_** Replace **< user_name >** with your user name, **< user_password >** with your user password and **< database_name >** with your database name. Or, you can also set path for your database in .env file.
>
> **_NOTE:_** We already have added path for database and metadata in env.py file and make required changes, you can skip this step as well.

- Your migrations

```bash
alembic revision --autogenerate -m "<Migration Name>"
i.e alembic revision --autogenerate -m "Create User Table"
```

- Apply Migrations

```bash
alembic upgrade heads
```

## Usage

- Create .env file:
Create .env file in project root directory and add required environment variables in it.

```bash
touch .env
```

- Pre Defined Roles and Super Admin User:
We have already added some roles and also a super admin user in database at the time of migrations. So you can use these to login.

- Run FastAPI Server:
To run the FastAPI server run this command

```bash
uvicorn main:app --reload --host localhost --port 8000
```

- Access Swagger UI:
<http://0.0.0.0:8000/docs>

- Access Redoc UI:
<http://0.0.0.0:8000/redoc>


## Docker Commands

Run the following command to build the docker image:

```bash
docker build -t fastapi-boiler-plate .
```

OR

Use Docker Compose to build the docker image:

```bash
docker compose up --build
```
