# Module: Multi Paradigm Programming
# Paradigm: Object Orientated
# Author: Ante Dujic

import csv

# Product class
class Product:
    def __init__(self, name, price=0): # Price set to 0, doesn't have to be passed when creating a class instance
        self.name = name
        self.price = price

    # String represantation of the class objects
    def __repr__(self):
        str = f"PRODUCT NAME: {self.name}\n"
        str += f"PRODUCT PRICE: EUR {self.price}\n"
        return str

# ProductStock class
class ProductStock:
    def __init__(self, product, quantity):
        self.product = product  # Class product will be passed here
        self.quantity = quantity

    # Method to get product name
    def name(self):
        return self.product.name
    # Method to get product price
    def price(self):
        return self.product.price
    # Method to calculate/get product cost
    def cost(self):
        return self.price() * self.quantity
    # String representation
    def __repr__(self):
        return "{}ON STOCK: {}\n-------------------------------------------------".format(self.product, int(self.quantity))

# Shop class
class Shop:
    def __init__(self, path):
        self.stock = [] # Empty list (one to many relationship)

        # Assigning shop properties from csv file
        # Open csv file
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            # Read the first row
            first_row = next(csv_reader)
            # Assign value to shop cash
            self.cash = float(first_row[0])
            
            # Loop throught the csv file
            for row in csv_reader:
                # Create instances of class Product
                    # Pass the product name and price
                p = Product(row[0], float(row[1]))
                # Create instances of class ProductStock
                    # Pass the above created class Product and quantity
                ps = ProductStock(p, float(row[2]))
                # Append instances of class ProductStock to the list (create the stock list)
                self.stock.append(ps)

    # Method to update cash
    def update_cash(self, c):
        # Current cash + the customer cart total cost
        self.cash = self.cash + c.get_cartCost()
        return self.cash
    # Method to update stock
    def update_stock(self, c):
        # Loop through the shop stock
        for shop_item in self.stock:
            # Loop through the customer shopping list
            for customer_item in c.shopping_list:
                # If the product name in the shopping list matches the name in the shop stock
                if customer_item.name() == shop_item.name():
                    # Update quantity (quantity is reduced by the items bought)
                    shop_item.quantity = shop_item.quantity - customer_item.quantity
    
    def __repr__(self):
        str = ""
        str += f"/////////////////////////////////////////////////\n"
        str += f'SHOP CASH BALANCE: EUR {self.cash}\n' 
        str += f"/////////////////////////////////////////////////\n"
        str += f'STOCKLIST:\n'
        str += f"-------------------------------------------------\n"
        # Loop through the stock (list of class ProductStock)
        for i in self.stock:
            str += f"{i}\n"
        return str

# Customer class
class Customer:
    def __init__(self):
        self.shopping_list=[] # Empty list (one to many relationship)
        # Promtpt the user to enter customer (csv) file name
        self.customer_file = input("Please enter the customer file name: ")
        # Path to read the csv
        path = "../" + str(self.customer_file) + ".csv"
        # Assigning customer properties from csv file
        # Open csv file (same as in class Shop)
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            first_row = next(csv_reader)
            # Assign value to the name
            self.name = first_row[0]
            # Assign value to the budget
            self.budget = float(first_row[1])
            
            # Loop through the csv file
            for row in csv_reader:
                # Assign product name
                name = row[0]
                # Assign product qty
                quantity = float(row[1])
                # Create instance of class Product
                p = Product(name)   # Pass only the name (no price)
                # Create instance of class ProductStock
                    # Pass the above created class Product and quantity
                ps = ProductStock(p, quantity)
                # Append the classes ProductStock to the list (create a shopping list)
                self.shopping_list.append(ps)

    # Method to get budget
    def get_budget(self):
        return self.budget

    # Method to print the shopping list
        # Shopping list is the list of the products in the customer csv file
    def show_shoppingList(self):
        print(f"SHOPPING LIST:\n")
        # Loop throught the shopping list (of classes ProductStock)
        for item in self.shopping_list:
            # Access ProductStock quantity and get name using name method
            print (f"{item.quantity:.0f} x {item.name()}")
        print("-------------------------------------------------")

    # Method to create a cart (pass class shop property stock)
        # Cart is the list of the products that are on the customer list,
        # but are also available in the shop stock
    def create_cart(self, s):
        cart = [] # Empty list
        # Loop through the customer shopping list
        for item in self.shopping_list:
            # Loop through the shop stock
            for stock_item in s:
                # If the name of the product in the shopping list matches one in the shop stock
                if item.name() == stock_item.name():
                    # If the stock quantity is more then 0 (item is available)
                    if stock_item.quantity > 0:
                        # If quantity on the shopping list is higher then one on the shop stock
                        # (If customer wants more then is available in stock)
                        if item.quantity > stock_item.quantity:
                            # Update the product quantity in the shopping list
                            # to available quantity
                            item.quantity = stock_item.quantity
                            # Add product to the cart
                            cart.append(item)
                            # Assign the product price to the customer product (price unknown before)
                            item.product.price = stock_item.price()
                        # If there is enough items on the shop stock
                        else:
                            # Add item to the cart
                            cart.append(item)
                            # Assign the product price to the customer product (price unknown before)
                            item.product.price = stock_item.price()
        return cart
    
    # Method to get the cart cost
    def get_cartCost(self):
        cost = 0
        for item in self.shopping_list:
                cost += item.cost()
        return cost

    # Method to print the cart products
    def show_cart(self, cart):
        print(f'SHOPPING CART:\n')
        # Loop through the cart (list of class ProductStock)
        for item in cart:
            # Print qty, get name, price and calculate cost using defined methods
            print(f"{item.quantity:.0f} x {item.name()} (EUR {item.price():.1f}) -------- EUR {item.cost():.1f}")
        print("-------------------------------------------------")
        print("Total cost: EUR", self.get_cartCost())

    # Method to get budget
    def get_budget(self):
        return self.budget

    # Method to update budget
    def update_budget(self):
        self.budget = self.budget - self.get_cartCost()
        return self.budget

    # String represantation
    def __repr__(self):
        str = f"CUSTOMER NAME: {self.name} \nCUSTOMER BUDGET: EUR {self.budget}\n"
        str += "-------------------------------------------------\n"
        return str

# LiveCustomer class (child of Customer class)
    # Inheretance
class LiveCustomer(Customer):
    # This init method gets called first (if not defined init from class Customer would be accessed)
    def __init__(self):
        # Prompt the user to input the name
        self.name = input ("Enter your name: ")
        # Prompt the user to input budget
        self.budget = float(input("Enter your budget: EUR "))
        self.shopping_list = [] # Empty list
        print("-------------------------------------------------")
        print("Add products to your shopping list. Product names are case sensitive.")
        # Loop while True
        live = True
        while live:
            # Prompt the user to input product name
            item = input ("\nPlease enter product name: ")
            # Prompt the user to input product qty
            qty = int (input ("Please enter product quantity: "))
            # Create the instance of class Product (passing inputted product name)
            prod = Product(item)
            # Create instance of class ProductStock (passing above class product) and inputted qty
            prodS = ProductStock(prod, qty)
            # Append to the shopping list
            self.shopping_list.append(prodS)

            # Prompt the user to repeat the process
            end = input ("\nWould you like to add another item (Y/N): ")
            # If input is not Y or y, break the loop (set live to False)
            if (end != "Y") & (end != "y"):
                print("-------------------------------------------------")
                live = False         

# Method to call menu (not part of any class)
def display_menu():
    print ("/////////////////////////////////////////////////")
    print("\nMENU")
    print("====")
    print("1 - View Shop Details")
    print("2 - Load existing customers")
    print("3 - Live Shopping")
    print("0 - Exit\n")

# Main method
def main():
    print ("/////////////////////////////////////////////////")
    print ("//////////////////PARADIGM SHOP//////////////////")

    # Path for the stock (to read in the shop values)
    path = ("../stock.csv")
    # Create instance of a shop (from CSV)
    s = Shop (path)

    # Loop while true
    while True:
        display_menu()
        # Choose the menu option
        choice = input ("\nChoice:")
        
        if (choice == "1"):
            # Print shop (call repr method)
            print(s)

        elif (choice == "2"):
            # Error handling
            try:
                print ("/////////////////////////////////////////////////")
                # Create instance of a customer
                c = Customer()
                # Print customer (calls repr method)
                print(c)
                # Show customer shopping list
                    # Call method from the class Customer (of the created instance)
                c.show_shoppingList()
                print(f"\nChecking the stock...\nAdding available items to the cart...\n")
                # Create a cart
                    # Crate variable class by calling method from class Customer 
                    # (passing the stock from class Shop)
                cart = c.create_cart(s.stock)
                # Print the customer cart
                    # Calling method from the class Customer (of the created instance)
                c.show_cart(cart)
                # If the cost is higher then available customer budget
                    # Calling methods to get cart cost and the budget
                if c.get_cartCost() > c.get_budget():
                    print("-------------------------------------------------\n")
                    print(f"{c.name} doesn't have enough money for this shopping.")
                # If the cost is not higher then available customer budget
                else:
                    # Update the customer budget
                        # Call the method from class Customer (on the created instance)
                    c.update_budget()
                    print("-------------------------------------------------\n")
                    print("Processing order...\n")
                    print("-------------------------------------------------")
                    # Get the budget is now updated (after calling update_budget method)
                    print(f"{c.name} has EUR {c.get_budget():.1f} left in the wallet.")
                    # Update shop cash
                        # Call the method from class Shop (passing instance of the class Customer)
                    s.update_cash(c)
                    # Update shop stock
                        # Call the method from class Shop (passing instance of the class Customer)
                    s.update_stock(c)
                    print("-------------------------------------------------\n")
                    print(f"SHOP CASH BALANCE UPDATED TO: EUR {s.cash}")
            # Error handling
            except OSError as e:
                print("-------------------------------------------------\n")
                print ("Customer file doesn't exist. Please try again.")
        elif (choice == "3"):
            # Error handling
            try:
                print(s)
                print ("/////////////////////////////////////////////////")
                # Create and instance of a class LiveCustomer (child of class Customer) 
                # Below is same as the choice 2
                lc = LiveCustomer()
                print(lc)
                lc.show_shoppingList()
                print(f"\nChecking the stock...\nAdding available items to the cart...\n")
                lcart = lc.create_cart(s.stock)
                lc.show_cart(lcart)
                if lc.get_cartCost() > lc.get_budget():
                    print("-------------------------------------------------\n")
                    print("You don't have enough money for this shopping.")
                else:
                    lc.update_budget()
                    print("-------------------------------------------------\n")
                    print("Processing order...\n")
                    print("-------------------------------------------------")
                    print(f"You have {lc.get_budget()} left in your wallet.")
                    s.update_cash(lc)
                    s.update_stock(lc)
                    print("-------------------------------------------------\n")
                    print(f"SHOP CASH BALANCE UPDATED TO: EUR {s.cash}")
            # Error handling  
            except ValueError as ve:
                print("Wrong value entered. Please try again.")
        # Exit the menu
        elif (choice == "0"):
            break

if __name__ == "__main__":
	main()