import logging
from collections import defaultdict
from decimal import Decimal

from transactions_models import Currency, Transaction

logger = logging.getLogger(__name__)


class Calculator:
    def __init__(self, transaction_list: list["Transaction"]) -> None:
        self.transactions_by_currency: dict[str, list[Transaction]] = (
            self._group_by_currency(transaction_list)
        )

    @staticmethod
    def _group_by_currency(
        transactions: list[Transaction],
    ) -> dict[str, list[Transaction]]:
        grouped: defaultdict[str, list[Transaction]] = defaultdict(list)

        for tx in transactions:
            currency = (tx.currency_code or "").strip().upper() or "UNKNOWN"
            if tx.category:
                tx.category.lower()
            grouped[currency].append(tx)

        return dict(grouped)

    @staticmethod
    def _category(transaction: Transaction) -> str:
        return (
            transaction.category.strip().lower()
            if transaction.category and transaction.category.strip()
            else "others"
        )

    @staticmethod
    def amount_formater(amount: Decimal, symbol_str: str) -> str:
        # Construct the summary of the transaction
        return f"{'-' if amount < 0 else ''}{symbol_str}{abs(amount):,.2f}"

    @staticmethod
    def printout(transaction_summary: dict) -> str:
        lines = []

        for currency, items in transaction_summary.items():
            # Attempt to get the symbol of the currency
            try:
                symbol = Currency(currency).symbol
            except ValueError:
                symbol = f"{currency} "

            # A single summary: {"count": ..., "total": ...}
            if "count" in items and "total" in items:
                count = items["count"]
                total = Decimal(str(items["total"]))
                tx_word = "transaction" if count == 1 else "transactions"

                lines.append(
                    f"{Calculator.amount_formater(total, symbol)}, {count} {tx_word}"
                )
                continue

            # A breakdown: category/payer -> {"count": ..., "total": ...}
            for name, summary in items.items():
                count = summary["count"]
                total = Decimal(str(summary["total"]))
                tx_word = "transaction" if count == 1 else "transactions"

                lines.append(
                    f"{name}: {Calculator.amount_formater(total, symbol)}, {count} {tx_word}"
                )

        return "\n".join(lines)

    def get_total_income(self) -> dict:
        result = {}
        for currency, transaction in self.transactions_by_currency.items():
            income_tx = [
                tx
                for tx in transaction
                if (self._category(tx) == "salary") and tx.amount > 0
            ]

            result[currency] = {
                "count": len(income_tx),
                "total": sum((tx.amount for tx in income_tx), Decimal("0.00")),
            }
        return result

    def get_total_spending(self) -> dict:
        result = {}
        for currency, transaction in self.transactions_by_currency.items():
            spending_tx = [tx for tx in transaction if tx.amount < 0]
            result[currency] = {
                "count": len(spending_tx),
                "total": sum(
                    (tx.amount for tx in spending_tx), Decimal("0.00")
                ),
            }
        return result

    def get_spending_by_category(self) -> dict:
        result = {}
        for currency, transcation in self.transactions_by_currency.items():
            totals = self._default_tx_dict()

            for tx in transcation:
                if tx.amount >= 0:
                    # If the amount is positive, means it's
                    # credit or income, so skip it.
                    continue

                category = self._category(tx)
                totals[category]["count"] += 1
                totals[category]["total"] += tx.amount

            result[currency] = dict(totals)

        return result

    def get_salary_income_by_payer(self) -> dict:
        result = {}
        for currency, transcation in self.transactions_by_currency.items():
            totals = self._default_tx_dict()

            for tx in transcation:
                if self._category(tx) != "salary" or tx.amount <= 0:
                    continue

                payer = (tx.description or "").strip() or "Unknown payer"

                totals[payer]["count"] += 1
                totals[payer]["total"] += tx.amount

            result[currency] = dict(totals)
        return result

    def get_monthly_expenses(self) -> dict:
        result = {}

        for currency, transactions in self.transactions_by_currency.items():
            monthly_totals = self._default_tx_dict()

            for tx in transactions:
                if tx.amount >= 0:
                    continue

                # Assumes transaction_date is a date or datetime object
                month_key_name = tx.date.strftime("%Y-%m")

                monthly_totals[month_key_name]["count"] += 1
                monthly_totals[month_key_name]["total"] += abs(tx.amount)

            result[currency] = dict(sorted(monthly_totals.items()))

        return result

    def _default_tx_dict(self) -> dict:
        return defaultdict(
            lambda: {
                "count": 0,
                "total": Decimal("0.00"),
            }
        )

    def get_total_credits(self) -> dict:
        result = {}

        for currency, transaction in self.transactions_by_currency.items():
            # Any transaction is not under the "Salary" category and the
            # amount is positive value. It will fall under credit summary
            # This include refund, benefits and gift card (if there's any)
            credit_tx = [
                tx
                for tx in transaction
                if tx.amount > 0 and self._category(tx) != "salary"
            ]

            result[currency] = {
                "count": len(credit_tx),
                "total": sum(
                    (tx.amount for tx in credit_tx),
                    Decimal("0.00"),
                ),
            }

        return result
