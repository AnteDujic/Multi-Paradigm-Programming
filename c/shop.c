// Module: Multi Paradigm Programming
// Paradigm: Procedural
// Author: Ante Dujic

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <stdbool.h>
#include <ctype.h>

// Data structure for product
struct Product {
	char* name;			// Name variable
	double price;		// Price variable
};

// Data structure for product stock
struct ProductStock {
	struct Product product;		// Nested product struct 
	int quantity;				// Quantitiy variable
};

// Data structure for shop
struct Shop {
	double cash;						// Cash variable
	struct ProductStock stock[20];		// Nested product stock struct
	int index;							// Index variable for loop
};

// Data structure for customer
struct Customer {
	char* name;								// Name variable
	double budget;							// Budget variable
	struct ProductStock shoppingList[10];	// Nested product stock struct (list)
	struct ProductStock shoppingCart[10];	// Nested product stock struct (cart)
	int index;								// Index variable for loop
};

// Function declaration
	// To allow different function order in the code
void menu();
int file_exists(const char* filename);
void printProduct(struct Product p);
void printCustomer(struct Customer c);
void print_shopping_list(struct Customer c);
void create_cart(struct Customer *c, struct Shop *s);
double total_cost (struct Customer c);
void print_shopping_cart (struct Customer c);
struct Shop createAndStockShop();
void printShop(struct Shop s);
struct Customer loadCustomer();
void update_budget(struct Customer *c);
void update_cash(struct Shop *s, struct Customer *c);
void update_stock(struct Shop *s, struct Customer *c);
struct Customer liveCustomer();


// Struct to read shop values from the csv file
struct Shop createAndStockShop()
{
	// Define variables to read csv
		// REF: Lectures
    FILE * fp;
    char * line = NULL;
    size_t len = 0;
    size_t read;

	// Path
    fp = fopen("../stock.csv", "r");
    if (fp == NULL)
        exit(EXIT_FAILURE);

	read = getline(&line, &len, fp);
	// Assign the value from csv to cash
	float cash = atof(line);
	
	// Create instance of the struct Shop, with cash passed in as cash (first variable)
	struct Shop shop = { cash };

    while ((read = getline(&line, &len, fp)) != -1) {
		// Assingning the values from csv
		char *n = strtok(line, ",");
		char *p = strtok(NULL, ",");
		char *q = strtok(NULL, ",");
		
		int quantity = atoi(q); // Convert to integer
		double price = atof(p);	// Convert to double
		char *name = malloc(sizeof(char) * 50); // Allocate memory
		strcpy(name, n);	// Copy to destination

		// Create instance of Product struct, with name and price passed in
		struct Product product = { name, price };
		// Create instance of ProductStock struct
		// with Product struct from above and quantity passed in
		struct ProductStock stockItem = { product, quantity };
		// Loop throught the array and add ProductStock structs (create a stock)
		shop.stock[shop.index++] = stockItem;
    }
	
	return shop;
}

// Function to print the shop
	// Take instance of Shop Struct
void printShop(struct Shop s)
{
	printf("/////////////////////////////////////////////////\n");
	printf("SHOP CASH BALANCE: EUR %.1f\n", s.cash);
	printf("/////////////////////////////////////////////////\n");
	printf("STOCKLIST:\n");
	printf("-------------------------------------------------\n");
	for (int i = 0; i < s.index; i++)
	{
		printProduct(s.stock[i].product);
		printf("ON STOCK: %d\n", s.stock[i].quantity);
		printf("-------------------------------------------------\n");
	}
}

// Function to print the product
	// Take instance of Product struct
void printProduct(struct Product p)
{
	// Accessing Product struct name and price
	printf("PRODUCT NAME: %s \nPRODUCT PRICE: EUR %.1f\n", p.name, p.price);
}

// Function to update shop cash
	// Take instances of Shop struct and Customer struct
void update_cash(struct Shop *s, struct Customer *c)
{
	double cart_cost;
	// Assign value to the cart cost using function
	cart_cost = total_cost(*c);
	// Update shop cash, increase for the cart cost
	s->cash += cart_cost;
}

// Function to update shop stock
	// Take instances of Shop struct and Customer struct
void update_stock(struct Shop *s, struct Customer *c)
{
	// Loop through the shop stock
	for(int i = 0; i < s->index; i++)
	{
		// Loop through the customer shopping list
		for (int j = 0; j < c->index; j++)
		{
			// If product names in shopping list and on the shop stock match
			if (strcmp(c->shoppingList[j].product.name, s->stock[i].product.name)==0)
			{
				// Update shop stock qty, reduce for the bought qty
				s->stock[i].quantity -= c->shoppingList[j].quantity;
			}
		}
	}		
}

// Function to check if the file exists
// REF: https://www.learnc.net/c-tutorial/c-file-exists/
int file_exists(const char* filename){
    struct stat buffer;
    int exist = stat(filename,&buffer);
    if(exist == 0)
        return 1;
    else // -1
        return 0;
}

// Struct to read customer from csv file   
struct Customer loadCustomer()
{
	// Define variables to read csv
	// REF: Lectures
	FILE * fp;
    char *fileName = malloc(sizeof(char) * 20);  
    char * line = NULL;
    size_t len = 0;
    ssize_t read;

	// Prompt the user to enter the csv file name
	printf("Please enter the customer file name: ");
	// Take the input from the user as string
	scanf("%s", fileName);

	// Create the csv path
	strcat(fileName, ".csv");	// Concatinate
    char filepath[40] = "../";
	strcat(filepath, fileName);	// Concatinate 

	// Check if the file exists 
	int exist = file_exists(filepath);
	
	// If file exists
	if(exist)
	{
		FILE * fp;
		fp = fopen(filepath, "r");
	
		// Assingning the values from csv
		read = getline (&line, &len, fp);
		char *n = strtok(line, ",");
		char *b = strtok(NULL, ",");
		char *name = malloc(sizeof(char) * 100);

		strcpy(name, n);
		double budget = atof(b);	// Convert to double

		// Create instance of Customer struct (pass the name and budget)
		struct Customer c = {name, budget};

		while ((read = getline(&line, &len, fp)) != -1) 
			{
				// Assingning the values from csv
				char *n = strtok(line, ",");
				char *q = strtok(NULL, ",");

				int quantity = atoi(q);	// Convert to integer
				char *pname = malloc(sizeof(char) * 50); 	// Memory allocation
				strcpy(pname, n);

				// Create instance of Product struct (pass the pname)
				struct Product product = {pname};
				// Create instance of ProductStock struct
					// Pass above Product struct and qty
				struct ProductStock custItem = {product, quantity };
				// Loop throught the array and add items to index locations
				c.shoppingList[c.index++] = custItem;
    		}
		return c;
	}
	// If file doesn't exist
	else 
	{
		// Empty struct for error handling
		struct Customer c = {};
		printf("-------------------------------------------------\n");
    	printf("\nCustomer file doesn't exist. Please try again.\n");
		return c;
	}
}

// Struct for the live shopping
	// Similar to the loadCustomer but assigning values from user inputs
struct Customer liveCustomer()
{
	// Create the var and allocate memory
	char *name = malloc(sizeof(char) * 20); 
	char *b = (char*) malloc(sizeof(char) * 20);

	char *pName = (char*) malloc(sizeof(char) * 20);
	char *pq = (char*) malloc(sizeof(char) * 20); 

	// Prompt the user to enter the name
	printf("Enter your name: ");
	// Take the user input as string
	scanf("%s", name);

	// Prompt the user to enter the budget
	printf("Enter your budget: EUR ");
	// Take the user input as string
	scanf("%s", b);

	double budget = atof(b);	// Convert to double

	// Create instance of the Customer struct
		// Take above defined values
	struct Customer lc = {name, budget};

	// NOTE:Error handling
	// (If customer inputs 0 or any other character that's not positive int (returns 0))
	// If budget is not 0
	if (budget != 0)
	{
		printf("-------------------------------------------------\n");
		printf("Add products to your shopping list. Product names are case sensitive. \n\n");

		// Loop while true
			// c library imported to use boolian (<stdbool.h>)
		bool live = true;
		char end[5];
		while (live)
		{
			char *pname = malloc(sizeof(char) * 50);
			strcpy(pname, pName);
			// Prompt the user to enter product name
			printf("Please enter product name: ");
			// Take the user input as string
			scanf(" %[^\n]s", pname);	// Avoid space issues

			// Prompt the user to enter product qty
			printf("Please enter product quantity: ");
			// Take user input as a string
			scanf("%s", pq);

			int pQuantity = atoi(pq);	// Convert to integer

			// Error handling (same as for the budget)
			// If qty is not 0
			if (pQuantity != 0)
			{
				// Create instance of Product struct, take pname value
				struct Product lProduct = {pname};
				// Create intance of ProductStock struct, take Product struct and qty
				struct ProductStock cItem = {lProduct, pQuantity};
				// Adding products to the shopping list array (loop)
				lc.shoppingList[lc.index++] = cItem;

				// Prompt the user if they want to continue adding products to the list
				printf("\nWould you like to add another item (Y/N): ");
				// Take the user input as string
				scanf("%s", end);

				// If the input is Y or y stay in loop (live still True)
				if (!strcmp(end, "Y") || !strcmp(end, "y"))
    	    	    {
					printf("-------------------------------------------------\n");
    	    	    live = true;
					}
				// If the input is not Y or Y break the loop (live set to False)
				else{
					printf("-------------------------------------------------\n");
					live = false;
				}
			}
			// Error handling
			else
			{
				printf("Wrong value entered. Please try again.\n");
				live = false;
			}
		}
		
	}
	// Error handling
	else
	{
		printf("Wrong value entered. Please try again.\n");
	}
	return lc;
}

// Function to print the customer
	// Take instance of Customer struct
void printCustomer(struct Customer c)
{
	// Access the Customer struct name and budget
	printf("CUSTOMER NAME: %s \nCUSTOMER BUDGET: EUR %.1f\n", c.name, c.budget);
	printf("-------------------------------------------------\n");
}

// Function to print the shopping list
	// Take instance of Customer struct
void print_shopping_list(struct Customer c)
{
	printf("\nSHOPPING LIST:\n\n");
	// Loop throught the shopping list (ProductStock struct)
		// Customer struct index var used for loop
	for(int i = 0; i < c.index; i++)
	{
		// Accessing shopping list quantity and name
			// Customer struct -> ProductStock struct within -> quantity/name
		printf("%d x %s\n", c.shoppingList[i].quantity, c.shoppingList[i].product.name);
	}
	printf("-------------------------------------------------\n");
}

// Funtion to create a cart
	// Take instance of Customer struct and Shop struct
void create_cart(struct Customer *c, struct Shop *s)
{
	// Loop through the customer shopping list (ProductStock struct)
	for(int i = 0; i < c->index; i++)
	{
		// Loop through the shop stock (ProductStock struct)
		for (int j = 0; j < s->index; j++)
		{
			// If the product name in the shopping list matches the product name in the shop stock 
			if (strcmp(c->shoppingList[i].product.name, s->stock[j].product.name)==0)
			{
				// If the shopping list product qty is higher then one in the shop stock
					// If there is less stock available then the customer wants to buy
				if (c->shoppingList[i].quantity > s->stock[j].quantity)
				{
					// Update the shopping list product qty to be the same as the one on the stock
					c->shoppingList[i].quantity = s->stock[j].quantity;
					// Assign the price to the shopping list product (unknown before)
					c->shoppingList[i].product.price = s->stock[j].product.price;
				}
				// If the needed qty on stock is available
				else
				{
					// Assign the price to the shopping list product (unknown before)
					c->shoppingList[i].product.price = s->stock[j].product.price;
				}
				// Set Cart to be same as newly updated shopping list
					// Created because different methods are called to print the shopping list and the cart
				c->shoppingCart[i] = c->shoppingList[i];
			}
		}
	}
}

// Function to calculate the total cost
	// Take instance of Customer struct
double total_cost (struct Customer c)
{
	// Initial cost is 0
	double cost = 0.0;
	// Loop through the shopping list
	for(int i = 0; i < c.index; i++)
	{
		// Calculate the cost
		cost += (c.shoppingList[i].product.price) * (c.shoppingList[i].quantity);
	}
	return cost;
}

// Function to print the shopping cart and get the total cost
	// Take instance of the Customer struct
void print_shopping_cart (struct Customer c)
{
	// Initial cost set to 0
	double cost = 0.0;
	printf("\nSHOPPING CART:\n\n");
	// Loop through the cart
	for(int i = 0; i < c.index; i++)
	{
		// If the quantity is higer then 0
			// To avoid printing products which qty gets set to 0
			// due to product being unavailable in shop stock
		if (c.shoppingCart[i].quantity > 0)
		{
		// Calculate the cost
		cost = (c.shoppingCart[i].product.price) * (c.shoppingCart[i].quantity);
		// Access qty, name, price and the above cost
			// Customer Struct -> ProductStock struct (qty)-> Product struct (name, price)
		printf("%d x %s (EUR %.1f) -------- EUR %.1f\n", c.shoppingCart[i].quantity, c.shoppingCart[i].product.name, c.shoppingCart[i].product.price, cost);
		}
	}
	printf("-------------------------------------------------\n");
}

// Function to update customer budget
	// Take instance of Customer struct
void update_budget(struct Customer *c)
{
	double cart_cost;
	// Assign cart_cost value using method
	cart_cost = total_cost(*c);
	// Update budget, decrease for the cart cost
	c->budget -= cart_cost;
}

// Menu
void menu(void)
{
	// Create instance of the Shop struct using function
	struct Shop shop = createAndStockShop();
	// Creating variables
	double totalCost;
	double liveCost;
    int choice = -1;
	
	// Loop through the menu
    while (choice !=0)
	{
		fflush(stdin);	// Error handling (+avoid endless loop)
		printf("/////////////////////////////////////////////////\n");
    	printf("\nMENU\n");
    	printf("====\n");
    	printf("1 - View Shop Details\n");
    	printf("2 - Load existing customers\n");
    	printf("3 - Live Shopping\n");
    	printf("0 - Exit\n\n");
		
		// Prompt the user for the menu choice
		printf("\nChoice:");
		// Take user input
        scanf("%d",&choice);
 
        if (choice == 1)
        {
			// Call the function
				// Pass instance of the Shop struct
            printShop(shop);
        }
		else if (choice == 2)
		{
			
			printf ("/////////////////////////////////////////////////\n");
			// Create instance of the Customer struct (from csv file)
			struct Customer c = loadCustomer();
			// Error handling
			if ((c.budget != 0))
			{
				// Call the function to print customer
					// Pass the instance of Customer struct
				printCustomer(c);
				// Call the function to print shopping list
					// Pass the instance of Customer struct
				print_shopping_list(c);
				printf("\nChecking the stock...\nAdding available items to the cart...\n");
				// Call the function to create shopping cart
					// Pass the instance of Customer struct and Shop struct
				create_cart(&c, &shop);
				// Call the function to print the shopping cart
					// Pass the instance of Customer struct
				print_shopping_cart(c);
				// Assign the value to the totalCost using function
				totalCost = total_cost(c);
				printf("Total cost: EUR %.1f\n", totalCost);
				printf("-------------------------------------------------\n");

				// If the total cost is higher then customer budget
					// (customer doesn't have enough money)
				if (totalCost > c.budget)
				{
            	    printf("\n%s doesn't have enough money for this shopping.\n", c.name);
				}
				// If customer has enough money
				else
				{
					// Call the function to update customer budget
					// Pass the instance of Customer struct
					update_budget(&c);
            	    printf("\nProcessing order...\n\n");
            	    printf("-------------------------------------------------\n");
					printf("%s has EUR %.1f left in the wallet.\n", c.name, c.budget);
					// Call the function to update cash
					// Pass the instances of Customer struct and Shop struct
					update_cash(&shop, &c);
					// Call the function to update stock
					// Pass the instances of Customer struct and Shop struct
					update_stock(&shop, &c);
					printf("-------------------------------------------------\n");
            	    printf("\nSHOP CASH BALANCE UPDATED TO: EUR %.1f\n", shop.cash); // Access shop cash
				}
			}

		}
		else if (choice == 3)
		{
			printShop(shop);
			printf("/////////////////////////////////////////////////\n");
			// Create instance of Customer struct (from user inputs)
			struct Customer lc = liveCustomer();
			// Error handling
			if ((lc.budget != 0) && (lc.shoppingList->quantity != 0))
			{
				// Below code follows the same logic as in option 2
				printCustomer(lc);
				print_shopping_list(lc);
				printf("\nChecking the stock...\nAdding available items to the cart...\n");
				create_cart(&lc, &shop);
				print_shopping_cart(lc);
				liveCost = total_cost(lc);
				printf("Total cost: EUR %.1f\n", liveCost);
				printf("-------------------------------------------------\n");

				if (totalCost > lc.budget)
				{
            	    printf("You don't have enough money for this shopping.\n");
				}
				else
				{
					update_budget(&lc);
            	    printf("\nProcessing order...\n\n");
            	    printf("-------------------------------------------------\n");
					printf("You have %.1f left in your wallet.\n", lc.budget);
					update_cash(&shop, &lc);
					update_stock(&shop, &lc);
					printf("-------------------------------------------------\n");
            	    printf("\nSHOP CASH BALANCE UPDATED TO: EUR %.1f\n", shop.cash);
				}
			}
		}
    } 
 
}

// Main function
int main(void) 
{
    printf("/////////////////////////////////////////////////\n");
    printf("//////////////////PARADIGM SHOP//////////////////\n");
	
	menu();
    return 0;
}
