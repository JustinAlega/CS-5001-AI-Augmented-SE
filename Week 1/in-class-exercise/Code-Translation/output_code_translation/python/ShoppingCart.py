from typing import Dict, Tuple

class ShoppingCart:
    def __init__(self) -> None:
        self.items: Dict[str, Tuple[float, int]] = {}

    def add_item(self, item: str, price: float, quantity: int = 1) -> None:
        # In the original C++ both branches assign the same value,
        # so we simply set/overwrite the entry.
        self.items[item] = (price, quantity)

    def remove_item(self, item: str, quantity: int = 1) -> None:
        if item in self.items:
            price, current_qty = self.items[item]
            new_qty = current_qty - quantity
            if new_qty <= 0:
                del self.items[item]
            else:
                self.items[item] = (price, new_qty)

    def view_items(self) -> Dict[str, Tuple[float, int]]:
        # Return a shallow copy to mirror C++ returning a copy of the map
        return self.items.copy()

    def total_price(self) -> float:
        total = 0.0
        for price, qty in self.items.values():
            total += price * qty
        return total
