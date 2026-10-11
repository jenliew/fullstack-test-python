import logging
from csv import DictReader

import pytest

from main import normalise_transactions

logger = logging.getLogger(__name__)


@pytest.fixture
def transactions():
    with open("transactions.csv") as f:
        yield list(DictReader(f))


def test_normalise_transactions(transactions):
    normalise_transactions(transactions)
    assert True
