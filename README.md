# Project introduction

This project is a calculator application that implements REPL to allow users to choose an operation (addition, subtraction, multiplication, division, power, root, modulus, percent, integer division, absolute difference) and input 2 numbers to perform the chosen calculation.

The application allows REPL commands such as history and clear: to view or clear the calculation history; undo and redo: to reverse or restore calculations; save and load: to manage saved CSV history; help: which shows all commands; exit: which exits the application; and cancel: which cancels operand entry.

# Running Application

After installing required dependencies and activating virtual environment, start the calculator from the project's root directory with:
```python
python main.py
```
The calculator launches the REPL, which allows the users to enter arithmetic commands, and provide two numerical operands. Users can enter the help command to display all the available commands, history to view previous calculations, or exit to terminate the application. When prompted to enter operands, users can type *cancel* to abort the current calculation

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

- `.github/workflows/tests.yml`

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

**Commands to clone and access project directory:**
```bash
git clone https://github.com/dbalicky/FA_IS601_midterm_project.git

cd FA_IS601_midterm_project
```

*Note, cloning the repository requires the creation of a local .env file*

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

```bash
python -m pytest --cov=app --cov-report=term-missing
```

*Note, latest local test run reported 112 tests passing with 90% coverage*

### CI/CD with Github Actions

Workflow configuration for this project is located in:

*.github/workflows/tests.yml*

The workflow is reponsible for setting up the Python environment using a specific version, installing the required dependencies from *requirements.txt*, and running automated tests using pytest.

Test results and execution status of the workflow are located in the **Actions** tab of the Github repository.

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
    """Start the calculator command-line app."""
    calculator_repl()

if __name__ == "__main__":
    main()
```

## Correct Input Validation in REPL

### Implement input validation in REPL

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

## Configure and Implement .env

### Create .env

**Added configurations to .env:**
```python
CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

### Fix calculator precicion in calculator_repl.py

**Changed following code:**
```python
if isinstance(result, Decimal):
    result = result.normalize()

print(f"\nResult: {result}")
```

**to:**
```python
if isinstance(result, Decimal):
    display_result = f"{result:.{calc.config.precision}f}"
    display_result = display_result.rstrip('0').rstrip('.') if '.' in display_result else display_result
else:
    display_result = str(result)

print(f"\nResult: {display_result}")
```

### Fix auto save in calculator_repl.py only if auto-save is enabled

**Added to auto save code:**
```python
...
  if calc.config.auto_save:
    ...
```
**Added code to EOFError handler**
```python
...
if calc.config.auto_save:
try:
  calc.save_history()
  print("History saved successfully.")
except Exception as e:
  print(f"Warning, could not save successfully: {e}")
...
```

### Add default encoding to write and read methods in calculator.py

**Added following parameter to all .to_csv and .read_csv commands in load_history and save_history methods**
```python
encoding=self.config.default_encoding
```

### Fix calculator tests for automatic saving

**Made changes to following:**
```python
@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit(mock_print, mock_input):
    with patch('app.calculator.Calculator.save_history') as mock_save_history:
        calculator_repl()
        mock_save_history.assert_called_once()
        mock_print.assert_any_call("History saved successfully.")
        mock_print.assert_any_call("Goodbye!")

...

@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit_save_history_error(mock_print, mock_input):
    with patch(
        'app.calculator.Calculator.save_history',
        side_effect=Exception("save failed")
    ):
        calculator_repl()

    mock_print.assert_any_call("Warning: Could not save history: save failed")
    mock_print.assert_any_call("Goodbye!")
```
**to:**
```python
@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit(mock_print, mock_input):
    with patch('app.calculator_repl.Calculator') as mock_calculator:
        mock_calc = mock_calculator.return_value

        mock_calc.config.auto_save = True

        calculator_repl()

        mock_calc.save_history.assert_called_once()
        mock_print.assert_any_call("History saved successfully.")
        mock_print.assert_any_call("Goodbye!")

...

@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit_save_history_error(mock_print, mock_input):
    with patch('app.calculator_repl.Calculator') as mock_calculator:
        mock_calc = mock_calculator.return_value

        # Enable auto save
        mock_calc.config.auto_save = True

        # Simulate an error when saving history
        mock_calc.save_history.side_effect = Exception("save failed")

        calculator_repl()

        mock_calc.save_history.assert_called_once()
        mock_print.assert_any_call("Warning: Could not save history: save failed")
        mock_print.assert_any_call("Goodbye!")
```

**Added following test for when auto_save=False**
```python
@patch('builtins.input', side_effect=['exit'])
@patch('builtins.print')
def test_calculator_repl_exit_auto_save_disabled(mock_print, mock_input):
    with patch('app.calculator_repl.Calculator') as mock_calculator:
        mock_calc = mock_calculator.return_value

        mock_calc.config.auto_save = False

        calculator_repl()

        mock_calc.save_history.assert_not_called()

        mock_print.assert_any_call("Goodbye!")
```

### Adjust configuration settings in calculator_config.py

**Updated configuration setting for maximum history size in __init__()**
```python
self.max_history_size = (
    max_history_size
    if max_history_size is not None
    else int(os.getenv('CALCULATOR_MAX_HISTORY_SIZE', '1000'))
)
```

**Updated configuration setting for precision**
```python
self.precision = (
    precision
    if precision is not None
    else int(os.getenv('CALCULATOR_PRECISION', '10'))
)
```

**Updated configuration setting for maximum input value**
```python
self.max_input_value = (
    Decimal(str(max_input_value))
    if max_input_value is not None
    else Decimal(os.getenv('CALCULATOR_MAX_INPUT_VALUE', '1e999'))
)
```

**Updated configuration setting for default encoding**
```python
self.default_encoding = (
    default_encoding
    if default_encoding is not None
    else os.getenv('CALCULATOR_DEFAULT_ENCODING', 'utf-8')
)
```

**Changed precision check for ConfigurationError**
```python
if self.precision < 0:
    raise ConfigurationError("precision must not be negative")
```

### Validate configuration values in calculator_config.py

**Added encoding validation with codecs**
```python
import codecs
...
...
try:
  codecs.lookup(self.default_encoding)
except (LookupError, TypeError):
  raise ConfigurationError(
    f"Invalid encoding: {self.default_encoding}"
  )
```

**Updated log_dir property**
```python
path = Path(os.getenv('CALCULATOR_LOG_DIR', 'logs'))

if not path.is_absolute():
    path = self.base_dir / path

return path.resolve()
```

**Updated history_dir property**
```python
path = Path(os.getenv('CALCULATOR_HISTORY_DIR', 'history'))

if not path.is_absolute():
    path = self.base_dir / path

return path.resolve()
```

**Updated history_file property**
```python
configured_path = os.getenv('CALCULATOR_HISTORY_FILE')

if configured_path is None:
    return (self.history_dir / "calculator_history.csv").resolve()

path = Path(configured_path)

if not path.is_absolute():
    path = self.base_dir / path

return path.resolve()
```

**Updated log_file property**
```python
path = Path(os.getenv(
    'CALCULATOR_LOG_FILE',
    str(self.log_dir / "calculator.log")
))

if not path.is_absolute():
    path = self.base_dir / path

return path.resolve()
```

**Updated expected thrown error value in test_config.py for precision check**
```python
def test_invalid_precision():
    with pytest.raises(ConfigurationError, match="precision must not be negative"):
        config = CalculatorConfig(precision=-1)
        config.validate()
```

**Updated code for base directory**
```python
self.base_dir = Path(
    base_dir if base_dir is not None
    else os.getenv('CALCULATOR_BASE_DIR', str(project_root))
).resolve()
```