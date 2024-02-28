from functools import wraps
import os


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def handle_error(func):
    """
    Decorator to handle errors in the functions.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            args[0].view.display_error(str(e))
    return wrapper

# def handle_error(func):
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         try:
#             return func(*args, **kwargs)
#         except KeyError:
#             return 'Some error'
#         except ValueError:
#             return 'Some error'
#         except IndexError:
#             return 'Some error'
#         except PermissionError as e:
#             return f'No access rights! {str(e)}'
#         except Exception as e:
#             return f'An unexpected error occurred: {str(e)}'
#     return wrapper


class CommandHandler:
    def __init__(self, commands, view):
        self.commands = commands
        self.view = view

    def handle_command(self, choice):
        command_tuple = self.commands.get(choice)
        if command_tuple:
            command_function = command_tuple[1]
            if callable(command_function):
                command_function()
            else:
                self.view.display_message('Command not executable.')
        else:
            self.view.display_message('Invalid command')

    def get_commands_for_display(self):
        """
        Returns a dictionary of commands for display purposes.

        The dictionary keys are command identifiers (typically strings),
        and the values are the descriptions of the commands.
        """
        return {cmd: desc for cmd, (desc, _) in self.commands.items()}

    def return_to_main_menu(self):
        """
        Return to the main menu.
        """
        return
