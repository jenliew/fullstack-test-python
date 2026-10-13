import uuid
from datetime import datetime
from decimal import Decimal

import pytest

from transactions_models import Currency, Transaction


@pytest.mark.parametrize(
    (
        "create_timestamp, updated_timestamp, description, int_amount, currency,category_str,date"
    ),
    [
        (
            "2026-10-01 01:20:30",
            "2026-01-11 03:14:15",
            "DESCRIPTION 1",
            Decimal(100),
            Currency.GBP,
            None,
            "2026-01-13 00:00:00",
        ),
        (
            "2026-06-01 10:11:30",
            "2026-06-14 14:20:00",
            "DESCRIPTION 22",
            Decimal(-45),
            Currency.EURO,
            "Shopping",
            "2026-09-14 08:02:17",
        ),
    ],
)
def test_transaction_items(
    create_timestamp: str,
    updated_timestamp: str,
    description: str,
    int_amount: Decimal,
    currency: Currency,
    category_str: str | None,
    date: str,
):
    tx_test = Transaction(
        id=uuid.uuid4(),
        created_at=create_timestamp,
        updated_at=updated_timestamp,
        description=description,
        amount=int_amount,
        currency_code=currency,
        category=category_str,
        date=date,
    )

    assert isinstance(tx_test.id, uuid.UUID)
    assert tx_test.created_at == (datetime.fromisoformat(create_timestamp))
    assert tx_test.updated_at == (datetime.fromisoformat(updated_timestamp))
    assert tx_test.category == category_str
    assert tx_test.amount == int_amount
    assert tx_test.date == (datetime.fromisoformat(date))
    assert tx_test.currency_code == currency


@pytest.mark.parametrize(
    (
        "create_timestamp, updated_timestamp, description, int_amount, currency,category_str,date,error_msg"
    ),
    [
        (
            "2026-10-01 01:20:30:abc30",
            "2026-01-11 03:14:15",
            "DESCRIPTION 1",
            Decimal(100),
            Currency.GBP,
            None,
            "2026-01-13 00:00:00",
            "Invalid create_at timestamp: '2026-10-01 01:20:30:abc30'",
        ),
        (
            "2026-06-01 10:11:30",
            "2026-06-14 14:20:00",
            "DESCRIPTION 22",
            "false",
            Currency.EURO,
            "Shopping",
            "2026-09-14 08:02:17",
            "Invalid amount format: 'false'",
        ),
        (
            "2026-07-01 09:15:00",
            "2026-07-20 08:18:00",
            "DESCRIPTION 23",
            Decimal(17),
            Currency.EURO,
            "",
            "bac2026-09-14 08:02:17",
            "Invalid date timestamp: 'bac2026-09-14 08:02:17'",
        ),
    ],
)
def test_invalid_transaction_item(
    create_timestamp: str,
    updated_timestamp: str,
    description: str,
    int_amount: int,
    currency: Currency,
    category_str: str | None,
    date: str,
    error_msg: str,
):

    with pytest.raises(ValueError, match=error_msg):
        Transaction(
            id=uuid.uuid4(),
            created_at=create_timestamp,
            updated_at=updated_timestamp,
            description=description,
            amount=Decimal(str(int_amount)),
            currency_code=currency,
            category=category_str,
            date=date,
        )
