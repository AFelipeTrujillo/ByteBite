from enum import Enum

class Category(Enum):
    VEGETABLES  = 101
    DAIRY_EGGS  = 102
    MEAT_FISH   = 103
    PANTRY      = 104
    SPICES      = 105
    FRUITS      = 106
    FROZEN      = 107
    OTHERS      = 999

    @property
    def label(self) -> str:
        """Returns a human-readable string for the UI."""
        _labels = {
            Category.VEGETABLES: "Vegetables & Greens",
            Category.DAIRY_EGGS: "Dairy & Eggs",
            Category.MEAT_FISH:  "Meat & Seafood",
            Category.PANTRY:     "Pantry Essentials",
            Category.SPICES:     "Herbs & Spices",
            Category.FRUITS:     "Fresh Fruits",
            Category.FROZEN:     "Frozen Foods",
            Category.OTHERS:     "Everything Else"
        }
        return _labels.get(self, "Unknown")

    def __str__(self):
        return self.label