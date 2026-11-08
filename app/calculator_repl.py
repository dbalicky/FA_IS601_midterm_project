from decimal import Decimal
import logging

from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver, LoggingObserver
from app.operations import OperationFactory
from app.input_validators import InputValidator

from colorama import Fore, Style, init

init(autoreset=True)


def calculator_repl():
    """
    Command-line interface for the calculator.

    Implements a Read-Eval-Print Loop (REPL) that continuously prompts the user
    for commands, processes arithmetic operations, and manages calculation history.
    """
    try:
        # Initialize the Calculator instance
        calc = Calculator()

        # Register observers for logging and auto-saving history
        calc.add_observer(LoggingObserver())
        calc.add_observer(AutoSaveObserver(calc))

        print("Calculator started. Type 'help' for commands.")

        while True:
            try:
                # Prompt the user for a command
                command = input("\nEnter command: ").lower().strip()

                if command == 'help':
                    # Display available commands
                    print(Fore.CYAN + "\nAvailable commands:" + Style.RESET_ALL)
                    print(Fore.CYAN + "  add, subtract, multiply, divide, power, root, modulus, integer divide, percent, absolute difference" + Style.RESET_ALL)
                    print(Fore.CYAN + "  history - Show calculation history" + Style.RESET_ALL)
                    print(Fore.CYAN + "  clear - Clear calculation history" + Style.RESET_ALL)
                    print(Fore.CYAN + "  undo - Undo the last calculation" + Style.RESET_ALL)
                    print(Fore.CYAN + "  redo - Redo the last undone calculation" + Style.RESET_ALL)
                    print(Fore.CYAN + "  save - Save calculation history to file" + Style.RESET_ALL)
                    print(Fore.CYAN + "  load - Load calculation history from file" + Style.RESET_ALL)
                    print(Fore.CYAN + "  exit - Exit the calculator" + Style.RESET_ALL)
                    continue

                if command == 'exit':
                    # Save history on exit only if auto-save enabled

                    if calc.config.auto_save:
                        try:
                            calc.save_history()
                            print(Fore.GREEN + "History saved successfully." + Style.RESET_ALL)
                        except Exception as e:
                            print(Fore.YELLOW + f"Warning: Could not save history: {e}" + Style.RESET_ALL)
                            
                    print("Goodbye!")
                    break

                if command == 'history':
                    # Display calculation history
                    history = calc.show_history()
                    if not history:
                        print("No calculations in history")
                    else:
                        print(Fore.CYAN + "\nCalculation History:" + Style.RESET_ALL)
                        for i, entry in enumerate(history, 1):
                            print(f"{i}. {entry}")
                    continue

                if command == 'clear':
                    # Clear calculation history
                    calc.clear_history()
                    print(Fore.CYAN + "History cleared" + Style.RESET_ALL)
                    continue

                if command == 'undo':
                    # Undo the last calculation
                    if calc.undo():
                        print(Fore.CYAN + "Operation undone" + Style.RESET_ALL)
                    else:
                        print("Nothing to undo")
                    continue

                if command == 'redo':
                    # Redo the last undone calculation
                    if calc.redo():
                        print(Fore.CYAN + "Operation redone" + Style.RESET_ALL)
                    else:
                        print("Nothing to redo")
                    continue

                if command == 'save':
                    # Save calculation history to file
                    try:
                        calc.save_history()
                        print(Fore.GREEN + "History saved successfully" + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"Error saving history: {e}" + Style.RESET_ALL)
                    continue

                if command == 'load':
                    # Load calculation history from file
                    try:
                        calc.load_history()
                        print(Fore.GREEN + "History loaded successfully" + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.RED + f"Error loading history: {e}" + Style.RESET_ALL)
                    continue

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root', 'modulus', 'integer divide', 'percent', 'absolute difference']:
                    # Perform the specified arithmetic operation
                    try:
                        print(Fore.CYAN + "\nEnter numbers (or 'cancel' to abort):" + Style.RESET_ALL)
                        a = input("First number: ")
                        if a.lower() == 'cancel':
                            print(Fore.YELLOW + "Operation cancelled" + Style.RESET_ALL)
                            continue

                        # Validate the first number before continuing with the operations
                        a = InputValidator.validate_number(a, calc.config)

                        b = input("Second number: ")
                        if b.lower() == 'cancel':
                            print(Fore.YELLOW + "Operation cancelled" + Style.RESET_ALL)
                            continue

                        # Validate the second number before performing the operation
                        b = InputValidator.validate_number(b, calc.config)

                        # Create the appropriate operation instance using the Factory pattern
                        operation = OperationFactory.create_operation(command)
                        calc.set_operation(operation)

                        # Perform the calculation
                        result = calc.perform_operation(a, b)

                        # Format the result according to the configured precision
                        if isinstance(result, Decimal):
                            display_result = f"{result:.{calc.config.precision}f}"
                            display_result = display_result.rstrip('0').rstrip('.') if '.' in display_result else display_result
                        else:
                            display_result = str(result)

                        print(f"\nResult: {display_result}")
                    except (ValidationError, OperationError) as e:
                        # Handle known exceptions related to validation or operation errors
                        print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
                    except Exception as e:
                        # Handle any unexpected exceptions
                        print(Fore.RED + f"Unexpected error: {e}" + Style.RESET_ALL)
                    continue

                # Handle unknown commands
                print(Fore.CYAN + f"Unknown command: '{command}'. Type 'help' for available commands." + Style.RESET_ALL)

            except KeyboardInterrupt:
                # Handle Ctrl+C interruption gracefully
                print(Fore. YELLOW + "\nOperation cancelled" + Style.RESET_ALL)
                continue
            except EOFError:
                # Handle end-of-file (e.g., Ctrl+D) gracefully
                print("\nInput terminated. Exiting...")

                if calc.config.auto_save:
                    try:
                        calc.save_history()
                        print(Fore.GREEN + "History saved successfully." + Style.RESET_ALL)
                    except Exception as e:
                        print(Fore.YELLOW + f"Warning, could not save successfully: {e}" + Style.RESET_ALL)
                        
                break
            except Exception as e:
                # Handle any other unexpected exceptions
                print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
                continue

    except Exception as e:
        # Handle fatal errors during initialization
        print(Fore.RED + f"Fatal error: {e}" + Style.RESET_ALL)
        logging.error(Fore.RED + f"Fatal error in calculator REPL: {e}" + Style.RESET_ALL)
        raise