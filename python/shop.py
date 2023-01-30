# Module: Multi Paradigm Programming
# Paradigm: Procedural
# Author: Ante Dujic

import csv

# Method to create the shop and assign the values
def create_and_stock_shop(path):
    # Empty dict
    shop = {}

    # Open csv file
    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        first_row = next(csv_reader)
        # Define the shop cash in dict
        shop["cash"] = float(first_row[0])
        # Define the shop stock - Empty list (product dicts to be appended)
        shop["products"] = []
        # Loop through the csv file
        for row in csv_reader:
            product = {} # Empty dict
            
            # Define the product name in dict
            product["name"] = row[0]
            # Define the product price in dict
            product["price"] = float(row[1])
            # Define the product qty in dict
            product["quantity"] = float(row[2])

            # Add the dicts to the list - create the stock
            shop["products"].append(product)

    return shop

# Method to print the shop
# Passing shop dict
def print_shop(s):
    str = ""
    str += f"/////////////////////////////////////////////////\n"
    str += f'SHOP CASH BALANCE: EUR {s["cash"]}\n' 
    str += f"/////////////////////////////////////////////////\n"
    str += f'STOCKLIST:\n'
    str += f"-------------------------------------------------"
    print(str)
    # Loop through the product list and print each product using method
    for i in s["products"]:
        print_product(i)

# Method to print the product (accessing dict values)
# Passing product dict
def print_product(p):
    print(f'PRODUCT NAME: {p["name"]} \nPRODUCT PRICE: EUR {p["price"]}')
    print(f'ON STOCK: {p["quantity"]:.0f}\n-------------------------------------------------')

# Method to update shop cash
# Passing cart list and shop dict
def update_cash(cart, s):
    # Shop cash increases for the customer cart cost
    s["cash"] = s["cash"] + get_cartCost(cart)
    return s["cash"]

# Method to update shop stock
# Passing the shop dict and cart list
def update_stock(s, cart):
    # Loop through the shop stock
    for shop_item in s["products"]:
        # Loop through the cart
        for customer_item in cart:
            # If product name in the cart matches one in the shop stock
            if customer_item["name"] == shop_item["name"]:
                # Update qty (Reduce qty for the items bought)
                shop_item["quantity"] = shop_item["quantity"] - customer_item["quantity"]

# Method to read in the customer file and assign the values
# Same approach as creating a shop
def read_customer(file_name):
    # Empty dict
    customer = {}

    # Open csv file
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        first_row = next(csv_reader)

        # Define the customer name in dict
        customer["name"] = first_row[0]
        # Define customer budget in dict
        customer["budget"] = float(first_row[1])
        # Define the customer shopping list - Empty list (product dicts to be appended)
        customer["products"] = []
        
        # Loop through the csv file
        for row in csv_reader:
            product = {} # Empty dict

            # Define the product name in dict
            product["name"] = row[0]
            # Define the product qty in fict
            product["quantity"] = float(row[1])

            # Add the dicts to the list - create the shopping list 
            customer["products"].append(product)

    return customer

# Method for the live shopping
def live_customer():
    # Empty dict
    customer = {}
    # Prompt the user to input the name
    # Define customer name (dict key)
    customer["name"] = input ("Enter your name: ")
    # Prompt the user to input the budget
    # Define customer budget
    customer["budget"] = float(input("Enter your budget: EUR "))
    # Empty list
    customer["products"] = []

    print("-------------------------------------------------")
    print("Add products to your shopping list. Product names are case sensitive.")

    # Loop while true
    live = True
    while live:
        # Empty dict
        product = {}
        # Prompt the user to input product name
        item = input ("\nPlease enter product name: ")
        # Prompt the user to input product qty
        qty = float (input ("Please enter product quantity: "))
        # Assign the value to the product name (dict key)
        product["name"] = item
        # Assign the value to the product qty (dict key)
        product["quantity"] = qty
        # Add the product (dict) to the shopping list
        customer["products"].append(product)
        
        # Prompt the user if they want to add more items to the list
        end = input ("\nWould you like to add another item (Y/N): ")
        # If the input is not Y or y then break the loop (set live to false)
        if (end != "Y") & (end != "y"):
            print("-------------------------------------------------")
            live = False
    return customer

# Method to print the customer
# Passing customer dict
def print_customer(c):
    str = f'CUSTOMER NAME: {c["name"]} \nCUSTOMER BUDGET: EUR {c["budget"]}\n'
    str += "-------------------------------------------------\n"
    print(str)

# Method to print the shopping list
# Passing customer dict
def print_shopping_list(c):
    print(f'SHOPPING LIST:\n')
    for item in c["products"]:
        print ((f'{item["quantity"]:.0f} x {item["name"]}'))
    print("-------------------------------------------------")

# Method to create a cart
# Pass in the customer and shop dicts
def create_cart(c, s):
    cart = [] # Empty list

    # Loop through the customer shopping list
    for item in c["products"]:
        # Loop through the shop stock
        for stock_item in s["products"]:
            # If the product name in the shopping list matches the product name on the shop stock 
            if item["name"] == stock_item["name"]:
                # If the product qty on the stock is higher then 0
                # (If the item is available)
                if stock_item["quantity"] > 0:
                    # If the product qty on the shopping list is higher then product qty on the shop stock
                    # (If customer wants more then available on stock)
                    if item["quantity"] > stock_item["quantity"]:
                        # The customer product qty updated to be the same as the stock qty
                        # (Customer list is updated to available stock)
                        item["quantity"] = stock_item["quantity"]
                        # Add the available product the cart
                        cart.append(item)
                        # Get the product price
                        item["price"] = stock_item["price"]
                    # If there is enough stock in the shop
                    else:
                        # Add the product to the shopping cart
                        cart.append(item)
                        # Get the product price
                        item["price"] = stock_item["price"]
    return cart

# Method to calculate the cart cost
# Passing the cart
def get_cartCost(cart):
    # Initial cost is 0
    cost = 0
    # Loop through the cart
    for item in cart:
            # Add each item cost to total cost
            cost += item["quantity"]*item["price"]
    return cost

# Method to print shopping cart
# Passing customer and the cart 
def print_shopping_cart(c, cart):
    print(f'SHOPPING CART:\n')
    # Loop through the cart and print each product
    for item in cart:
        item_cost = item["quantity"]*item["price"]
        print ((f'{item["quantity"]:.0f} x {item["name"]} (EUR {item["price"]}) -------- EUR {item_cost:.1f}'))
    print("-------------------------------------------------")
    # Print the total cost (get cost using method)
    print("Total cost: EUR", get_cartCost(cart))

# Method to update customer budget after shopping
# Passing customer dict and the cart list
def update_budget(c, cart):
    # Decrease the budget for the cart cost
    c["budget"] = c["budget"] - get_cartCost(cart)
    return c["budget"]

# Method to display menu
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
    
    # Create a path for the csv file to be read
    path = ("../stock.csv")
    # Create the shop
    shop = create_and_stock_shop(path)
    
    # Loop the menu
    while True:
        display_menu()
        choice = input ("\nChoice:")

        if (choice == "1"):
            # Call the method to print the shop
            print_shop(shop)

        elif (choice == "2"):
            # Error handling
            try:
                print ("/////////////////////////////////////////////////")
                # Prompt the user to input csv file name
                customer_name = input("Please enter the customer file name: ")
                # Create the path to the csv file
                customer_file = "../" + str(customer_name) + ".csv"
                # Create a customer
                c = read_customer(customer_file)
                # Call the method to print the customer
                print_customer(c)
                # Call the method to print the shopping list
                print_shopping_list(c)
                # Create the cart - call the method to create the cart
                cart = create_cart(c, shop)
                print(f"\nChecking the stock...\nAdding available items to the cart...\n")
                # Call the method to print the shopping cart
                print_shopping_cart(c, cart)
                # If the cost is higher then available customer budget
                    # Calling method to get cart cost and access the customer dict key budget
                if get_cartCost(cart) > c["budget"]:
                    print("-------------------------------------------------\n")
                    print(f'{c["name"]} doesn\'t have enough money for this shopping.')
                # If the cost is not higher then available customer budget
                else:
                    # Call the method to update the budget
                    update_budget(c, cart)
                    print("-------------------------------------------------\n")
                    print("Processing order...\n")
                    print("-------------------------------------------------")
                    print(f'{c["name"]} has EUR {c["budget"]:.1f} left in the wallet.')
                    # Call the method to update cash
                    update_cash(cart, shop)
                    # Call the method to update stock
                    update_stock(shop, cart)
                    print("-------------------------------------------------\n")
                    print(f'SHOP CASH BALANCE UPDATED TO: EUR {shop["cash"]}')
            # Error handling
            except OSError as e:
                print("-------------------------------------------------\n")
                print ("Customer file doesn't exist. Please try again.")

        elif (choice == "3"):
            # Error handling
            try:
                print_shop(shop)
                print ("/////////////////////////////////////////////////")
                # Create the customer by calling the method live_customer
                lc = live_customer()
                # Below is same as the choice 2 
                print_customer(lc)
                print_shopping_list(lc)
                live_cart = create_cart(lc, shop)
                print(f"\nChecking the stock...\nAdding available items to the cart...\n")
                print_shopping_cart(lc, live_cart)
                if get_cartCost(live_cart) > lc["budget"]:
                    print("You don't have enough money for this shopping.")
                else:
                    update_budget(lc, live_cart)
                    print("-------------------------------------------------\n")
                    print("Processing order...\n")
                    print("-------------------------------------------------")
                    print(f'You have {lc["budget"]} left in your wallet.')
                    update_cash(live_cart, shop)
                    update_stock(shop, live_cart)
                    print("-------------------------------------------------\n")
                    print(f'SHOP CASH BALANCE UPDATED TO: EUR {shop["cash"]}')
            # Error handling
            except ValueError as ve:
                print("Wrong value entered. Please try again.")
        # Exit the menu
        elif (choice == "0"):
            break

if __name__ == "__main__":
	main()