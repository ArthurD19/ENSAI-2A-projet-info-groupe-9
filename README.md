# ENSAI 2A Project Info: Poker Server
# TAPIS!

## Features of our poker server and the needs it fulfils

This project implements a **Texas Hold’em Poker server** with a simple client application.  
The server handles game logic, player management, tables, and database interactions, while the client allows users to join tables and play in real time.  

The server addresses the following needs:

- Enable multiple users to play poker simultaneously on the same database.
- Keep track of user accounts, balances, and game history.
- Provide a fast and responsive interface for betting, folding, and joining tables.
- Offer a basic but functional TUI (Text User Interface) for interacting with the game.

---

## :arrow_forward: Software and tools needed to use this server

- [Visual Studio Code](https://code.visualstudio.com/)
- [Python 3.13](https://www.python.org/)
- A [PostgreSQL](https://www.postgresql.org/) database

---

## :arrow_forward: Organisation of our server

### General information

| Item                       | Description                                                              |
| -------------------------- | ------------------------------------------------------------------------ |
| `README.md`                | Provides useful information to present, install, and use the application |
| `LICENSE`                  | Specifies the usage rights and licensing terms for the repository        |

### Configuration files

This repository contains configuration files to manage the project and development environment.

| Item                       | Description                                                              |
| -------------------------- | ------------------------------------------------------------------------ |
| `.github/workflows/ci.yml` | Automated workflow for testing, linting, or deploying                     |
| `.vscode/settings.json`    | Contains VS Code settings specific to this project                       |
| `.coveragerc`              | Test coverage configuration                                               |
| `.gitignore`               | Lists files and folders that should not be tracked by Git                |
| `logging_config.yml`       | Logging configuration                                                    |
| `requirements.txt`         | List of Python packages required to run the project                      |

> You will also need a `.env` file containing the database connection information.  

### Folders

| Item                       | Description                                                              |
| -------------------------- | ------------------------------------------------------------------------ |
| `data`                     | SQL scripts and data sets                                                |
| `doc`                      | UML diagrams, project documentation, project status                      |
| `logs`                     | Contains logs generated during execution                                  |
| `src`                      | Python code organized with a layered architecture                         |

---

### Settings files

Most configuration files should **not** need modification, except for:

- `.env` (database connection)
- `requirements.txt` (to install missing packages)

---

## :arrow_forward: Access our server

1. Download or clone the project repository
2. Open VSCode
3. Go to `File > Open Folder`
4. Select the root folder of the project (*ENSAI-2A-projet-info-groupe-9*)

---

## :arrow_forward: Install required packages

Run the following command to install all dependencies:

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

If you wish to use our database, please do not reset it. 
Otherwise, please follow the instructions below to initialise or reset your database.

- [ ] In Git Bash: 
```bash
psql -U nom_utilisateur -d nom_de_la_base
```
Ou 
- [ ] 
```bash
SET search_path TO public;
\i data/init_db.sql
```

## :arrow_forward: Execute our tests

If you want to execute all our tests.
```bash
pytest -v
```
If you just want to execute some tests.
```bash
python -m unittest <test_file>.py
```

## :arrow_forward: Launch the TUI application

This command launches a simple menu-based interface for interacting with the server:

- [ ] In Git Bash: `python -m src.main`

## :arrow_forward: Launch the server

Start the FastAPI server:
```bash
uvicorn src.api.api_main:app --host 0.0.0.0 --port 8000 --reload
```
Or

```bash
python src/api/api_main.py
```

Documentation :

- /docs
- /redoc

## :arrow_forward: Notes

All players must use the same SSP Cloud user to share the game state.
The server and clients can run on multiple terminals simultaneously.
For testing, you can launch multiple clients using python -m src.main.

