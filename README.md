# Bank Account Manager

[Versión en español](README.es.md)

A Python module for managing bank transfers, deposits and account balances, built in three stages as coursework for the Software Development course at Universidad Carlos III de Madrid. Each stage lives in its own folder, so the repository shows how the same problem was first solved, then tested more carefully, and finally restructured.

| Folder | What it contains |
|---|---|
| [`01-transaction-validation`](01-transaction-validation) | A script that reads a transfer request from JSON and validates both IBAN codes |
| [`02-account-manager`](02-account-manager) | `AccountManager` with transfers, deposits and balance calculation, developed test-first with a documented test design |
| [`03-refactoring`](03-refactoring) | The same features refactored so that each field validates itself, with storage separated from the business logic |

All three work with Spanish IBAN (`ES` plus 22 digits) and check them with the ISO 13616 mod-97 algorithm.

## Running the tests

Each folder is independent. Python 3.8 or later is needed; the tests of folders 02 and 03 use [`freezegun`](https://pypi.org/project/freezegun/) to fix the current date.

```bash
cd 01-transaction-validation
python -m unittest

cd ../02-account-manager        # same for 03-refactoring
pip install freezegun
PYTHONPATH=src/main/python python -m unittest discover -s src/unittest/python -t src/unittest/python
```

On Windows PowerShell, set the path with `$env:PYTHONPATH = "src/main/python"` before running the last command. Folders 02 and 03 also include a PyBuilder configuration (`build.py`, `pylintrc`) used during the course.

## Notes

- This is academic work: the validation rules (amount range, concept format, accepted dates, file formats) come from the assignment specifications, not from real banking requirements.
- Transfer codes are MD5 hashes and deposit signatures are SHA-256 hashes, as the assignment required. They identify records; they are not meant to be secure.
