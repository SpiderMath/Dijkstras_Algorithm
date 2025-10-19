import time
import sys
from utils import Style, clear_screen
import tests

# menu_structure:- nested dict to represent menu structure
menu_structure = {
    "Test on a real-world dataset": {
        "Adjacency Matrix + Unordered List implementation": tests.dijkstra_adj_matrix.test(dataset="CUSTOM"),
        "Adjacency List + Binary Heap implementation": tests.dijkstra_adj_list_bin_heap.test(dataset="CUSTOM"),
        "Adjacency List + Fibonacci Heap implementation": tests.dijkstra_adj_list_fib_heap.test(dataset="CUSTOM"),
        "Compare various implementations": tests.comparisons.test(dataset="CUSTOM"),
    },
    "Test a custom dataset (your dataset should be in tests.txt)": {
        "Adjacency Matrix + Unordered List implementation": tests.dijkstra_adj_matrix.test(dataset="CUSTOM"),
        "Adjacency List + Binary Heap implementation": tests.dijkstra_adj_list_bin_heap.test(dataset="CUSTOM"),
        "Adjacency List + Fibonacci Heap implementation": tests.dijkstra_adj_list_fib_heap.test(dataset="CUSTOM"),
        "Compare various implementations": tests.comparisons.test(dataset="CUSTOM"),
    },
    "Benchmark on our testing datasets": {
        "Adjacency Matrix + Unordered List implementation": tests.dijkstra_adj_matrix.test(dataset="CUSTOM"),
        "Adjacency List + Binary Heap implementation": tests.dijkstra_adj_list_bin_heap.test(dataset="CUSTOM"),
        "Adjacency List + Fibonacci Heap implementation": tests.dijkstra_adj_list_fib_heap.test(dataset="CUSTOM"),
        "Compare various implementations": tests.comparisons.test(dataset="CUSTOM"),
    },
    "Exit": sys.exit  # The action for "Exit" is to call sys.exit
}

# --- Main Application Logic ---
def display_menu(menu, breadcrumbs):
    while True:
        clear_screen()

        # Display header and breadcrumbs
        print(f"{Style.BLUE}{Style.BOLD}--- Command Line Interface ---{Style.RESET}")
        if breadcrumbs:
            print(f"Current Path: {Style.CYAN}{' > '.join(breadcrumbs)}{Style.RESET}\n")
        else:
            print("Welcome! Please select an option below.\n")

        options = list(menu.keys())

        for i, option in enumerate(options, 1):
            print(f"  {Style.YELLOW}{i}.{Style.RESET} {option}")

        if breadcrumbs:
            print(f"  {Style.YELLOW}0.{Style.RESET} Back")

        choice = input("\nEnter your choice: ")

        if not choice.isdigit():
            print(f"\n{Style.RED}Invalid input. Please enter a number.{Style.RESET}")
            time.sleep(1)
            continue

        choice_index = int(choice)

        # Handle "Back" option
        if breadcrumbs and choice_index == 0:
            return # Exit this submenu level, going back up the call stack

        # Validate choice range
        if not (1 <= choice_index <= len(options)):
            print(f"\n{Style.RED}Invalid choice. Please select a number from the list.{Style.RESET}")
            time.sleep(1)
            continue

        # Process selection
        selection_key = options[choice_index - 1]
        selection_value = menu[selection_key]

        if isinstance(selection_value, dict):
            # if the value is a dictionary, it's a submenu.
            new_breadcrumbs = breadcrumbs + [selection_key]
            display_menu(selection_value, new_breadcrumbs)
        else:
            clear_screen()
            print(f"Executing: {Style.GREEN}{' > '.join(breadcrumbs + [selection_key])}{Style.RESET}\n")
            selection_value()
            print(f"\n{Style.BOLD}Task finished. Exiting now.{Style.RESET}")
            time.sleep(2)
            sys.exit(0)


def main():
    try:
        display_menu(menu_structure, [])
    except KeyboardInterrupt:
        print("\n\nExiting application. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
