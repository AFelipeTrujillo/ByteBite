from dataclasses import dataclass
from src.Domain.ValueObject.Unit import Unit


@dataclass(frozen=True)
class IngredientQuantity:
    amount: float
    unit: Unit

    def __add__(self, other: "IngredientQuantity") -> 'IngredientQuantity':
        if self.unit != other.unit:
            raise ValueError(f"You cannot add {self.unit} to {other.unit}")

        return IngredientQuantity(self.amount + other.amount, self.unit)