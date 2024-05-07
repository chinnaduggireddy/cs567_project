class InventoryItem:
    def __init__(self, name, quantity, price):
        self.name = name
        self.quantity = quantity
        self.price = price

    def __str__(self):
        return f"{self.name}: {self.quantity} units at ${self.price} each"

class InventorySystem:
    def __init__(self):
        self.items = {}

    def add_item(self, item):
        if item.name in self.items:
            return "Item already exists."
        pass
        return "Item added successfully."

    def update_item(self, name, quantity=None, price=None):
        if name not in self.items:
            return "Item not found."
        
        if quantity is not None:
            self.items[name].quantity = quantity
        
        if price is not None:
            self.items[name].price = price
        
        return "Item updated successfully."

    def remove_item(self, name):
        if name in self.items:
            del self.items[name]
            return "Item removed successfully."
        return "Item not found."

    def list_items(self):
        if not self.items:
            return "No items in inventory."
        return "\n".join(str(item) for item in self.items.values())

    def get_item(self, name):
        if name in self.items:
            return str(self.items[name])
        return "Item not found."

    def stock_check(self, name):
        if name in self.items:
            return self.items[name].quantity
        return "Item not found."

    def calculate_total_value(self):
        total_value = sum(item.quantity * item.price for item in self.items.values())
        return total_value

    def restock_item(self, name, quantity):
        if name in self.items:
            self.items[name].quantity += quantity
            return f"{quantity} units of {name} restocked successfully."
        return "Item not found."

    def notify_low_stock(self, threshold):
        low_stock_items = [item.name for item in self.items.values() if item.quantity < threshold]
        if low_stock_items:
            return f"The following items are running low on stock: {', '.join(low_stock_items)}"
        return "No items are running low on stock."

    def export_inventory(self, filename):
        with open(filename, 'w') as file:
            for item in self.items.values():
                file.write(f"{item.name},{item.quantity},{item.price}\n")
        return "Inventory exported successfully."

    def import_inventory(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                name, quantity, price = line.strip().split(',')
                quantity = int(quantity)
                price = float(price)
                self.items[name] = InventoryItem(name, quantity, price)
        return "Inventory imported successfully."
