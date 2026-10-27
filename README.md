# Project Setup

## Directory Setup

**In class folder (FA_is601_projects/)**
```bash
mkdir midterm_project/

cd midterm_project/
```

**Open in VSCode**
```bash
code .
```

### Create folders and files in the directory (project folder)

**In VSCode: right-click in explorer; New File or New Folder**

- `.github/workkflows/tests.yml`

- `.vscode/`
    - `launch.json`
    - `settings.json`

- `app/`
  - `__init__.py`
  - `calculation.py`
  - `calculator_config.py`
  - `calculator_memento.py`
  - `calculator_repl.py`
  - `calculator.py`
  - `exceptions.py`
  - `history.py`
  - `input_validators.py`
  - `operations.py`

- `tests/`
  - `__init__.py`
  - `test_calculation.py`
  - `test_calculator.py`
  - `test_config.py`
  - `test_exceptions.py`
  - `test_history.py`
  - `test_operations.py`
  - `test_validators.py`

- `.gitignore`

- `LICENSE`

- `main.py`

- `pytest.ini`

- `README.md`

- `requirements.txt`

## Project Initialization

### Set python version to 3.10
```bash
pyenv local 3.10
```

### Create and activate venv
```bash
python3 -m venv venv

source venv/bin/activate
```

### Initialize local repository
```bash
git init
```

### Add remote github repository
```bash
git remote add origin git@github.com:dbalicky/FA_IS601_midterm_project.git
```

### **Add code to necessary app files, test files, config files, etc.**

## Test Code

### Install dependencies
```bash
pip install -m requirements.txt
```

### Check and Test app
```bash
pytest
```

```bash
python3 main.py
```

## Update Github Repository

### Add files and commit
```bash
git add <folder_name/file_name>

git commit -m 'added/updated <file(s)>'
```

### Push to Github repo
```bash
git push -u origin main

### afterwards use: git push
```