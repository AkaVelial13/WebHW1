from contact_manager import run_contact_manager
from note_manager import run_note_manager
from event_manager import run_event_manager
from file_sorter import run_file_sorter, counter
from base_view import ConsoleView
from common import clear_console, CommandHandler


def run_contact_manager_wrapper():
    clear_console()
    run_contact_manager()


def run_note_manager_wrapper():
    clear_console()
    run_note_manager()


def run_event_manager_wrapper():
    clear_console()
    run_event_manager()


def run_file_manager_wrapper():
    clear_console()
    file_manager_menu(ConsoleView())


def exit_program():
    clear_console()
    exit()


def run():
    view = ConsoleView()
    commands = {
        '1': ('Contact Manager', run_contact_manager_wrapper),
        '2': ('Note Manager', run_note_manager_wrapper),
        '3': ('Event Manager', run_event_manager_wrapper),
        '4': ('File Manager', run_file_manager_wrapper),
        '0': ('Exit', exit_program)
    }
    handler = CommandHandler(commands, view)

    while True:
        choice = view.display_menu("Main Menu", handler.get_commands_for_display())
        handler.handle_command(choice)


def run_file_sorter_wrapper():
    clear_console()
    run_file_sorter()
    counter()


def return_to_main_menu():
    clear_console()


def file_manager_menu(view):
    commands = {
        '1': ('Sort Files', run_file_sorter_wrapper),
        '0': ('Return to Main Menu', return_to_main_menu)
    }
    handler = CommandHandler(commands, view)

    while True:
        choice = view.display_menu("File Manager V0.1", handler.get_commands_for_display())
        if choice == '0':
            break
        handler.handle_command(choice)


if __name__ == '__main__':
    run()
