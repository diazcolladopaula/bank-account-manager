# Transaction Validation

A small Python program that reads a bank transfer request from a JSON file and checks that both IBAN codes are valid Spanish IBAN.

It was written as the first guided exercise of the Software Development course at Universidad Carlos III de Madrid, as a first step before building the account manager in `02-account-manager`.

## How it works

The request file has three fields:

```json
{
  "from": "ES9121000418450200051332",
  "to": "ES7921000813610123456789",
  "receptor_name": "Jose Lopez"
}
```

`TransactionManager.read_transaction_from_json` loads the file and validates both IBAN. A Spanish IBAN is `ES` followed by 22 digits, and its check digits are verified with the ISO 13616 mod-97 algorithm. If everything is correct it returns a `TransactionRequest`; otherwise it raises a `TransactionManagementException` with one of these messages:

| Message | Cause |
|---|---|
| `Wrong file or file path` | The file does not exist |
| `JSON Decode Error - Wrong JSON Format` | The file is not valid JSON |
| `JSON Decode Error - Invalid JSON Key` | A required key is missing |
| `Invalid FROM IBAN` / `Invalid TO IBAN` | The IBAN has the wrong format or check digits |

## Usage

Requires Python 3.8 or later and no external packages.

```bash
python main.py                      # validates sample_transaction.json
python main.py path/to/request.json
```

Example output:

```
TransactionRequest:{"from": "ES9121000418450200051332", "to": "ES7921000813610123456789", "receptor_name": "Jose Lopez"}
IBAN_FROM: ES9121000418450200051332
IBAN_TO: ES7921000813610123456789
```

## Tests

```bash
python -m unittest -v
```

The tests cover IBAN validation (valid codes, wrong check digits, wrong length, wrong country, non-digit characters, non-string input) and each error case when reading a request file.

## Project structure

```
main.py                         Command-line entry point
sample_transaction.json         Example request
bank_manager/
    transaction_manager.py      JSON loading and IBAN validation
    transaction_request.py      Transfer request data object
    transaction_management_exception.py
tests/
    test_transaction_manager.py
```
