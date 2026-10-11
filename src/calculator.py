import logging
from collections import defaultdict
from decimal import Decimal

from transactions_models import Transaction

logger = logging.getLogger(__name__)


class Calculator:
    def __init__(self, transaction_list: list["Transaction"]) -> None:
        self.transaction_list = transaction_list

    @staticmethod
    def _category(transaction: "Transaction") -> str:
        return (
            transaction.category.strip().lower()
            if transaction.category and transaction.category.strip()
            else "unknown_category"
        )

    def get_total_income(self) -> dict:
        transactions = [tx for tx in self.transaction_list if tx.amount > 0]

        return {
            "count": len(transactions),
            "total": sum(tx.amount for tx in transactions),
        }

    def get_total_spending(self) -> dict:
        transactions = [tx for tx in self.transaction_list if tx.amount < 0]

        return {
            "count": len(transactions),
            "total": sum(tx.amount for tx in transactions),
        }

    def get_spending_by_category(self) -> dict:
        totals = defaultdict(
            lambda: {
                "count": 0,
                "total": Decimal("0.00"),
            }
        )

        for tx in self.transaction_list:
            if tx.amount >= 0:
                continue

            category = self._category(tx)
            totals[category]["count"] += 1
            totals[category]["total"] += tx.amount

        return dict(totals)

    def get_salary_income_by_payer(self) -> dict:
        totals = defaultdict(
            lambda: {
                "count": 0,
                "total": Decimal("0.00"),
            }
        )

        for tx in self.transaction_list:
            if self._category(tx) != "salary" or tx.amount <= 0:
                continue

            payer = (tx.description or "").strip() or "Unknown payer"

            totals[payer]["count"] += 1
            totals[payer]["total"] += tx.amount

        return dict(totals)
