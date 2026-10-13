# Konfir Python Test

## The challenge

The aim of this exercise is to demonstrate your problem-solving skill and understanding of Python.

### Instructions
A list of bank transactions is available to you (transactions.csv). Given this raw data, implement the following results:

- Income - Total amount and number of all transactions (e.g. Income: 2 transactions, £1,500)
- Spending - Total amount and number of all transactions  (e.g. Spending: 10 transactions, -£1,500)
- Spending - Total amount and number of transactions per category (e.g. Shopping: £20, 2 transactions - Bills and Utilities: £110, 1 transaction)
- Income - Total amount and number of transactions per payer for the category "salary" 

You may add as many function as you would like


### Additional terms

- We are big on TDD, so we expect you to complete this test using this approach.
- Credit will be given for approach, correctness, clean code, and testing.
- You can take as long as you like to complete the exercise, but for an indicative timescale we expect a senior developer can accomplish this in an hour.
- Please do not use external libraries (except for a testing library)
- You may of course use any resources you like to assist you with specific techniques, syntax etc - but please do not just copy code.
- Please don't share this exercise with anyone else :)


### Instructions for running the tests

With Poetry:

- Run `poetry install` to install dependencies
- Run `poetry run pytest` to run the tests

To setup virtual environment with poetry and pyenv:

- cd fullstack-test-python 
- pyenv install <python version> #e.g: pyenv install 3.13.7
- poetry config --local virtualenvs.in-project true #to setup the virtual in the project instead of home directory
- poetry env use <python version> #e.g: pyenv env use 3.13.7
- source .venv/bin/activate #The virtual environment should be setup in the project
