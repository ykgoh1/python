


import json
from datetime import datetime

# File paths
CUSTOMER_FILE = "customer_data.json"
CONSIGNMENT_FILE = "consignment_data.json"
# File path for storing user data
FILE_PATH = "store.json"


# save data to file
def load_data_from_json(filename):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        return None


# Load parcel prices from parcel_prices.json
ParcelPrice = load_data_from_json("parcel_prices.json")
if ParcelPrice is None:
    ParcelPrice = {
        "UNDER 1KG": {
            "Zone A": 8.00,
            "Zone B": 9.00,
            "Zone C": 10.00,
            "Zone D": 11.00,
            "Zone E": 12.00,
        },
        "1KG TO 3KG": {
            "Zone A": 16.00,
            "Zone B": 18.00,
            "Zone C": 20.00,
            "Zone D": 22.00,
            "Zone E": 24.00,
        },
    }

# Creating an empty dictionary to store user data
user_data = {}


# Function to initialize user_data from the file
def initialize_user_data():
    try:
        with open(FILE_PATH, "r") as file:
            user_data.update(json.load(file))
    except FileNotFoundError:
        pass  # Ignore if the file doesn't exist initially


# Function to show user data
def show_user_data():
    for username, data in user_data.items():
        print(f"Username: {username}, Data: {data}")


# Function to save user_data to the file
def save_user_data():
    with open(FILE_PATH, "w") as file:
        json.dump(user_data, file, indent=4)


# Function to ask the user to register or login
def ask_user():
    while True:
        initialize_user_data()
        ask = input("You are login user or register user? If register user enter '1' ,login user enter '2': ") # Ask user to register or login

        if ask.lower() == '1': # IF user register
            register_user()
        elif ask.lower() == '2': # ELIF user login
            login_user()
            save_user_data()  # Save the data before exiting
            break
        else: # OUTPUT "Invalid choice. Please enter '1' or '2'."
            print("Invalid choice. Please enter '1' or '2'.")


# Function to register a new user
# INPUT username, full name, email, password, user type, gender
def register_user():
    while True:
        username = input("Enter username: ")
        if not username:
            print("Username cannot be empty. Please enter a username.")
            continue

        name = input("Enter your full name:")
        if not name:
            print("Full name cannot be empty. Please enter your full name.")
            continue

        gmail = input("Enter gmail:")
        if not gmail:
            print("Gmail cannot be empty. Please enter a gmail.")
            continue

        password = input("Enter password.")
        if not password:
            print("Password cannot be empty. Please enter a password.")
            continue
        break
    while True:
        user_ty = input("Enter your user type (administrator or operator): ").lower()
        if user_ty in ['administrator', 'operator']:
            user_type = user_ty
            break
        else:
            print("Invalid user type. Please enter 'administrator' or 'operator'.")

    while True:
        user_gender = input("Enter gender (girl/boy): ").lower()
        if user_gender in ['girl', 'boy']:
            gender = user_gender
            break
        else:
            print("Invalid input. Please enter 'girl' or 'boy'.")

    user_data[username] = {'password': password, 'user_type': user_type, 'name': name, 'gmail': gmail, 'gender': gender}
    save_user_data()  # Save the data after registration
    print("User registered successfully.") # OUTPUT "User registered successfully"


# Function to validate user login
def login_user():
    while True: # INPUT username, password
        username = input("Enter Username: ")
        password = input("Enter Password: ")

        if username in user_data and user_data[username]['password'] == password:
            print("User successfully logged in.")
            if user_data[username]['user_type'] == "administrator": # IF username and password match AND user type is “Administrator”
                management_user()
            elif user_data[username]['user_type'] == "operator": # ELIF username and password match AND user type is “Operator”
                operatorMenu()
                # Save any changes made by user into customer_data.json and consignment_data.json
                with open(CUSTOMER_FILE, "w") as file:
                    json.dump(customer_database, file, indent=4)
                with open(CONSIGNMENT_FILE, "w") as file:
                    json.dump(consignment_details_dict, file, indent=4)
            else:
                print("Unknown user type.")
            break
        else: # OUTPUT "Incorrect username or password. Please try again."
            print("Incorrect username or password. Please try again.")


# Parcel price management menu
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. View Parcel Price List")
        print("2. Add or Modify Parcel Price")
        print("3. Check Parcel Price")
        print("4. Delete Parcel Price")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1": # IF Administrator view parcel price list
            show_list(ParcelPrice)

        elif choice == "2": # ELIF Administrator add or modify parcel price
            while True: # INPUT weight
                weight_input = input("Enter the weight (in kg): ")
                if weight_input.isdigit() and int(weight_input) > 3:
                    weight = int(weight_input)
                    while True:
                        try:
                            price = float(input("Enter the price: ")) # INPUT price
                            break
                        except ValueError:
                            print("Invalid input. Please try again.")

                    while True:
                        zone = input("Enter the zone (Ex. Zone A): ") # INPUT zone
                        if zone in ("Zone A", "Zone B", "Zone C", "Zone D", "Zone E"):
                            break
                        else:
                            print("Invalid zone. Please try again.")

                    add_parcel_type_function(weight, price, zone, ParcelPrice)
                    show_list(ParcelPrice)
                    save_data_to_json(ParcelPrice, "parcel_prices.json")
                    break
                else:
                    print("Invalid input. Please try again.")

        elif choice == "3": # ELIF Administrator check parcel price
            checkPrice(ParcelPrice)

        elif choice == "4": # ELIF Administrator delete parcel price
            while True:
                weight_input = input("Enter the weight (in kg) to delete price: ") # INPUT weight
                if weight_input.isdigit() and int(weight_input) > 3:
                    weight = int(weight_input)
                    break
                else:
                    print("Invalid input. Please try again.")

            while True:
                zone = input("Enter the zone (Ex. Zone A) to delete price: ") # INPUT zone
                if zone in ("Zone A", "Zone B", "Zone C", "Zone D", "Zone E"):
                    break
                else:
                    print("Invalid zone. Please try again.")

            delete_parcel_price(weight, zone, ParcelPrice)
            show_list(ParcelPrice)

        elif choice == "5": # ELIF Administrator exits
            print("Back to User Management.")
            break  # Exit the loop to end the program

        else: # OUTPUT "Invalid choice. Please enter a number from 1 to 5."
            print("Invalid choice. Please enter a number from 1 to 5.")

    save_data_to_json(ParcelPrice, "parcel_prices.json")


# show list function
def show_list(parcel_price):
    print("Destinations".ljust(12), end="\t")
    for zone in parcel_price[list(parcel_price.keys())[0]]:
        print(zone.ljust(7), end="\t")
    print()

    for parcel_type, prices in parcel_price.items():
        print(parcel_type.ljust(12), end="\t")
        price_list = ["{:.2f}".format(price).ljust(7) for price in prices.values()]
        print("\t".join(price_list))


# add or modify parcel price function
def add_parcel_type_function(weight, price, zone, parcel_price):
    weight_str = f"{weight}KG"

    if weight_str not in parcel_price:
        # Initialize all zones to 0.00 for a new weight category
        parcel_price[weight_str] = {zone: 0.00 for zone in parcel_price[list(parcel_price.keys())[0]]}

    # Update the price for the specified zone
    parcel_price[weight_str][zone] = price

    # Check if all prices for this weight category are 0.00, then delete the weight category
    if all(value == 0.00 for value in parcel_price[weight_str].values()):
        del parcel_price[weight_str]
        print(f"All prices for {weight}KG were 0.00. Weight category removed.")


# check parcel price function
def checkPrice(ParcelPrice):
    while True:
        weight_input = input("Enter the weight of the parcel (kg): ")
        try:
            weight = float(weight_input)
            if weight > 0:
                break
            else:
                print("Weight must be greater than 0. Please try again.")
        except ValueError:
            print("Invalid weight. Please try again.")

    while True:
        zone = input("Enter the destination (Ex. Zone A): ")
        if zone in ("Zone A", "Zone B", "Zone C", "Zone D", "Zone E"):
            break
        else:
            print("Invalid zone. Please try again.")

    if weight < 1:
        if zone == "Zone A":
            print(f"The price for a {weight}KG parcel delivering to {zone} is RM8.00")
        if zone == "Zone B":
            print(f"The price for a {weight}KG parcel delivering to {zone} is RM9.00")
        if zone == "Zone C":
            print(f"The price for a {weight}KG parcel delivering to {zone} is RM10.00")
        if zone == "Zone D":
            print(f"The price for a {weight}KG parcel delivering to {zone} is RM11.00")
        if zone == "Zone E":
            print(f"The price for a {weight}KG parcel delivering to {zone} is RM12.00")
    elif 1 <= weight <= 3:
        if zone == "Zone A":
            print(f"The price for a {weight}KG parcel delivering to {zone} is RM16.00")
        if zone == "Zone B":
            print(f"The price for a {weight}KG parcel delivering to {zone} is RM18.00")
        if zone == "Zone C":
            print(f"The price for a {weight}KG parcel delivering to {zone} is RM20.00")
        if zone == "Zone D":
            print(f"The price for a {weight}KG parcel delivering to {zone} is RM22.00")
        if zone == "Zone E":
            print(f"The price for a {weight}KG parcel delivering to {zone} is RM24.00")
    else:
        weight = int(weight)
        weight = str(weight) + "KG"
        for weight_category, prices in ParcelPrice.items():
            if weight_category.startswith(weight):
                print(f"{weight_category}:")
                for zone_input, price in prices.items():
                    if zone_input == zone:
                        if price == 0.00:
                            print(f"No price found for {weight} parcel in {zone}.")
                            return
                        else:
                            print(f"The price for a {weight} parcel delivering to {zone_input} is RM{price:.2f}")
                            return  # Return to exit the function
        else:
            print(f"No price found for {weight} parcel in {zone}.")


# delete parcel price function
def delete_parcel_price(weight, zone, parcel_price):
    weight_str = f"{weight}KG"
    print("Weight to search:", weight_str)
    if weight_str in parcel_price:
        print("Weight found:", weight_str)
        if zone in parcel_price[weight_str]:
            parcel_price[weight_str][zone] = 0.00
            print(f"Price for {weight}KG in {zone} deleted.")

            # Check if all zones have 0.00 prices for this weight
            all_zero_prices = True
            for price_data in parcel_price[weight_str].values():
                if price_data != 0.00:
                    all_zero_prices = False
                    break

            if all_zero_prices:
                del parcel_price[weight_str]
        else:
            print(f"No price found for {zone} in {weight}KG.")
    else:
        print(f"No price found for {weight}KG.")

    save_data_to_json(parcel_price, "parcel_prices.json")


def management_user():
    while True:
        print("\nManagement Options:") # Display user management menu
        print("1. Add User")
        print("2. Remove User")
        print("3. Edit User")
        print("4. Find User")
        print("5. View User")
        print("6. Parcel Price Management")
        print("7. Exit Management")

        choice = input("Enter your choice (1-6): ")

        if choice == '1': # IF Administrator choose 1 “Add User”
            register_user()
        elif choice == '2': # ELIF Administrator choose 2 “Remove user”
            remove_user()
        elif choice == '3': # ELIF Administrator choose 3 “Edit user”
            edit_user()
        elif choice == '4': # ELIF Administrator choose 4 “Find user”
            find_user()
        elif choice == '5': # ELIF Administrator choose 5 “View user”
            view_user()
        elif choice == '6': # ELIF Administrator choose 6 “Parcel Price Management”
            main_menu()
        elif choice == '7': # ELIF Administrator choose 7 “Exit Management”
            print("Exiting the program.") # OUTPUT "Exiting the program."
            break
        else: # OUTPUT “Invalid choice. Please enter a number between 1 and 6.”
            print("Invalid choice. Please enter a number between 1 and 6.")


# Function to remove a user
def remove_user():
    username_remove = input("Enter Username: ")

    global user_data  # Declare user_data as global to modify the global variable

    if username_remove in user_data:
        del user_data[username_remove]
        save_user_data()  # Save the data after removing the user
        print(f"User {username_remove} successfully removed.")
    else:
        print(f"User with username {username_remove} not found.")


# Function to edit user details
def edit_user():
    username_to_edit = input("Enter the username to edit: ")

    if username_to_edit in user_data:
        while True:
            print("\nEdit Options:")
            print("1. Change Password")
            print("2. Change Name")
            print("3. Change Gmail")
            print("4. Change Gender")
            print("5. Finish Editing")

            edit_choice = input("Enter your edit choice (1-5): ")

            if edit_choice == '1':
                user_data[username_to_edit]['password'] = input("Enter the new password: ")
                save_user_data()
            elif edit_choice == '2':
                user_data[username_to_edit]['name'] = input("Enter the new name: ")
                save_user_data()
            elif edit_choice == '3':
                user_data[username_to_edit]['gmail'] = input("Enter the new gmail: ")
                save_user_data()
            elif edit_choice == '4':
                while True:
                    new_gender = input("Enter the new gender (girl/boy): ").lower()
                    if new_gender in ['girl', 'boy']:
                        user_data[username_to_edit]['gender'] = new_gender
                        save_user_data()
                        break
                    else:
                        print("Invalid input. Please enter 'girl' or 'boy'.")
            elif edit_choice == '5':
                print(f"Editing for user {username_to_edit} finished.")
                save_user_data()
                break
            else:
                print("Invalid edit choice. Please enter a number between 1 and 5.")
    else:
        print(f"User with username {username_to_edit} not found.")


# Function to find user details
def find_user():
    username_to_find = input("Enter the username to find: ")

    if username_to_find in user_data:
        print(f"User Details for {username_to_find}: {user_data[username_to_find]}")
    else:
        print(f"User with username {username_to_find} not found.")


# Function to view a list of users
def view_user():
    show_user_data()


# Function to save data to the file
def savefile(file_path, data):
    with open(file_path, "w") as file:
        json.dump(user_data, file, indent=4)


def save_data_to_json(data, filename):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


# Read and load file from the file path
def load_data_from_file(file_path):
    try:
        with open(file_path, "r") as input_file:
            return json.load(input_file)
    except FileNotFoundError:
        return {}


# Save and overwrite the data into the JSON file
def save_data_to_file(data, file_path):
    with open(file_path, "w") as output_file:
        json.dump(data, output_file, indent=4)


# Read the last used parcel number to prevent overlapping
def load_last_parcel_number():
    try:
        with open("last_parcel_number.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 1000000  # Or any other suitable starting value
    except ValueError:
        print("Error loading last parcel number. Using default value.")
        return 1000000  # Or any other suitable starting value


# Read the last used customer ID to prevent overlapping
def load_last_customer_ID():
    try:
        with open("last_customer_ID.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 1
    except ValueError:
        print("Error loading last customer ID. Using default value.")
        return 1


# Parcel number and customer ID is declared into their corresponding variables
last_parcel_number = load_last_parcel_number()
last_customer_ID = load_last_customer_ID()

# Read and load the customer list from customer_data.json
try:
    with open(CUSTOMER_FILE, "r") as file:
        customer_database = json.load(file)
except FileNotFoundError:
    customer_database = {}
except json.JSONDecodeError:
    customer_database = {}

# Read and load the consignment list from consignment_data.json
try:
    with open(CONSIGNMENT_FILE, "r") as file:
        consignment_details_dict = json.load(file)
except FileNotFoundError:
    consignment_details_dict = {}
except json.JSONDecodeError:
    consignment_details_dict = []


# Will clear and reset the consignment list when called
def clear_consignment_file():
    consignment_details_dict.clear()

    # Reset last_parcel_number to a specific starting value
    new_last_parcel_number = 1000000  # or any other suitable starting value

    # Save the updated last_parcel_number to the file
    with open("last_parcel_number.txt", "w") as f:
        f.write(str(new_last_parcel_number))

    # Save the updated consignment_details_dict to the file
    save_data_to_file(consignment_details_dict, CONSIGNMENT_FILE)
    return consignment_details_dict


# Will clear and reset the customer list when called
def clear_customer_file():
    customer_database.clear()

    # Reset last_customer_ID to 1
    new_last_customer_ID = 0

    # Save the updated last_customer_ID to the file
    with open("last_customer_ID.txt", "w") as f:
        f.write(str(new_last_customer_ID))

    save_data_to_file(customer_database, CUSTOMER_FILE)
    return customer_database, new_last_customer_ID


# Save and overwrite data into both customer_data.json and consignment_data.json
def save_all_data():
    save_data_to_file(customer_database, CUSTOMER_FILE)
    save_data_to_file(consignment_details_dict, CONSIGNMENT_FILE)
    print("All data saved successfully.")

# Updates the price based on the weight and delivery zone using predefined prices.
def update_price(weight, zone, prices):
    weight_str = str(weight) + "KG"

    if weight < 1:
        weight_category = "UNDER 1KG"
    elif 1 <= weight <= 3:
        weight_category = "1KG TO 3KG"
    else:
        weight_category = weight_str

    if weight_category in prices:
        if zone in prices[weight_category]:
            price = prices[weight_category][zone]
            if price == 0.00:
                print(f"No price found for {weight_str} parcel in {zone}.")
                return None
            else:
                print(f"The price for a {weight_str} parcel delivering to {zone} is RM{price:.2f}")
                return price
        else:
            print(f"No price found for {weight_str} parcel in {zone}.")
            return None
    else:
        print(f"No price found for {weight_str} parcel in {zone}.")

    return None

# Calculates the total price for a list of items based on their weights and zones.
def calculate_total_price(items, prices):
    return sum(
        [
            update_price(current_item["Weight"], current_item["Zone"], prices) or 0
            for current_item in items
        ]
    )

# Accept input from user to add customer into customer_data.json
def addCustomerDetails():
    addCustomer = "y"
    next_customer_ID = last_customer_ID + 1

    while addCustomer.lower() == "y":
        customerName = input("Enter customer name:")
        if all(x.isalpha() or x.isspace() for x in customerName):
            customerAddress = input("Enter customer address:")
            customerNumbers = input("Enter customer telephone number (without spaces or -):")

            if customerNumbers.isnumeric():
                customer_database[next_customer_ID] = {"name": customerName, "address": customerAddress,
                                                       "phone": customerNumbers}
                next_customer_ID += 1
            else:
                print("Invalid Telephone Numbers.")
        else:
            print("Invalid Name.")

        addCustomer = input("Would you like to continue? [y/n]:")

    with open("last_customer_ID.txt", "w") as f:
        f.write(str(next_customer_ID - 1))  # Record the last used customer ID into last_customer_ID.txt

    save_all_data()
    return next_customer_ID, last_customer_ID


# Search and overwrite details of desired customer
def modifyCustomerAddressTelephone():
    customerID = int(input("Enter the Customer ID to modify details: "))
    if str(customerID) in customer_database:
        newAddress = input("Enter new address: ")
        newTelephone = input("Enter new telephone number: ")
        customer_database[str(customerID)]['address'] = newAddress
        customer_database[str(customerID)]['phone'] = newTelephone
        print(f"Customer ID {customerID} details updated successfully.")
        save_all_data()
    else:
        print(f"Customer ID {customerID} not found.")


# Display contents of customer_data.json
def viewCustomerList():
    for key, data in customer_database.items():
        print(f"ID: {key}")
        print(f"Name: {data.get('name', 'N/A')}")
        print(f"Address: {data.get('address', 'N/A')}")
        print(f"Phone: {data.get('phone', 'N/A')}")
        print()


def generateParcelList():
    date = input("Enter the date (DD/MM/YYYY): ")
    zone = input("Enter the destination zone (eg. 'Zone A'): ")

    parcelResult = []

    for order_id, order_data in consignment_details_dict.items():
        delivery_date = order_data.get('Delivery_Date', '')
        if delivery_date == date:
            items = order_data.get('Items', [])
            for item in items:
                item_zone = item.get('Zone', '').upper()
                if item_zone == zone:
                    # Extracting relevant information
                    customer_id = item.get('Customer_ID', '')
                    sender_name = item.get('Sender', {}).get('Name', '')
                    sender_address = item.get('Sender', {}).get('Address', '')
                    sender_phone = item.get('Sender', {}).get('Phone', '')
                    receiver_name = item.get('Receiver', {}).get('Name', '')
                    receiver_address = item.get('Receiver', {}).get('Address', '')
                    receiver_phone = item.get('Receiver', {}).get('Phone', '')
                    weight = item.get('Weight', '')
                    parcel_number = item.get('Parcel_Number', '')
                    price = item.get('Price', '')

                    # Formatting and appending to result list
                    result_item = f"Customer ID: {customer_id}\nSender: {sender_name}\nAddress: {sender_address}\nPhone: {sender_phone}\nReceiver: {receiver_name}\nAddress: {receiver_address}\nPhone: {receiver_phone}\nWeight: {weight} kg\nParcel Number: {parcel_number}\nPrice: ${price}\n"
                    parcelResult.append(result_item)

    if parcelResult:
        print("Search Result:")
        for parcel in parcelResult:
            print("Date:", date)
            print("Destination Zone:", zone)
            print(parcel)
    else:
        print("No parcel on this date and destination zone.")


customer_details_to_check = ["Customer ID"]
consignment_id = "10000000"
parcel_number_base = 1000000

# Guides the user through creating a new consignment, gathering necessary information.
# Calculates prices, displays a detailed bill, and updates data files.
# Returns the new consignment ID and last parcel number.
def create_consignment(current_consignment_id, local_last_parcel_number, prices):
    recorded_info = {}

    local_last_parcel_number = load_data_from_json("last_parcel_number.txt")
    if local_last_parcel_number is None:
        local_last_parcel_number = 1000000

    for detail in customer_details_to_check:
        valid_input = False
        while not valid_input:
            customer_id_input = input(f"Enter {detail}: ")

            if customer_id_input in customer_database:
                print(f"{detail}: {customer_id_input} is recorded in our list.")
                print("We will now proceed to show you your details according to your ID.")
                recorded_info = customer_database[customer_id_input]
                valid_input = True
            else:
                print(f"{detail}: {customer_id_input} is not recorded in our list. Please try again.")

    # Confirm customer details
    print("\nThese are your details:")
    print("Customer ID:", customer_id_input)
    print("Your Name:", recorded_info.get("name", ""))
    print("Your Address:", recorded_info.get("address", ""))
    print("Your Telephone number:", recorded_info.get("phone", ""))

    while True:
        confirm = input("Are the recorded details correct? (yes/no): ").lower()
        if confirm == "yes":
            print("We will now proceed to creating your consignment bill.")
            break
        elif confirm == "no":
            print("Returning to the first stage.")
            return None, None
        else:
            print("Invalid input. Please enter 'yes' or 'no.'")

    items = []

    next_consignment_id = str(int(current_consignment_id) + 1)

    while next_consignment_id in consignment_details_dict:
        next_consignment_id = str(int(next_consignment_id) + 1)

    while True:
        # Get details for a single parcel
        print("\nDetails for the Parcel:")

        # Sender details for the parcel
        sender_name = input("Enter Sender's Name: ")
        sender_address = input("Enter Sender's Address: ")
        sender_phone = input("Enter Sender's Phone Number: ")

        # Receiver details for the parcel
        receiver_name = input("Enter Receiver's Name: ")
        receiver_address = input("Enter Receiver's Address: ")
        receiver_phone = input("Enter Receiver's Phone Number: ")

        while True:
            try:
                weight = float(input("Enter the weight of the item (in KG):"))
                if weight.is_integer():
                    weight = int(weight)
                break
            except:
                print("Invalid input for weight. Please enter a valid number.")

        while True:
            zone = input("Enter the delivery zone for the item (eg. 'Zone A'): ")
            if zone in ["Zone A", "Zone B", "Zone C", "Zone D", "Zone E"]:
                break
            else:
                print("Invalid delivery zone. Please enter a valid zone.")

        # Calculate the price based on weight and zone
        price = update_price(weight, zone, prices)

        if price is not None:
            print(f"\nCalculated Price: RM{price:.2f}")

            next_parcel_number = int(local_last_parcel_number) + 1
            print(f"Parcel Number: P{next_parcel_number}")

            items.append({
                "Customer_ID": customer_id_input,
                "Customer_Name": recorded_info.get("name", ""),
                "Sender": {
                    "Name": sender_name,
                    "Address": sender_address,
                    "Phone": sender_phone
                },
                "Receiver": {
                    "Name": receiver_name,
                    "Address": receiver_address,
                    "Phone": receiver_phone
                },
                "Weight": weight,
                "Parcel_Number": next_parcel_number,
                "Zone": zone,
                "Price": price,  # Add the calculated price to the parcel details
            })

            # Update local_last_parcel_number to the latest value
            local_last_parcel_number = next_parcel_number

            # Save the updated local_last_parcel_number to the file
            with open("last_parcel_number.txt", "w") as f:
                f.write(str(local_last_parcel_number))

            # Ask if the user wants to add another parcel to this consignment
            add_more = input("Do you want to add another parcel to this consignment? (yes/no): ").lower()
            if add_more != "yes":
                break
        else:
            # Handle the case where price is not found
            break

    # Continue with the rest of the consignment creation process
    total_price = calculate_total_price(items, prices)

    # Display the total amount for all items
    print(f"\nTotal Amount for All Items: RM{total_price:.2f}")

    # Display fully detailed bill
    print("\n Bill:")
    print("Customer ID:", customer_id_input)
    print("Your Name:", recorded_info.get("name", ""))
    print(f"Consignment ID: {next_consignment_id}")
    print(f"Delivery Date: {datetime.now().strftime('%d/%m/%Y')}")

    # Display sender's details for each parcel
    for i, consignment_item in enumerate(items, start=1):
        print(f"\n  - Item {i} - Sender's Details:")
        print(f"      - Sender's Name: {consignment_item['Sender']['Name']}")
        print(f"      - Sender's Address: {consignment_item['Sender']['Address']}")
        print(f"      - Sender's Phone: {consignment_item['Sender']['Phone']}")

        # Display receiver's details for each parcel
        print(f"      - Receiver's Name: {consignment_item['Receiver']['Name']}")
        print(f"      - Receiver's Address: {consignment_item['Receiver']['Address']}")
        print(f"      - Receiver's Phone: {consignment_item['Receiver']['Phone']}")

        # Display parcel details
        print(f"      - Parcel Number: P{consignment_item['Parcel_Number']}")
        print(f"      - Weight: {consignment_item['Weight']} kg")
        print(f"      - Delivery Zone: {consignment_item['Zone']}")
        print(f"      - Price: RM{consignment_item['Price']:.2f}")

    # Display total amount for all items
    print(f"\nTotal Amount: RM{total_price:.2f}")

    # Add Customer_ID to consignment_data
    consignment_data = {
        "Customer_ID": customer_id_input,
        "Delivery_Date": datetime.now().strftime('%d/%m/%Y'),
        "Items": items,
        "Total_Amount": total_price,
    }

    # Store consignment details in the dictionary using the consignment ID as the key
    consignment_details_dict[next_consignment_id] = consignment_data

    save_all_data()

    # Return the updated consignment ID and parcel number
    return next_consignment_id, local_last_parcel_number

# Guides the user through creating a new consignment, gathering necessary information.
# Calculates prices, displays a detailed bill, and updates data files.
# Returns the new consignment ID and last parcel number.
def search_consignment():
    while True:
        search_consignment_id = input("Enter the consignment ID to search: ")
        try:
            search_consignment_id = int(search_consignment_id)
            break
        except ValueError:
            print("Invalid input. Please enter a valid consignment ID.")

    search_consignment_id_str = str(search_consignment_id)

    if search_consignment_id_str in consignment_details_dict:
        print("\nConsignment Details:")
        searched_consignment_details = consignment_details_dict[search_consignment_id_str]
        print(f"Consignment ID: {search_consignment_id_str}")

        # Iterate through the "Items" list to find the customer ID
        customer_id_found = None
        for consignment_item in searched_consignment_details.get('Items', []):
            if 'Customer_ID' in consignment_item:
                customer_id_found = consignment_item['Customer_ID']
                break

        if customer_id_found:
            print(f"Customer ID: {customer_id_found}")
        else:
            print("Customer ID: N/A")

        for consignment_key, consignment_value in searched_consignment_details.items():
            if consignment_key != 'Items':
                print(f"{consignment_key}: {consignment_value}")

        # Display details for each item in the consignment
        for i, consignment_item in enumerate(searched_consignment_details.get('Items', []), start=1):
            print(f"\n  - Item {i} - Sender's Details:")
            print(f"      - Sender's Name: {consignment_item['Sender']['Name']}")
            print(f"      - Sender's Address: {consignment_item['Sender']['Address']}")
            print(f"      - Sender's Phone: {consignment_item['Sender']['Phone']}")

            # Display receiver's details for each parcel
            print(f"      - Receiver's Name: {consignment_item['Receiver']['Name']}")
            print(f"      - Receiver's Address: {consignment_item['Receiver']['Address']}")
            print(f"      - Receiver's Phone: {consignment_item['Receiver']['Phone']}")

            # Display parcel details
            print(f"      - Parcel Number: P{consignment_item['Parcel_Number']}")
            print(f"      - Weight: {consignment_item['Weight']} kg")
            print(f"      - Delivery Zone: {consignment_item['Zone']}")
            print(f"      - Price: ${consignment_item['Price']:.2f}")

        while True:
            confirm = input("Is this the correct consignment? (yes/no): ").lower()
            if confirm == "yes":
                print("Confirmed.")
                update_parcel_and_details(search_consignment_id_str, ParcelPrice)  # Call the update function
                break
            elif confirm == "no":
                print("Returning to the main menu.")
                return
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
    else:
        print(f"No consignment found with Consignment ID: {search_consignment_id_str}")

# Guides the user through updating details for a specific parcel within a consignment.
def update_parcel_and_details(consignment_id_param, prices):
    while True:
        parcel_number_input = input("Enter the parcel number to check (Without 'P'): ")
        try:
            parcel_number_input = int(parcel_number_input)
            break
        except ValueError:
            print("Invalid input. Please enter a valid parcel number.")

    # Check if the consignment ID exists
    if consignment_id_param in consignment_details_dict:
        consignment_details = consignment_details_dict[consignment_id_param]

        # Check if the parcel number exists in the consignment
        targeted_item = None
        for loop_item in consignment_details.get('Items', []):
            if loop_item['Parcel_Number'] == parcel_number_input:
                targeted_item = loop_item
                break

        if targeted_item:
            while True:
                print(f"\nDetails for Parcel Number P{parcel_number_input}:")
                print(f"  - Weight: {targeted_item['Weight']} kg")
                print(f"  - Destination Zone: {targeted_item['Zone']}")
                print("  - Sender Details:")
                print(f"      - Name: {targeted_item['Sender'].get('Name', '')}")
                print(f"      - Address: {targeted_item['Sender'].get('Address', '')}")
                print(f"      - Phone: {targeted_item['Sender'].get('Phone', '')}")
                print("  - Receiver Details:")
                print(f"      - Name: {targeted_item['Receiver'].get('Name', '')}")
                print(f"      - Address: {targeted_item['Receiver'].get('Address', '')}")
                print(f"      - Phone: {targeted_item['Receiver'].get('Phone', '')}")

                print("\nUpdate Options:")
                print("1. Update Weight")
                print("2. Update Destination")
                print("3. Update Sender Details")
                print("4. Update Receiver Details")
                print("5. Delete Parcel")
                print("6. Go back to Main Menu")
                update_option = input("Select an option (1/2/3/4/5/6): ").lower()

                if update_option == "1":
                    new_weight = input("Enter the new weight (in kg): ")
                    try:
                        new_weight = float(new_weight)
                        if new_weight.is_integer():
                            new_weight = int(new_weight)

                        targeted_item['Weight'] = new_weight
                        targeted_item['Price'] = update_price(targeted_item['Weight'], targeted_item['Zone'], prices)
                        print("Weight updated successfully.")
                        save_all_data()
                    except ValueError:
                        print("Invalid input for weight. Please enter a valid number.")
                elif update_option == "2":
                    new_zone = input("Enter the new destination zone (eg. 'Zone A'): ")
                    if new_zone in ("Zone A", "Zone B", "Zone C", "Zone D", "Zone E"):
                        targeted_item['Zone'] = new_zone
                        targeted_item['Price'] = update_price(targeted_item['Weight'], new_zone, prices)
                        print("Destination zone updated successfully.")
                        save_all_data()
                    else:
                        print("Invalid destination zone. Please enter a valid zone.")
                elif update_option == "3":
                    update_sender_details(targeted_item['Sender'])
                    print("Sender details updated successfully.")
                    save_all_data()
                elif update_option == "4":
                    update_receiver_details(targeted_item['Receiver'])
                    print("Receiver details updated successfully.")
                    save_all_data()
                elif update_option == "5":
                    confirm_delete = input(
                        f"Are you sure you want to delete Parcel Number P{parcel_number_input}? (yes/no): ").lower()
                    if confirm_delete == 'yes':
                        consignment_details['Items'].remove(targeted_item)
                        print(f"Parcel Number P{parcel_number_input} deleted successfully.")
                        save_all_data()
                        break
                    else:
                        print("Deletion canceled.")
                elif update_option == "6":
                    print("Returning to the Main Menu.")
                    return
                else:
                    print(
                        "Invalid input. Please enter '1' for weight, '2' for destination, '3' for sender details, '4' for receiver details, '5' for deletion, or '6' to go back to the Main Menu.")

                # Calculate and update the new total price
                new_total_price = calculate_total_price(consignment_details.get('Items', []), prices)
                consignment_details['Total_Amount'] = new_total_price
                print(f"New Total Amount: {new_total_price}")

            save_all_data()

            print(f"\nUpdated Total Amount for All Items: ${new_total_price:.2f}")

            print("\nUpdated Consignment Bill:")
            print(f"Consignment ID: {consignment_id_param}")
            print(f"Customer ID: {consignment_details.get('Customer_ID', '')}")
            print(f"Delivery Date: {consignment_details.get('Delivery_Date', '')}")
            print("Items:")
            for i, consignment_item in enumerate(consignment_details.get('Items', []), start=1):
                print(f"  - Item {i}:")
                print(f"      - Weight: {consignment_item['Weight']} kg")
                print(f"      - Parcel Number: P{consignment_item['Parcel_Number']}")
                print(f"      - Delivery Zone: {consignment_item['Zone']}")
                print(f"      - Price: RM{update_price(consignment_item['Weight'], consignment_item['Zone'], consignment_item['Price']):.2f}")
                print("      - Sender Details:")
                print(f"          - Name: {consignment_item['Sender'].get('Name', '')}")
                print(f"          - Address: {consignment_item['Sender'].get('Address', '')}")
                print(f"          - Phone: {consignment_item['Sender'].get('Phone', '')}")
                print("      - Receiver Details:")
                print(f"          - Name: {consignment_item['Receiver'].get('Name', '')}")
                print(f"          - Address: {consignment_item['Receiver'].get('Address', '')}")
                print(f"          - Phone: {consignment_item['Receiver'].get('Phone', '')}")
            print(f"Total Amount: ${new_total_price:.2f}")

        else:
            print(f"No item found with Parcel Number P{parcel_number_input} in Consignment ID: {consignment_id_param}.")
    else:
        print(f"No consignment found with Consignment ID: {consignment_id_param}")

# Guides the user through updating details for the sender of a parcel.
def update_sender_details(sender_details):
    while True:
        print("\nUpdate Sender Details:")
        print("1. Edit Sender's Name")
        print("2. Edit Sender's Address")
        print("3. Edit Sender's Phone")
        print("4. Go back")

        option = input("Select an option (1/2/3/4): ")

        if option == "1":
            sender_details['Name'] = input("Enter sender's new name: ")
            print("Sender's Name updated successfully.")
        elif option == "2":
            sender_details['Address'] = input("Enter sender's new address: ")
            print("Sender's Address updated successfully.")
        elif option == "3":
            sender_details['Phone'] = input("Enter sender's new phone: ")
            print("Sender's Phone updated successfully.")
        elif option == "4":
            print("Returning to the previous menu.")
            break
        else:
            print("Invalid input. Please enter '1', '2', '3', or '4'.")

# Guides the user through updating details for the receiver of a parcel.
def update_receiver_details(receiver_details):
    while True:
        print("\nUpdate Receiver Details:")
        print("1. Edit Receiver's Name")
        print("2. Edit Receiver's Address")
        print("3. Edit Receiver's Phone")
        print("4. Go back")

        option = input("Select an option (1/2/3/4): ")

        if option == "1":
            receiver_details['Name'] = input("Enter receiver's new name: ")
            print("Receiver's Name updated successfully.")
        elif option == "2":
            receiver_details['Address'] = input("Enter receiver's new address: ")
            print("Receiver's Address updated successfully.")
        elif option == "3":
            receiver_details['Phone'] = input("Enter receiver's new phone: ")
            print("Receiver's Phone updated successfully.")
        elif option == "4":
            print("Returning to the previous menu.")
            break
        else:
            print("Invalid input. Please enter '1', '2', '3', or '4'.")

# Searches for and displays consignment details based on a consignment number.
def search_consignment_by_number(consignment_number):
    consignment_number_str = str(consignment_number)
    if consignment_number_str in consignment_details_dict:
        print("\nConsignment Details:")
        searched_consignment_details = consignment_details_dict[consignment_number_str]
        print(f"Consignment ID: {consignment_number_str}")

        for consignment_key, consignment_value in searched_consignment_details.items():
            if consignment_key == 'Items':
                print(f"\n{consignment_key}:")
                for consignment_item in consignment_value:
                    print(f"  - Item {consignment_item['Parcel_Number']}:")
                    print(f"      - Weight: {consignment_item['Weight']} kg")
                    print(f"      - Parcel Number: P{consignment_item['Parcel_Number']}")
                    print(f"      - Delivery Zone: {consignment_item['Zone']}")
                    print(f"      - Price: ${consignment_item['Price']:.2f}")
                    print("      - Sender's Details:")
                    print(f"          - Name: {consignment_item['Sender']['Name']}")
                    print(f"          - Address: {consignment_item['Sender']['Address']}")
                    print(f"          - Phone: {consignment_item['Sender']['Phone']}")
                    print("      - Receiver's Details:")
                    print(f"          - Name: {consignment_item['Receiver']['Name']}")
                    print(f"          - Address: {consignment_item['Receiver']['Address']}")
                    print(f"          - Phone: {consignment_item['Receiver']['Phone']}")
            else:
                print(f"\n{consignment_key}: {consignment_value}")

        while True:
            confirm = input("Is this the correct consignment? (yes/no): ").lower()
            if confirm == "yes":
                print("Confirmed.")
                break
            elif confirm == "no":
                print("Returning to the main menu.")
                return
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
    else:
        print(f"No consignment found with Consignment Number: {consignment_number_str}")

# Prompts the user to enter a customer ID and displays all bills associated with that customer.
def view_customer_bills():
    while True:
        customer_id_to_view = input("Enter the customer ID to view bills: ")
        if customer_id_to_view in customer_database:
            print("\nCustomer Bills:")
            total_amount = 0
            for inner_consignment_id, consignment_details in consignment_details_dict.items():
                if consignment_details["Customer_ID"] == customer_id_to_view:
                    print(f"Consignment ID: {inner_consignment_id}")
                    print(f"Customer ID: {consignment_details.get('Customer_ID', '')}")
                    print(
                        f"Delivery Date: {datetime.strptime(consignment_details['Delivery_Date'], '%d/%m/%Y').strftime('%d/%m/%Y')}")
                    print(f"Total Amount: ${consignment_details['Total_Amount']:.2f}")
                    print("Items:")
                    # Display details for each item in the consignment
                    for i, consignment_item in enumerate(consignment_details.get('Items', []), start=1):
                        print(f"\n  - Item {i} - Sender's Details:")
                        print(f"      - Sender's Name: {consignment_item['Sender']['Name']}")
                        print(f"      - Sender's Address: {consignment_item['Sender']['Address']}")
                        print(f"      - Sender's Phone: {consignment_item['Sender']['Phone']}")

                        # Display receiver's details for each parcel
                        print(f"      - Receiver's Name: {consignment_item['Receiver']['Name']}")
                        print(f"      - Receiver's Address: {consignment_item['Receiver']['Address']}")
                        print(f"      - Receiver's Phone: {consignment_item['Receiver']['Phone']}")

                        # Display parcel details
                        print(f"      - Parcel Number: P{consignment_item['Parcel_Number']}")
                        print(f"      - Weight: {consignment_item['Weight']} kg")
                        print(f"      - Delivery Zone: {consignment_item['Zone']}")
                        print(f"      - Price: ${consignment_item['Price']:.2f}")

                    total_amount += consignment_details['Total_Amount']

            print(f"Total Amount for Customer {customer_id_to_view}: ${total_amount:.2f}")
            break
        else:
            print(f"Customer ID {customer_id_to_view} not found. Please try again.")

# Provides options to view customer bills based on a specific date or within a date range.
def view_customer_bills_by_date():
    while True:
        print("Options:")
        print("1. View bills by a specific date")
        print("2. View bills within a date range")
        print("3. Back to the main menu")

        option = input("Enter your choice (1, 2, or 3): ")

        if option == "1":
            specific_date_str = input("Enter the date (DD/MM/YYYY): ")
            try:
                specific_date = datetime.strptime(specific_date_str, "%d/%m/%Y")
                break
            except ValueError:
                print("Invalid date format. Please enter a date in the format DD/MM/YYYY.")
        elif option == "2":
            start_date_str = input("Enter the start date (DD/MM/YYYY): ")
            end_date_str = input("Enter the end date (DD/MM/YYYY): ")
            try:
                start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
                end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
                break
            except ValueError:
                print("Invalid date format. Please enter dates in the format DD/MM/YYYY.")
        elif option == "3":
            print("Returning to the main menu.")
            return
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    print("\nCustomer Bills:")
    total_amount = 0
    for inner_consignment_id, consignment_details in consignment_details_dict.items():
        delivery_date = datetime.strptime(consignment_details["Delivery_Date"], "%d/%m/%Y")

        if (option == "1" and delivery_date == specific_date) or (
                option == "2" and start_date <= delivery_date <= end_date
        ):
            print(f"Consignment ID: {inner_consignment_id}")
            print(f"Delivery Date: {delivery_date.strftime('%d/%m/%Y')}")
            print(f"Total Amount: ${consignment_details['Total_Amount']:.2f}")

            for inner_item in consignment_details["Items"]:
                print(f"  - Parcel Number: P{inner_item['Parcel_Number']}")
                print(f"    - Weight: {inner_item['Weight']} kg")
                print(f"    - Zone: {inner_item['Zone']}")

            print()
            total_amount += consignment_details["Total_Amount"]

    print(f"Total Amount for Selected Date/Range: ${total_amount:.2f}")


def operatorMenu():
    current_consignment_id = "10000000"  # You can use the initial consignment ID value
    local_last_parcel_number = "1000000"
    ParcelPrice = load_data_from_json("parcel_prices.json")
    while True:
        print("\nMenu:")
        print("\n1. Add customer details")
        print("2. Modify customer address/ telephone number")
        print("3. View customer list")
        print("4. Clear customer list")
        print("5. Check price of parcel")
        print("6. Generate list of parcels")
        print("7. Create a new consignment")
        print("8. Search for a consignment ID to modify")
        print("9. Search for a consignment ID to check")
        print("10. View Customer Bills and Total Amount")
        print("11. View Customer Bills by Date")
        print("12. Clear consignment data file")
        print("0. Exit")

        while True:
            choice = input("Enter your choice (0 - 12): ")
            if choice.isdigit() and 0 <= int(choice) <= 12: # Checks the validity of input from user
                break # Proceed if the input is valid
            else: # OUTPUT "Invalid choice. Please enter a valid option (0 - 12)."
                print("Invalid choice. Please enter a valid option (0 - 12).")

        if choice == "1": # IF Operator add customer details
            addCustomerDetails()
        elif choice == "2": # ELIF Operator modify customer address and telephone number
            modifyCustomerAddressTelephone()
        elif choice == "3": # ELIF Operator view customer list
            viewCustomerList()
        elif choice == "4": # ELIF Operator clear customer list
            customer_database, last_customer_ID = clear_customer_file()
            print("Customer data cleared.")
        elif choice == "5": # ELIF Operator check parcel price
            checkPrice(ParcelPrice)
        elif choice == "6": # ELIF Operator generate parcel list
            generateParcelList()
        elif choice == "7": # ELIF Operator create consignment 
            consignment_id, last_parcel_number = create_consignment(current_consignment_id, local_last_parcel_number, ParcelPrice)
        elif choice == "8": # ELIF Operator search consignment id to modify
            search_consignment()
        elif choice == "9": # ELIF Operator search consignment id to check 
            while True:
                consignment_number_to_search = input("Enter the consignment number to search: ")
                try:
                    consignment_number_to_search = int(consignment_number_to_search)
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid consignment number.")
            search_consignment_by_number(consignment_number_to_search)
        elif choice == "10": # ELIF Operator view customer bill and total amount 
            view_customer_bills()
        elif choice == "11": # ELIF Operator view customer bill by date 
            view_customer_bills_by_date()
        elif choice == "12": # ELIF Operator clear consignment file
            consignment_details_dict = clear_consignment_file()
            print("Consignment data cleared.")
        elif choice == "0": # ELIF Operator exits
            print("Exiting the program. Goodbye!")
            break
        else: # OUTPUT "Invalid choice. Please enter 0 - 12"
            print("Invalid choice. Please enter 0 - 12")

        while True:
            another_operation = input("Do you want to perform another operation? (yes/no): ").lower()
            if another_operation in ["yes", "no"]:
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        if another_operation == "no":
            print("Exiting the program. Goodbye!")
            break


# Creating an empty dictionary to store user data
user_data = {}

# Initialize user_data from the file
initialize_user_data()

# Starting the program
ask_user()

# Save the data before exiting
save_user_data()






