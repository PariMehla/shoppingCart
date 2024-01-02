
# This file creates an electronic shopping cart for each customer. It constantly updates the inventory by adding and removing items from the shopping cart.


# To represent products, define a product class.
class Product:
    def __init__(self, name, price, category):
        # Set up the products properties and attributes.
        self._name = name
        self._price = price
        self._category = category

    def __eq__(self, other):
        # Compare the properties and attributes of two items to see if they are equivalent.
        if isinstance(other, Product):
            return (self._name == other._name and self._price == other._price and self._category == other._category)
        else:
            return False

    def get_name(self):
        # Find out the product's name.
        return self._name

    def get_price(self):
        # Find out the product's pricing.
        return self._price

    def get_category(self):
        # Find the product's category.
        return self._category

    def __repr__(self):
        # The product's string representation.
        return f'Product({self._name} , {self._price} , {self._category})'

# Create an inventory class to control the costs and quantities of products.
class Inventory:
    def __init__(self):
        # Create a blank dictionary initially to hold product inventory.
        self._items = {}

    def add_to_productInventory(self, productName, productPrice, productQuantity):
        # Enter a product in the inventory with price, quantity and name.
        self._items[productName] = {'price': productPrice, 'quantity': productQuantity}

    def add_productQuantity(self, nameProduct, addQuantity):
        # Increase the quantity of an already-existing product in the inventory.
        if nameProduct in self._items:
            self._items[nameProduct]['quantity'] += addQuantity

    def remove_productQuantity(self, nameProduct, removeQuantity):
        # Remove the quantity of an already-existing product in the inventory.
        if nameProduct in self._items:
            self._items[nameProduct]['quantity'] -= removeQuantity

    def get_productPrice(self, nameProduct):
        # Locate a product's price in the inventory.
        return self._items[nameProduct]['price']

    def get_productQuantity(self, nameProduct):
        # Determine a product's quantity from the inventory.
        return self._items[nameProduct]['quantity']

    def display_Inventory(self):
        # Present the inventory's contents
        for name, info in self._items.items():
            print(f'{name}, {info["price"]}, {info["quantity"]}')

# To manage the items in a shopping cart, define a class called ShoppingCart.
class ShoppingCart:
    def __init__(self, buyerName, inventory):
        # Initialize the shopping cart with an inventory a buyer's name.
        self._buyerName = buyerName
        self._inventory = inventory
        self._cart = {}  # Create an empty cart.

    def add_to_cart(self, nameProduct, requestedQuantity):
        # Add an item to the cart with the provided specified quantity
        if self._inventory.get_productQuantity(nameProduct) >= requestedQuantity:
            self._inventory.remove_productQuantity(nameProduct, requestedQuantity)
            self._cart[nameProduct] = self._cart.get(nameProduct, 0) + requestedQuantity
            return "Filled the order"
        else:
            return "Can not fill the order"

    def remove_from_cart(self, nameProduct, requestedQuantity):
        # Take out a product from the cart with the provided specified quantity.
        if nameProduct not in self._cart:
            return "Product not in the cart"
        elif self._cart[nameProduct] < requestedQuantity:
            return "The requested quantity to be removed from cart exceeds what is in the cart"
        else:
            self._cart[nameProduct] -= requestedQuantity
            self._inventory.add_productQuantity(nameProduct, requestedQuantity)
            if self._cart[nameProduct] == 0:
                del self._cart[nameProduct]
            return "Successful"

    def view_cart(self):
        # Examine what's in the shopping cart and calculate how much it will cost overall.
        total = 0
        for product, quantity in self._cart.items():
            price = self._inventory.get_productPrice(product)
            total += price * quantity
            print(f'{product} {quantity}')
        print(f'Total:  {total}')
        print(f'Buyer Name: {self._buyerName}')

# To handle the product catalogue, define a ProductCatalog class.
class ProductCatalog:
    def __init__(self):
        # Create an empty list to hold products in the catalog.
        self._products = []

    def addProduct(self, product):
        # Add a product to the catalog.
        self._products.append(product)

    def price_category(self):
        # Calculate and display the quantity of products available in carious pricing ranges.
        low_prices, medium_prices, high_prices = 0, 0, 0
        for product in self._products:
            price = product.get_price()
            if price < 100:
                low_prices += 1
            elif 100 <= price < 500:
                medium_prices += 1
            else:
                high_prices += 1
        print(f'Number of low price items: {low_prices}')
        print(f'Number of medium price items: {medium_prices}')
        print(f'Number of high price items: {high_prices}')

    def display_catalog(self):
        # Show the products lsited in the catalog.
        for product in self._products:
            print(f'Product: {product.get_name()} Price: {product.get_price()} Category: {product.get_category()}')

# The function to populate an inventory from a CSV file.
def populate_inventory(filename):
    inventory = Inventory()
    try:
        with open(filename, 'r') as file:
            for line in file:
                name, price, quantity, _ = line.strip().split(',')
                inventory.add_to_productInventory(name, int(price), int(quantity))
    except FileNotFoundError:
        print(f"Could not read file: {filename}")
    return inventory

# The function to populate a product catalog from a CSV file.
def populate_catalog(filename):
    catalog = ProductCatalog()
    try:
        with open(filename, 'r') as file:
            for line in file:
                name, price, quantity, category = line.strip().split(',')
                product = Product(name, int(price), category)
                catalog.addProduct(product)
    except FileNotFoundError:
        print(f"Could not read file: {filename}")
    return catalog

