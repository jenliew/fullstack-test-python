import uuid
from decimal import Decimal

import pytest

from calculator import Currency
from main import Calculator
from transactions_models import Transaction


@pytest.fixture
def mock_transaction_list() -> list[Transaction]:
    return [
        Transaction(
            id=uuid.uuid4(),
            created_at="2022-07-01 07:24:30",
            updated_at="2022-07-01 07:24:35",
            description="TRAINLINE TICKET ONLINE GB ",
            amount=Decimal("-21.55"),
            currency_code=Currency.GBP,
            category="Transport",
            date="2019-01-03 00:00:00",
        ),
        Transaction(
            id=uuid.uuid4(),
            created_at="2022-07-01 07:24:30",
            updated_at="2022-07-01 07:24:35",
            description="ASDA SUPERSTORE London GB",
            amount=Decimal("-35.15"),
            currency_code=Currency.GBP,
            category="Shopping",
            date="2019-01-15 00:00:00",
        ),
        Transaction(
            id=uuid.uuid4(),
            created_at="2022-07-01 07:24:30",
            updated_at="2022-07-01 07:24:35",
            description="WEB GENIUS",
            amount=Decimal("1400.00"),
            currency_code=Currency.GBP,
            category="Salary",
            date="2019-01-02 00:00:00",
        ),
        Transaction(
            id=uuid.uuid4(),
            created_at="2022-07-01 07:24:30",
            updated_at="2022-07-01 07:24:35",
            description="RESTAURANT PAYMENT OTLEY GB",
            amount=Decimal("-41.20"),
            currency_code=Currency.GBP,
            category=None,
            date="2019-01-02 00:00:00",
        ),
        Transaction(
            id=uuid.uuid4(),
            created_at="2022-07-01 07:24:30",
            updated_at="2022-07-01 07:24:35",
            description="RESTAURANT PAYMENT OTLEY GB",
            amount=Decimal("-28.53"),
            currency_code=Currency.GBP,
            category=None,
            date="2019-02-16 13:40:00",
        ),
        Transaction(
            id=uuid.uuid4(),
            created_at="2022-07-01 07:24:30",
            updated_at="2022-07-01 07:24:35",
            description="WEB GENIUS",
            amount=Decimal("1200.00"),
            currency_code=Currency.GBP,
            category="Salary",
            date="2019-02-01 01:00:00",
        ),
        Transaction(
            id=uuid.uuid4(),
            created_at="2022-07-01 07:24:30",
            updated_at="2022-07-01 07:24:35",
            description="MONTHLY INTERNET BILL",
            amount=Decimal("-20.00"),
            currency_code=Currency.GBP,
            category="Bills and Utilities",
            date="2019-01-08 00:00:00",
        ),
        Transaction(
            id=uuid.uuid4(),
            created_at="2022-07-01 07:24:30",
            updated_at="2022-07-01 07:24:35",
            description="RESTAURANT PAYMENT Oslo",
            amount=Decimal("-30.10"),
            currency_code=Currency.EURO,
            category="Food & Dining",
            date="2019-02-15 12:50:00",
        ),
        Transaction(
            id=uuid.uuid4(),
            created_at="2022-07-01 07:24:30",
            updated_at="2022-07-01 07:24:35",
            description="UBER",
            amount=Decimal("400.00"),
            currency_code=Currency.GBP,
            category=None,
            date="2019-02-04 09:10:00",
        ),
    ]


@pytest.mark.parametrize(
    ("mock_transactions, expected_result"),
    [
        (
            [
                Transaction(
                    id=uuid.uuid4(),
                    created_at="2022-07-01 07:24:30",
                    updated_at="2022-07-01 07:24:35",
                    description="DESCRIPTION 1",
                    amount=Decimal("-52.98"),
                    currency_code=Currency.GBP,
                    category="Shopping",
                    date="2019-01-02 00:00:00",
                ),
                Transaction(
                    id=uuid.uuid4(),
                    created_at="2022-07-01 07:24:30",
                    updated_at="2022-07-01 07:24:35",
                    description="DESCRIPTION 2",
                    amount=Decimal("-100.00"),
                    currency_code=Currency.GBP,
                    category="Food & Dinning",
                    date="2019-01-02 00:00:00",
                ),
                Transaction(
                    id=uuid.uuid4(),
                    created_at="2022-07-01 07:24:30",
                    updated_at="2022-07-01 07:24:35",
                    description="DESCRIPTION 2",
                    amount=Decimal("-40.00"),
                    currency_code=Currency.GBP,
                    category="Bills and Utilities",
                    date="2019-01-02 00:00:00",
                ),
            ],
            {"GBP": {"count": 3, "total": Decimal("-192.98")}},
        ),
        (
            [
                Transaction(
                    id=uuid.uuid4(),
                    created_at="2022-07-01 07:24:30",
                    updated_at="2022-07-01 07:24:35",
                    description="DESCRIPTION 21",
                    amount=Decimal("100.00"),
                    currency_code=Currency.GBP,
                    category="Salary",
                    date="2019-01-02 00:00:00",
                ),
                Transaction(
                    id=uuid.uuid4(),
                    created_at="2022-07-01 07:24:30",
                    updated_at="2022-07-01 07:24:35",
                    description="DESCRIPTION 21",
                    amount=Decimal("-50.10"),
                    currency_code=Currency.GBP,
                    category="Healthcare",
                    date="2019-01-02 00:00:00",
                ),
                Transaction(
                    id=uuid.uuid4(),
                    created_at="2022-07-01 07:24:30",
                    updated_at="2022-07-01 07:24:35",
                    description="DESCRIPTION 21",
                    amount=Decimal("-120.00"),
                    currency_code=Currency.GBP,
                    category=None,
                    date="2019-01-02 00:00:00",
                ),
            ],
            {"GBP": {"count": 2, "total": Decimal("-170.10")}},
        ),
    ],
)
def test_get_total_spending(
    mock_transactions: list[Transaction],
    expected_result: dict[str, dict[str, int | Decimal]],
):

    calc = Calculator(mock_transactions)

    assert calc.get_total_spending() == expected_result


def test_empty_transaction_list():

    calc = Calculator([])
    assert len(calc.transactions_by_currency) == 0
    assert calc.get_total_spending() == {}
    assert calc.get_spending_by_category() == {}
    assert calc.get_total_spending() == {}
    assert calc.get_salary_income_by_payer() == {}
    assert calc.get_monthly_expenses() == {}


def test_group_by_currency_normalizes_currency_codes(mock_transaction_list):

    result_curr = Calculator._group_by_currency(mock_transaction_list)

    assert set(result_curr) == {"GBP", "EURO"}
    assert len(result_curr["GBP"]) == 8
    assert len(result_curr["EURO"]) == 1


def test_group_by_currency_uses_unknown_category(mock_transaction_list):

    mock_transaction_list.append(
        Transaction(
            id=uuid.uuid4(),
            created_at="2022-07-01 07:24:30",
            updated_at="2022-07-01 07:24:35",
            description="MONTHLY INTERNET BILL",
            amount=Decimal("-10.00"),
            currency_code=Currency.GBP,
            category=None,
            date="2019-02-01 01:00:00",
        )
    )

    calc = Calculator(mock_transaction_list)
    result = calc.get_spending_by_category()

    assert result == {
        "GBP": {
            "others": {"count": 3, "total": Decimal("-79.73")},
            "transport": {"count": 1, "total": Decimal("-21.55")},
            "shopping": {"count": 1, "total": Decimal("-35.15")},
            "bills and utilities": {"count": 1, "total": Decimal("-20.00")},
        },
        "EURO": {"food & dining": {"count": 1, "total": Decimal("-30.10")}},
    }

    result = calc.get_salary_income_by_payer()

    assert result == {
        "GBP": {
            "WEB GENIUS": {"count": 2, "total": Decimal("2600.00")},
        },
        "EURO": {},
    }


def test_get_credit_benefit_list(mock_transaction_list: list[Transaction]):
    calc = Calculator(mock_transaction_list)
    assert calc.get_total_credits() == {
        "GBP": {"count": 1, "total": Decimal("400.00")},
        "EURO": {"count": 0, "total": Decimal("0.00")},
    }


@pytest.mark.parametrize(
    ("mock_tx,expected_result"),
    [
        (
            Transaction(
                id=uuid.uuid4(),
                created_at="2022-07-01 07:24:30",
                updated_at="2022-07-01 07:24:35",
                description="RESTAURANT PAYMENT OTLEY GB",
                amount=Decimal("-41.20"),
                currency_code=Currency.GBP,
                category=None,
                date="2019-01-02 00:00:00",
            ),
            "others",
        ),
        (
            Transaction(
                id=uuid.uuid4(),
                created_at="2022-07-01 07:24:30",
                updated_at="2022-07-01 07:24:35",
                description="WEB GENIUS",
                amount=Decimal("1200.00"),
                currency_code=Currency.GBP,
                category="Salary",
                date="2019-02-01 01:00:00",
            ),
            "salary",
        ),
        (
            Transaction(
                id=uuid.uuid4(),
                created_at="2022-07-01 07:24:30",
                updated_at="2022-07-01 07:24:35",
                description="RESTAURANT PAYMENT Oslo",
                amount=Decimal("-30.10"),
                currency_code=Currency.EURO,
                category="Food & Dining",
                date="2019-02-15 12:50:00",
            ),
            "food & dining",
        ),
    ],
)
def test_retrieve_category(mock_tx: Transaction, expected_result: str) -> None:

    assert Calculator._category(mock_tx) == expected_result
