import logging

from calculator import Calculator
from transactions_models import Transaction

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)


def normalise_transactions(transactions: list):

    transaction_list = []
    for i in transactions:
        try:
            item = Transaction(**i)
            transaction_list.append(item)

        except (ValueError, TypeError, KeyError):
            logger.exception("Failed process %s", i)

    calculate_tx = Calculator(transaction_list)

    total_income = calculate_tx.get_total_income()

    total_expenses = calculate_tx.get_total_spending()

    expenses_by_category = calculate_tx.get_spending_by_category()

    total_income_payer = calculate_tx.get_salary_income_by_payer()
    logger.info(
        "%s %s, %s, %s",
        total_income,
        total_expenses,
        expenses_by_category,
        total_income_payer,
    )
