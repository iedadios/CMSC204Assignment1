# ---------- BUS CONFIGURATION ----------
ROWS = 10
COLS = 5
MAX_CAPACITY = 50

# 10x5 seating layout (0 = empty, 1 = occupied)
bus_seats = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Same size as bus_seats, stores the stop where the passenger boarded
boarded_at = [[None for _ in range(COLS)] for _ in range(ROWS)]

# ---------- CIRCULAR LINKED LIST FOR STOPS ----------
class StopNode:
    def __init__(self, name):
        self.name = name
        self.next = None  # points to the next stop
        self.boarded = 0  # passengers boarded at this stop
        self.alighted = 0  # passengers alighted at this stop


# Initialize 5 fixed stops in a circular linked list
stop_names = ["Stop A", "Stop B", "Stop C", "Stop D", "Stop E"]
head_stop = None
prev_node = None

for name in stop_names:
    node = StopNode(name)
    if not head_stop:
        head_stop = node
    if prev_node:
        prev_node.next = node
    prev_node = node

# Make it circular
prev_node.next = head_stop
current_stop = head_stop
total_passengers = 0  # total passengers on the bus

# ---------- SEAT FUNCTIONS ----------
def count_available_seats():
    return sum(seat == 0 for row in bus_seats for seat in row)

def board_passengers_at_stop():
    global current_stop, total_passengers

    stop_name = current_stop.name
    print(f"\nBus arrived at {stop_name}")

    try:
        num = int(input("Enter number of passengers boarding at this stop: "))
    except ValueError:
        print("Invalid input. No passengers boarded.")
        num = 0

    available = count_available_seats()

    if available == 0:
        print("Bus is FULL! No passengers can board.")
    elif num <= 0:
        print("No passengers boarded.")
    else:
        if num > available:
            print(f"Only {available} seats available.")
            num = available

        added = 0
        for i in range(ROWS):
            for j in range(COLS):
                if bus_seats[i][j] == 0 and added < num:
                    bus_seats[i][j] = 1
                    boarded_at[i][j] = stop_name
                    added += 1

        current_stop.boarded += added
        total_passengers += added
        print(f"{added} passenger(s) boarded at {stop_name}")

    # Move to next stop
    current_stop = current_stop.next
    print(f"Next stop: {current_stop.name}")

def alight_passengers_at_stop():
    global current_stop, total_passengers

    stop_name = current_stop.name
    print(f"\nBus arrived at {stop_name}")

    occupied = MAX_CAPACITY - count_available_seats()

    if occupied == 0:
        print("Bus is EMPTY! No passengers can alight.")
        current_stop = current_stop.next
        print(f"Next stop: {current_stop.name}")
        return

    # Show occupied seats
    print("\nOccupied Seats:")
    for i in range(ROWS):
        for j in range(COLS):
            if bus_seats[i][j] == 1:
                seat_number = i * COLS + j + 1
                print(f"Seat {seat_number:02} → Boarded at {boarded_at[i][j]}")

    while True:
        seats_input = input(
            "Enter seat numbers to alight (comma separated, e.g., 3,7,10): ").strip()

        if seats_input == "":
            print("No passengers alighted.")
            break

        parts = seats_input.split(",")

        # Validate all inputs are digits
        if not all(part.strip().isdigit() for part in parts):
            print("Invalid input! Use numbers separated by commas.")
            continue

        seat_numbers = [int(part.strip()) for part in parts]

        # Check range and occupancy
        valid = True
        for seat_number in seat_numbers:

            if seat_number < 1 or seat_number > MAX_CAPACITY:
                print(f"Seat {seat_number} is out of range.")
                valid = False
                break

            row = (seat_number - 1) // COLS
            col = (seat_number - 1) % COLS

            if bus_seats[row][col] == 0:
                print(f"Seat {seat_number} is already empty.")
                valid = False
                break

        if not valid:
            continue

        # Remove selected passengers
        for seat_number in seat_numbers:
            row = (seat_number - 1) // COLS
            col = (seat_number - 1) % COLS

            bus_seats[row][col] = 0
            boarded_at[row][col] = None
            total_passengers -= 1
            current_stop.alighted += 1

        print(f"{len(seat_numbers)} passenger(s) alighted at {stop_name}")
        break

    # Move to next stop
    current_stop = current_stop.next
    print(f"Next stop: {current_stop.name}")


def display_status():
    occupied = MAX_CAPACITY - count_available_seats()

    # Traverse circular list and build stop info
    node = head_stop
    stops_list = []
    route_visual = []

    while True:
        # Count passengers still onboard from this stop
        onboard_from_stop = 0
        for i in range(ROWS):
            for j in range(COLS):
                if boarded_at[i][j] == node.name:
                    onboard_from_stop += 1

        # Build stop info for statistics
        stops_list.append(
            f"{node.name} | Boarded: {node.boarded} | "
            f"Alighted: {node.alighted} | "
            f"Still On Bus: {onboard_from_stop}"
        )

        # Build stop label for visual route
        label = node.name
        if node == current_stop:
            label += " (CURRENT)"
        route_visual.append(label)

        node = node.next
        if node == head_stop:
            break

    # Display bus status
    print("\n----- BUS STATUS -----")
    print(f"Current Stop: {current_stop.name}")
    print(f"Total Stops: {len(stops_list)}\n")

    # Display circular route visual
    print("Route (Circular Visual):")
    print(" → ".join(route_visual))
    print("  ↖" + "─" * (len(" → ".join(route_visual))) + "↩ (circular)\n")

    # Display detailed statistics per stop
    print("Route Statistics (Boarded / Alighted / Still On Bus):")
    for stop_info in stops_list:
        print(f"  {stop_info}")

    print(f"\nOccupied Seats: {occupied}")
    print(f"Available Seats: {count_available_seats()}/{MAX_CAPACITY}")
    print(f"Total Passengers Onboard: {total_passengers}")
    print("----------------------\n")

# ---------- ADDITIONAL STOPS ----------
def add_additional_stop():
    global prev_node

    new_name = input("Enter name of new stop: ").strip()

    if not new_name:
        print("Stop name cannot be empty.\n")
        return

    # Check for duplicate stop name
    node = head_stop
    while True:
        if node.name.lower() == new_name.lower():
            print(f"A stop with the name '{new_name}' already exists.\n")
            return
        node = node.next
        if node == head_stop:
            break

    # Create and insert new stop after last node
    new_node = StopNode(new_name)
    new_node.next = head_stop
    prev_node.next = new_node
    prev_node = new_node  # update last node pointer

    print(f"{new_name} added to route.\n")

# ---------- REMOVE BUS STOP ----------
def delete_stop():
    global head_stop, current_stop, prev_node

    if not head_stop:
        print("No stops available.\n")
        return

    stop_name = input("Enter stop name to delete: ").strip().lower()

    current = head_stop
    prev = None

    while True:
        if current.name.lower() == stop_name:

            # Case 1: Only one stop exists
            if current.next == current:
                print("Cannot delete the only remaining stop.\n")
                return

            # Case 2: Deleting head_stop
            if current == head_stop:
                # Find last node
                last = head_stop
                while last.next != head_stop:
                    last = last.next

                head_stop = current.next
                last.next = head_stop

            else:
                prev.next = current.next

            # If deleting last node, update prev_node
            if current == prev_node:
                prev_node = prev

            # If deleting current active stop
            if current == current_stop:
                current_stop = current.next

            print(f"{current.name} deleted successfully.\n")
            return

        prev = current
        current = current.next

        if current == head_stop:
            break

    print("Stop not found.\n")

# ---------- SEARCH STOP ----------
def search_bus_stop():
    # Search for a bus stop by name and display passengers boarded/alighted.
    node = head_stop
    found = False

    route_name = input("Enter a bus stop name: ").strip().lower()

    while True:
        if node.name.lower() == route_name:

            # Count passengers still onboard from this stop
            onboard_from_stop = 0
            for i in range(ROWS):
                for j in range(COLS):
                    if boarded_at[i][j] == node.name:
                        onboard_from_stop += 1

            print(f"\nStop Found: {node.name}")
            print(f"Passengers Boarded: {node.boarded}")
            print(f"Passengers Alighted: {node.alighted}")
            print(f"Passengers Still On Bus: {onboard_from_stop}\n")

            found = True
            break

        node = node.next
        if node == head_stop:
            break

    if not found:
        print("Stop not found.\n")

# ---------- DISPLAY ALL PASSENGER SEATS ----------
def display_passenger_seats():
    print("\n--- Passenger Seat Layout ---")
    seat_number = 1
    for i in range(ROWS):
        for j in range(COLS):
            if bus_seats[i][j] == 0:
                print(f"Seat {seat_number:02} (Row {i+1}, Col {j+1}) → Empty")
            else:
                print(f"Seat {seat_number:02} (Row {i+1}, Col {j+1}) → Boarded at: {boarded_at[i][j]} (Still On Bus)")
            seat_number += 1
    print("-------------------------------\n")

# ---------- SEARCH SEAT NUMBERS ----------
def search_passenger_seats():
    print("\n--- Search Passengers by Seat Numbers ---")
    seats_input = input(f"Enter seat numbers (comma separated, e.g., 3,7,10): ").strip()

    if seats_input == "":
        print("No seats entered.\n")
        return

    # Split input and validate
    parts = seats_input.split(",")
    if not all(part.strip().isdigit() for part in parts):
        print("Invalid input! Use numbers separated by commas.\n")
        return

    seat_numbers = [int(part.strip()) for part in parts]

    for seat_number in seat_numbers:
        if seat_number < 1 or seat_number > MAX_CAPACITY:
            print(f"Seat {seat_number} is out of range (1-{MAX_CAPACITY}).")
            continue

        # Convert seat number → row & column
        row = (seat_number - 1) // COLS
        col = (seat_number - 1) % COLS

        if bus_seats[row][col] == 0:
            print(f"Seat {seat_number:02} (Row {row+1}, Col {col+1}) → Empty")
        else:
            print(f"Seat {seat_number:02} (Row {row+1}, Col {col+1}) → Boarded at: {boarded_at[row][col]} (Still On Bus)")

    print("-------------------------------\n")

# ---------- MENU ----------
def menu():
    while True:
        print("===== SMART BUS SYSTEM =====")
        print("1. Board Passengers at Current Stop")
        print("2. Add Additional Stop")
        print("3. Display Bus Status")
        print("4. Alight Passengers")
        print("5. Search specific seat number(s)")
        print("6. Show all Passenger Seats")
        print("7. Search Bus Stop")
        print("8. Remove Bus Stop")
        print("9. Exit")

        choice = input("Enter choice (1-9): ")

        if choice == "1":
            board_passengers_at_stop()
        elif choice == "2":
            add_additional_stop()
        elif choice == "3":
            display_status()
        elif choice == "4":
            alight_passengers_at_stop()
        elif choice == "5":
            search_passenger_seats()
        elif choice == "6":
            display_passenger_seats()
        elif choice == "7":
            search_bus_stop()
        elif choice == "8":
            delete_stop()
        elif choice == "9":
            print("Exiting system.")
            break
        else:
            # Invalid choice handling
            print("Invalid choice. Please enter a number between 1 and 9.\n")

# Run system
menu()
