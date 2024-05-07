import unittest
from unittest.mock import mock_open, patch
import os
from inventory_code import *

class TestInventorySystem(unittest.TestCase):
    def setUp(self):
        self.inventory = InventorySystem()
        self.inventory.add_item(InventoryItem("Laptop", 10, 999.99))
        self.inventory.add_item(InventoryItem("Smartphone", 20, 499.99))
        self.inventory.add_item(InventoryItem("Tablet", 5, 299.99))

    def test_add_item(self):
        # Test adding a new item
        response = self.inventory.add_item(InventoryItem("Monitor", 15, 200.00))
        self.assertEqual(response, "Item added successfully.")
        self.assertIn("Monitor", self.inventory.items)

        # Test adding a duplicate item
        response = self.inventory.add_item(InventoryItem("Laptop", 5, 950.00))
        self.assertEqual(response, "Item already exists.")

    def test_update_item(self):
        # Update quantity
        response = self.inventory.update_item("Laptop", quantity=15)
        self.assertEqual(response, "Item updated successfully.")
        self.assertEqual(self.inventory.items["Laptop"].quantity, 15)

        # Update price
        response = self.inventory.update_item("Laptop", price=1050.00)
        self.assertEqual(response, "Item updated successfully.")
        self.assertEqual(self.inventory.items["Laptop"].price, 1050.00)

        # Update non-existing item
        response = self.inventory.update_item("Camera", quantity=10)
        self.assertEqual(response, "Item not found.")

    def test_remove_item(self):
        # Test removing an existing item
        response = self.inventory.remove_item("Smartphone")
        self.assertEqual(response, "Item removed successfully.")
        self.assertNotIn("Smartphone", self.inventory.items)

        # Test removing a non-existent item
        response = self.inventory.remove_item("Camera")
        self.assertEqual(response, "Item not found.")

    def test_list_items(self):
        items_list = self.inventory.list_items()
        self.assertIn("Laptop: 10 units at $999.99 each", items_list)
        self.assertIn("Tablet: 5 units at $299.99 each", items_list)

    def test_get_item(self):
        item = self.inventory.get_item("Laptop")
        self.assertEqual(item, "Laptop: 10 units at $999.99 each")

        # Get non-existing item
        item = self.inventory.get_item("Camera")
        self.assertEqual(item, "Item not found.")

    def test_stock_check(self):
        quantity = self.inventory.stock_check("Laptop")
        self.assertEqual(quantity, 10)

        # Check stock for non-existing item
        quantity = self.inventory.stock_check("Camera")
        self.assertEqual(quantity, "Item not found.")

    def test_calculate_total_value(self):
        total_value = self.inventory.calculate_total_value()
        self.assertEqual(total_value, 10*999.99 + 20*499.99 + 5*299.99)

    def test_restock_item(self):
        response = self.inventory.restock_item("Tablet", 10)
        self.assertEqual(response, "10 units of Tablet restocked successfully.")
        self.assertEqual(self.inventory.items["Tablet"].quantity, 15)

        # Restock non-existing item
        response = self.inventory.restock_item("Camera", 5)
        self.assertEqual(response, "Item not found.")

    def test_notify_low_stock(self):
        response = self.inventory.notify_low_stock(10)
        self.assertEqual(response, "The following items are running low on stock: Tablet")

        response = self.inventory.notify_low_stock(25)
        self.assertEqual(response, "The following items are running low on stock: Laptop, Smartphone, Tablet")

        response = self.inventory.notify_low_stock(5)
        self.assertEqual(response, "No items are running low on stock.")

    @patch('builtins.open', new_callable=mock_open)
    def test_export_import_inventory(self, mock_file):
        # Test exporting inventory
        filename = "test_inventory.csv"
        response = self.inventory.export_inventory(filename)
        self.assertEqual(response, "Inventory exported successfully.")

        # Prepare for importing
        self.inventory.items.clear()

        # Mock data for importing
        mock_file().read.return_value = 'Laptop,10,999.99\nSmartphone,20,499.99\nTablet,5,299.99'
        response = self.inventory.import_inventory(filename)
        self.assertEqual(response, "Inventory imported successfully.")
        self.assertEqual(len(self.inventory.items), 3)
        self.assertEqual(self.inventory.items["Laptop"].quantity, 10)

if __name__ == '__main__':
    unittest.main()
