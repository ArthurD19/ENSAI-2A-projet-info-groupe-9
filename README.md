# ENSAI 2A Projet Info : Poker server
# TAPIS!

## Features of our poker server and the needs it fulfils

Ecrire ici une description des fonctionnalités de notre application et expliquer à quels besoins notre serveur répond


## :arrow_forward: Software and tools needed to use this server

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.13](https://www.python.org/)
- [Git](https://git-scm.com/)
- A [PostgreSQL](https://www.postgresql.org/) database


## :arrow_forward: Access our server

### Option 1: Clone the repository

- [ ] Open VSCode
- [ ] Open **Git Bash**
- [ ] Clone the repo
  - `git clone https://github.com/ludo2ne/ENSAI-2A-projet-info-template.git`

### Option 2: Use the archive folder

- [ ] Download the archive file containing the project

### Open Folder

- [ ] Open **Visual Studio Code**
- [ ] File > Open Folder
- [ ] Select folder *ENSAI-2A-projet-info-template*
  - *ENSAI-2A-projet-info-template* should be the root of your Explorer
  - :warning: if not the application will not launch. Retry open folder


## :arrow_forward: Organisation of our server

### General information

| Item                       | Description                                                              |
| -------------------------- | ------------------------------------------------------------------------ |
| `README.md`                | Provides useful information to present, install, and use the application |
| `LICENSE`                  | Specifies the usage rights and licensing terms for the repository        |

### Configuration files

This repository contains a large number of configuration files for setting the parameters of the various tools used.

| Item                       | Description                                                              |
| -------------------------- | ------------------------------------------------------------------------ |
| `.github/workflows/ci.yml` | Automated workflow that runs predefined tasks (like testing, linting, or deploying) |
| `.vscode/settings.json`    | Contains VS Code settings specific to this project                       |
| `.coveragerc`              | Setup for test coverage                                                  |
| `.gitignore`               | Lists the files and folders that should not be tracked by Git            |
| `logging_config.yml`       | Setup for logging                                                        |
| `requirements.txt`         | Lists the required Python packages for the project                       |

The file `requirements.txt` contains the list of packages required for the server to function properly. These packages must be installed. You will also need a `.env` file that you will have to create to use the server. The `.env` file contains the database connection information. (More information on these two files below) 


### Folders

| Item                       | Description                                                              |
| -------------------------- | ------------------------------------------------------------------------ |
| `data`                     | SQL script containing data sets                                          |
| `doc`                      | UML diagrams, project status...                                          |
| `logs`                     | Containing logs files (once you have launched the application)           |
| `src`                      | Folder containing Python files organized using a layered architecture    |



### Settings files

This repository contains a large number of configuration files for setting the parameters of the various tools used.

Normally, for the purposes of your project, you won't need to modify these files, except for `.env` and `requirements.txt`.


## :arrow_forward: Install required packages (focus on the file `requirements.txt`)

- [ ] In Git Bash, run the following commands to:
  - install all packages from file `requirements.txt`

```bash
pip install -r requirements.txt
```


## :arrow_forward: Environment variables (focus on the file `.env`)

At the root of the project :
- [ ] Create a file called `.env`
- [ ] Paste in and complete the elements below

```default
POSTGRES_PASSWORD=xxxxxxxxxxxx
POSTGRES_HOST=postgresql-93096.user-idxxxx
POSTGRES_PORT=5432
POSTGRES_DATABASE=defaultdb
POSTGRES_USER=user-idxxxx
POSTGRES_SCHEMA=public

PASSWORD_LENGTH="8"
```
If you want to use our database, please ask us for the exact login information. If you wish to connect to your own database, you will need to modify the first 6 lines with the login information for your database (your own Postgresql service).

## :arrow_forward: Initialising the database if necessary

If you wish to use our database, please do not reset it. Otherwise, please follow the instructions below to initialise or reset your database.

- [ ] In Git Bash: `psql -U nom_utilisateur -d nom_de_la_base -f /data/init_db.sql`
Ou 
- [ ] `SET search_path TO public;`
`\i data/init_db.sql`

## :arrow_forward: Launch the TUI application

This application provides a very basic graphical interface for navigating between different menus.

- [ ] In Git Bash: `python src/main.py`



## :arrow_forward: Launch the swagger

- [ ] `uvicorn src.api.api_main:app --reload`

Documentation :

- /docs
- /redoc