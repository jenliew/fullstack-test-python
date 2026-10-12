import logging
from csv import DictReader

import pytest

from main import (
    Transaction,
    get_credit_benefits_transaction_summary,
    get_income_by_payer_summary,
    get_monthly_expenses_summary,
    get_spending_by_category_summary,
    get_total_income_summary,
    get_total_spending_summary,
    normalise_transactions,
)

logger = logging.getLogger(__name__)


@pytest.fixture
def transactions():
    with open("transactions.csv") as f:
        yield list(DictReader(f))


def test_normalise_transactions(transactions: list[Transaction]):
    calc_obj = normalise_transactions(transactions)
    assert len(calc_obj.transactions_by_currency) == 2
    assert "EURO" in calc_obj.transactions_by_currency
    assert "GBP" in calc_obj.transactions_by_currency


def test_get_total_income_summary(transactions: list[Transaction]):
    calc_obj = normalise_transactions(transactions)

    result = get_total_income_summary(calc_obj)

    assert result == "£9,700.00, 6 transactions\n€0.00, 0 transactions"


def test_get_total_spending_summary(transactions: list[Transaction]):
    calc_obj = normalise_transactions(transactions)
    result = get_total_spending_summary(calc_obj)

    assert result == "-£1,025.11, 35 transactions\n-€86.49, 2 transactions"


def test_get_spending_by_category_summary(transactions: list[Transaction]):
    calc_obj = normalise_transactions(transactions)
    result = get_spending_by_category_summary(calc_obj)

    assert result == (
        "others: -£141.75, 4 transactions\n"
        "shopping: -£280.35, 11 transactions\n"
        "food & dining: -£73.35, 4 transactions\n"
        "bills and utilities: -£408.48, 8 transactions\n"
        "transport: -£39.05, 3 transactions\n"
        "entertainment: -£30.99, 2 transactions\n"
        "healthcare: -£21.15, 2 transactions\n"
        "health and fitness: -£29.99, 1 transaction\n"
        "food & dining: -€36.50, 1 transaction\n"
        "shopping: -€49.99, 1 transaction"
    )


def test_get_income_by_payer_summary(transactions: list[Transaction]):
    calc_obj = normalise_transactions(transactions)
    result = get_income_by_payer_summary(calc_obj)

    assert result == "WEB GENIUS: £9,700.00, 6 transactions"


def test_get_monthly_expenses_summary(transactions: list[Transaction]):
    calc_obj = normalise_transactions(transactions)
    result = get_monthly_expenses_summary(calc_obj)
    assert result == (
        "2019-01: £450.31, 12 transactions\n"
        "2019-02: £317.26, 15 transactions\n"
        "2019-03: £196.15, 6 transactions\n"
        "2019-04: £61.39, 2 transactions\n"
        "2019-02: €86.49, 2 transactions"
    )


def test_get_credit_benefits_transaction(transactions: list[Transaction]):
    calc_obj = normalise_transactions(transactions)
    result = get_credit_benefits_transaction_summary(calc_obj)
    assert result == ("£409.45, 3 transactions\n€0.00, 0 transactions")


def test_failed_normalise_transaction():
    with pytest.raises(ValueError, match="calc_obj cannot be None"):
        get_credit_benefits_transaction_summary(None)
