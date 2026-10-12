import logging

from calculator import Calculator
from transactions_models import Transaction

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s %(levelname)s: %(message)s"
)
logger = logging.getLogger(__name__)


def normalise_transactions(transactions: list):
    # Initialising the transaction list.
    transaction_list = []
    for i in transactions:
        try:
            item = Transaction(**i)
            transaction_list.append(item)

        except (ValueError, TypeError, KeyError):
            logger.exception("Failed process %s", i)

    return Calculator(transaction_list)


def get_total_income_summary(calc_obj: Calculator) -> str:
    if calc_obj is None:
        raise ValueError("calc_obj cannot be None")

    total_income = calc_obj.get_total_income()

    return calc_obj.printout(total_income)


def get_total_spending_summary(calc_obj: Calculator) -> str:
    if calc_obj is None:
        raise ValueError("calc_obj cannot be None")

    total_expenses = calc_obj.get_total_spending()
    return calc_obj.printout(total_expenses)


def get_spending_by_category_summary(calc_obj: Calculator) -> str:
    if calc_obj is None:
        raise ValueError("calc_obj cannot be None")

    expenses_by_category = calc_obj.get_spending_by_category()
    return calc_obj.printout(expenses_by_category)


def get_income_by_payer_summary(calc_obj: Calculator) -> str:
    if calc_obj is None:
        raise ValueError("calc_obj cannot be None")

    total_income_payer = calc_obj.get_salary_income_by_payer()
    return calc_obj.printout(total_income_payer)


def get_monthly_expenses_summary(calc_obj: Calculator) -> str:
    if calc_obj is None:
        raise ValueError("calc_obj cannot be None")

    expenses_by_monthly = calc_obj.get_monthly_expenses()
    return calc_obj.printout(expenses_by_monthly)


def get_credit_benefits_transaction_summary(calc_obj: Calculator) -> str:
    if calc_obj is None:
        raise ValueError("calc_obj cannot be None")

    credit_benefits_summary = calc_obj.get_total_credits()
    return calc_obj.printout(credit_benefits_summary)
