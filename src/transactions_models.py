from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation
from enum import Enum
from uuid import UUID


class Currency(str, Enum):
    GBP = "GBP"
    USD = "USD"
    EURO = "EURO"


@dataclass
class Transaction:
    id: UUID
    created_at: datetime | str
    updated_at: datetime | str
    description: str
    amount: Decimal
    currency_code: Currency
    category: str | None
    date: datetime | str
    # @field_validator("create_timestamp", "update_timestamp", mode="before")
    # @classmethod

    def __post_init__(self):
        if isinstance(self.id, str):
            try:
                self.id = UUID(self.id)
            except ValueError:
                raise ValueError(f"Invalid UUID format: '{self.id}'")

        self.created_at = self._parse_timestamp(self.created_at, "create_at")
        self.updated_at = self._parse_timestamp(self.updated_at, "update_at")
        self.description = str(self.description)
        self.amount = self._parse_amount(self.amount, "amount")
        self.category = self._parse_str(self.category, "category")
        self.currency_code = self._parse_currency_code(self.currency_code)
        self.date = self._parse_timestamp(self.date, "date")

    def _parse_amount(self, value, key_name):
        try:
            value = Decimal(value)
        except (ValueError, InvalidOperation):
            raise ValueError(f"Invalid {key_name} format: '{value}'")
        return value

    def _parse_timestamp(self, value, key_name):
        try:
            value = datetime.fromisoformat(value.replace(",", "."))
        except ValueError:
            raise ValueError(f"Invalid {key_name} timestamp: '{value}'")
        return value

    def _parse_str(self, value, key_name):
        if value is not None:
            if not isinstance(value, str):
                raise ValueError(
                    f"{key_name} must be a string or None, got {type(value)}"
                )
            try:
                value = str(value)
            except ValueError:
                raise ValueError(f"Invalid {key_name} format: '{value}'")

        return value

    def _parse_currency_code(self, value):
        try:
            value = Currency(value.upper().strip())
        except ValueError:
            raise ValueError(f"Invalid currency format: '{value}'")
        return value
