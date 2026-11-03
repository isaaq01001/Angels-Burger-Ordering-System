"""
Angels Burger Ordering System
Group: DevOps Dynamics
Period 2 Core Python Console System

This program is a local, console-based ordering and billing system.
Data is stored only during the current execution session.
"""

# VARIABLES AND THE DATA STRUCTURES. A DICTIONARY WHERE WE STORED THE MENU ITEMS OF THE ANGEL BURGER AND ITS PRICES.

STAFF_USERNAME = "admin"
STAFF_PASSWORD = "1234"

MENU = {
    1: {"name": "Classic Burger", "price": 120.00},
    2: {"name": "Cheeseburger", "price": 95.00},
    3: {"name": "Extra large Burger", "price": 110.00},
    4: {"name": "Regular Burger", "price": 85.00},
    5: {"name": "Iced Tea", "price": 45.00},
}

orders = []
next_order_id = 1

# THIS IS WHERE THE SYSTEM VALIDATES THE INPUT OF THE USER. THEN IT WILL CHECK IF THE INPUT IS A DIGIT
#  AND IF IT IS WITHIN THE RANGE OF THE MENU ITEMS. IF NOT IT WILL PRINT THE ERROR MESASGE.

def get_integer(prompt, minimum=None, maximum=None):
    """Return a valid integer within an optional range."""
    while True:
        value = input(prompt).strip()
        if not value.isdigit():
            print("Invalid input. Please enter a whole number.")
            continue

        number = int(value)

        if minimum is not None and number < minimum:
            print(f"Please enter a number from {minimum} to {maximum}.")
            continue

        if maximum is not None and number > maximum:
            print(f"Please enter a number from {minimum} to {maximum}.")
            continue

        return number


# LOGIN SYSTEM. STAFF'S LOGIN SYSTEM ARE SEPARATED FROM THE CUSTOMER'S LOGIN SYSTEM.

def login():
    """Validate staff credentials and return True for successful login."""
    attempts = 3

    while attempts > 0:
        print("\n========== STAFF LOGIN ==========")
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if username == STAFF_USERNAME and password == STAFF_PASSWORD:
            print("Login successful.")
            return True
        elif username != STAFF_USERNAME:
            print("Invalid username.")
        else:
            print("Invalid password.")

        attempts -= 1
        if attempts > 0:
            print(f"Attempts remaining: {attempts}")

    print("Too many failed attempts. System closed. please try again later.")
    return False

# MENU DISPLAY, THIS IS WHERE THE SYSTEM WILL DISPLAY THE MENU ITEMS AND ITS PRICES.
# THEN DIRECTLY PASSED DOWN TO THE ORDER ENTRY FUNCTION WHERE THE CUSTOMER WILL SELECT THE ITEM AND QUANTITY.

def display_menu():
    """Display all available food and drink items."""
    print("\n================ ANGELS BURGER MENU ================")
    print(f"{'No.':<5}{'Item':<25}{'Price':>10}")
    print("-" * 40)

    for number, item in MENU.items():
        print(f"{number:<5}{item['name']:<25}PHP {item['price']:>7.2f}")

    print("-" * 40)

# ORDER ENTRY, THIS IS WHERE THE SYSTEM CAPTURES THE CUSTOMER'S ORDER AND STORES IT IN A DICTIONARRY.
# THEN PASSED DOWN TO THE CALCULATE TOTAL FUNCTION TO COMPUTE THE TOTAL AMOUNT OF THE ORDER.

def create_order():
    """Capture a customer order and return the completed order dictionary."""
    global next_order_id

    # No customer name is required; the system identifies the order by its ID.
    customer = f"Order #{next_order_id}"
    items = []

    while True:
        display_menu()
        choice = get_integer("Enter item number (0 to finish): ", 0, len(MENU))

        if choice == 0:
            if not items:
                print("No items were added. Order cancelled.")
                return None
            break

        quantity = get_integer("Enter quantity: ", 1, 99)
        selected = MENU[choice]

        line_total = selected["price"] * quantity

        items.append({
            "item": selected["name"],
            "price": selected["price"],
            "quantity": quantity,
            "line_total": line_total
        })

        print(
            f"Added {quantity} x {selected['name']} "
            f"= PHP {line_total:.2f}"
        )

        more = input("Add another item? Yes/No: ").strip().lower()
        if more != "yes":
            break

    subtotal = calculate_total(items)

    # COLLECT PAYMENT BEFORE CONFIRMING THE ORDER.
    print("\n================ PAYMENT ================")
    print(f"Order ID: {next_order_id}")
    print(f"Total amount due: PHP {subtotal:.2f}")
    print("Please pay before the order is confirmed.")

    while True:
        try:
            paid_input = input("Amount paid by customer (PHP): ").strip()
            amount_paid = float(paid_input)
            if amount_paid < 0:
                print("Amount paid cannot be negative. Please try again.")
            elif amount_paid < subtotal:
                print(f"Insufficient payment. Please pay at least PHP {subtotal:.2f}.")
            else:
                break
        except ValueError:
            print("Invalid amount. Enter a number, such as 150 or 150.50.")

    change = amount_paid - subtotal

    order = {
        "id": next_order_id,
        "customer": customer,
        "items": items,
        "total": subtotal,
        "amount_paid": amount_paid,
        "change": change,
        "status": "Pending",
        "payment_status": "PAID"
    }

    print(f"Amount paid: PHP {amount_paid:.2f}")
    print(f"Change: PHP {change:.2f}")
    print("Payment received. Order confirmed.")

    next_order_id += 1
    return order

# CALCULATIONS, THIS IS WHERE THE SYSTEM WILL AUTOMATICALLY CALCULATE THE TOTAL AMOUNT OF THE ORDER BASED ON THE QUANTITY AND PRICE OF THE ITEM.

def calculate_total(items):
    """Calculate and return the total amount of all order lines."""
    total = 0.0

    for item in items:
        total += item["price"] * item["quantity"]

    return total

# RECEIPT AND BILLING SYSTEM.

def print_bill(order):
    """Display the customer's bill."""
    print("\n============ANGELS BURGER============")
    print("\n================ BILL ================")
    print(f"Order ID : {order['id']}")
    print(f"Customer : {order['customer']}")
    print("-" * 40)

    for item in order["items"]:
        print(
            f"{item['quantity']} x {item['item']} "
            f"@ PHP {item['price']:.2f} = "
            f"PHP {item['line_total']:.2f}"
        )

    print("-" * 40)
    print(f"TOTAL PAYMENT: PHP {order['total']:.2f}")
    print(f"AMOUNT PAID  : PHP {order.get('amount_paid', 0.0):.2f}")
    print(f"CHANGE       : PHP {order.get('change', 0.0):.2f}")
    print(f"ORDER STATUS : {order['status']}")
    print(f"PAYMENT STATUS: {order.get('payment_status', 'UNPAID')}")
    print("=" * 40)

# ORDER QUEUE, THIS IS WHERE THE ACTIVE ORDERS ARE BEING SHOWN. THE STAFF CAN SEE THE STATUS OF THE ORDER AND THE CUSTOMER NAME.

def view_orders():
    """this is where the active orders are displayed"""
    print("\n=============== ACTIVE ORDER QUEUE ===============")

    if not orders:
        print("No orders recorded in the current session.")
        return

    for order in orders:
        print(
            f"Order #{order['id']} | Customer: {order['customer']} | "
            f"Total: PHP {order['total']:.2f} | Status: {order['status']} | "
            f"Payment: {order.get('payment_status', 'UNPAID')}"
        )

    print("===================================================")

# ORDER STATUS UPDATE: STAFF CAN MARK AN ORDER AS COMPLETED.

def update_order_status():
    """Mark an existing order as Completed."""
    if not orders:
        print("There are no orders to update.")
        return

    view_orders()
    order_id = get_integer("Enter order ID to mark as completed: ", 1)

    for order in orders:
        if order["id"] == order_id:
            if order["status"] == "Completed":
                print(f"Order #{order['id']} is already Completed.")
                return

            print("\n1. Completed")
            confirm = get_integer("Choose 1 to mark this order as Completed: ", 1, 1)
            if confirm == 1:
                order["status"] = "Completed"
                print(f"Order #{order['id']} status updated to Completed.")
            return

    print("Order ID not found. Please check the order ID and try again.")

# FIND ORDER, IT FINDS THE ORDER BY ITS ID AND PRINTS THE BILL AND THE SAME AS THE SATUS OF THE ORDER.  

def update_payment_status():
    """Collect payment for an unpaid order; never mark an order paid without payment."""
    if not orders:
        print("There are no orders to update.")
        return

    view_orders()
    order_id = get_integer("Enter order ID to process payment: ", 1)

    for order in orders:
        if order["id"] == order_id:
            print(f"Customer: {order['customer']}")
            print(f"Amount due: PHP {order['total']:.2f}")
            print(f"Current payment status: {order.get('payment_status', 'UNPAID')}")

            if order.get("payment_status") == "PAID":
                print(f"Amount paid: PHP {order.get('amount_paid', order['total']):.2f}")
                print(f"Change: PHP {order.get('change', 0.0):.2f}")
                print("This order has already been paid.")
                return

            while True:
                try:
                    amount_paid = float(input("Enter amount received (PHP): ").strip())
                    if amount_paid < order["total"]:
                        print(f"Insufficient payment. Please receive at least PHP {order['total']:.2f}.")
                    else:
                        break
                except ValueError:
                    print("Invalid amount. Enter a number, such as 150 or 150.50.")

            order["amount_paid"] = amount_paid
            order["change"] = amount_paid - order["total"]
            order["payment_status"] = "PAID"
            print("Payment received successfully.")
            print(f"Amount paid: PHP {order['amount_paid']:.2f}")
            print(f"Change: PHP {order['change']:.2f}")
            return

    print("Order ID not found. Please check the order ID and try again.")


def find_order():
    """Find and display one order by its ID."""
    if not orders:
        print("No orders recorded.")
        return

    order_id = get_integer("Enter order ID: ", 1)

    for order in orders:
        if order["id"] == order_id:
            print_bill(order)
            return

    print("Order ID not found.")

# CUSTOMER ORDER UPDATE AND MENU: customers access their order using the order ID.

def customer_order_login():
    """Allow a customer to access their order using only the order ID."""
    if not orders:
        print("\nNo customer orders are available yet.")
        return None

    attempts = 3

    while attempts > 0:
        print("\n========= CUSTOMER ORDER UPDATE AND MENU =========")
        order_id = get_integer("Enter your Order ID: ", 1)

        for order in orders:
            if order["id"] == order_id:
                print("Order ID accepted.")
                return order

        attempts -= 1
        print("Order ID not found. Please check your order ID.")
        if attempts > 0:
            print(f"Attempts remaining: {attempts}")

    print("Too many failed attempts. Returning to the main screen.")
    return None


def customer_order_update_menu(order):
    """Allow a logged-in customer to view menu, status, and receipt."""
    while True:
        print("\n=========== CUSTOMER ORDER UPDATE AND MENU ===========")
        print(f"Welcome, {order['customer']}!")
        print("1. View Menu")
        print("2. View My Order Status")
        print("3. View My Receipt")
        print("4. Exit")
        print("=====================================")

        choice = get_integer("Select an option: ", 1, 4)

        if choice == 1:
            display_menu()
        elif choice == 2:
            print(f"\nOrder #{order['id']} Status: {order['status']}")
        elif choice == 3:
            print_bill(order)
        else:
            print("Thank You For Using The Angels Burger Ordering System.")
            break

# MAIN MENU

def main_menu():
    """Run the staff system flow until the employee chooses Exit."""
    while True:
        print("\n============== ANGELS BURGER STAFF SYSTEM ==============")
        print("1. Display Menu")
        print("2. Enter Customer Order")
        print("3. View Active Order Queue")
        print("4. Update Order Preparation Status")
        print("5. View Order Bill")
        print("6. Update Payment Status")
        print("7. Logout")
        print("==================================================")

        choice = get_integer("Select an option: ", 1, 7)

        if choice == 1:
            display_menu()
        elif choice == 2:
            order = create_order()
            if order is not None:
                orders.append(order)
                print(f"Order #{order['id']} successfully recorded.")
                print_bill(order)
        elif choice == 3:
            view_orders()
        elif choice == 4:
            update_order_status()
        elif choice == 5:
            find_order()
        elif choice == 6:
            update_payment_status()
        else:
            print("\nStaff logged out.")
            break

# PROGRAM START

def main():
    """Start the system and allow staff or customer access."""
    while True:
        print("\n=====================================================")
        print("              ANGELS BURGER ORDERING SYSTEM")
        print("=====================================================")
        print("1. Staff Login")
        print("2. Customer Order Update and Menu")
        print("3. Exit")
        print("=====================================================")

        choice = get_integer("Select user type: ", 1, 3)

        if choice == 1:
            if login():
                main_menu()
        elif choice == 2:
            order = customer_order_login()
            if order is not None:
                customer_order_update_menu(order)
        else:
            print("\nThank you for using the Angels Burger Ordering System.")
            break


if __name__ == "__main__":
    main()
