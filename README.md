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
pip install -r requirements.txt
```

### Test
```bash
pytest
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

# Project Corrections

## Fix App CL

### Add code to main.py

```python
from app.calculator_repl import calculator_repl

def main():
    "Start the calculator cl app"
    calculator_repl()

if __name__ == "__main__":
    main()
```

## Correct Input Validation in REPL

### Implement input valiadtion in REPL

**Added import to calculator_repl.py**
```python
from app.input_validators import InputValidator
```

**Added validation after first input in calculator_repl.py**
```python
a = InputValidator.validate_number(a, calc.config)
```

**Added validation after second input in calculator_repl.py**
```python
b = InputValidator.validate_number(b, calc.config)
```

## Remove Duplicate Arithmetic

### Edit result in Calculation class

**Edited result in calculation.py**
```python
result: Decimal
```

### Delete automatic calculation in Calculation class

**Removed function**
```python
def __post_init__(self):
  """
  Post-initialization processing.

  Automatically calculates result of operation after 
  the Calculation instance is created.
  """
  self.result = self.calculate()
```

### Remove duplicate functionality in calculation.py

**Removed methods:**
```python
def calculate(self) -> Decimal:
  ...

@staticmethod
def _raise_div_zero():
  ...

@staticmethod
def _raise_neg_power():
  ...

@staticmethod
def _raise_invalid_root(x: Decimal, y: Decimal):
  ...

@staticmethod
def _raise_mod_zero():
  ...

@staticmethod
def _raise_intdiv_zero():
  ...

@staticmethod
def _raise_percent_zero():
  ...
```

**Removed from from_dict method:**
```python
calc.timestamp = datetime.datetime.fromisoformat(data['timestamp'])

saved_result = Decimal(data['result'])
if calc.result != saved_result:
    logging.warning(
        f"Loaded calculation result {saved_result} "
        f"differs from computed result {calc.result}"
    )  # pragma: no cover

return calc
```

**Return a Calculation instance directly with the saved result and timestamp in the from_dict method**
```python
return Calculation(
    operation=data['operation'],
    operand1=Decimal(data['operand1']),
    operand2=Decimal(data['operand2']),
    result=Decimal(data['result']),
    timestamp=datetime.datetime.fromisoformat(data['timestamp'])
)
```

### Update Calculaion instance creation in calculator.py

**Add to calculation in perform_operation method:**
```python
result=result
```

### Remove unused import from calculation.py
```python
import logging
```

### Remove duplicate tests from test_calculation.py

**Removed duplicate tests already covered in test_operations.py**
```python
test_addition()
test_subtraction()
...
...
test_absolute_difference()
test_unknown_operation()
```

### Fix remaining tests in test_calculation.py

**Added result parameters to tests:**
```python
def test_format_result():
  ...
  result=Decimal("1") / Decimal("3")
  ...

def test_equality():
  calc1= Calculation(..., result=Decimal("5"))
  calc2= Calculation(..., result=Decimal("5"))
  calc3= Calculation(..., result=Decimal("2"))
```

** Updated test_from_dict_preserves_saved_result method to:***
```python
def test_from_dict_preserves_saved_result():
  data = {
      "operation": "Addition",
      "operand1": "2",
      "operand2": "3",
      "result": "10",
      "timestamp": datetime.now().isoformat()
  }

  calc = Calculation.from_dict(data)

  assert calc.result == Decimal("10")
```

**Removed logging import**