from abc import ABC, abstractmethod
from tabulate import tabulate
from colorama import Fore


class BaseView(ABC):
    @abstractmethod
    def display_message(self, message):
        """
        Displays a message to the user.
        """
        pass

    @abstractmethod
    def get_input(self, prompt):
        """
        Requests input from the user with a prompt.
        """
        pass

    @abstractmethod
    def display_error(self, message):
        """
        """
        pass

    @abstractmethod
    def display_program_name(self, program_name):
        """
        Displays the name of the program.
        """
        pass

    @abstractmethod
    def display_menu(self, program_name, options):
        """
        Displays a menu with options.
        """
        pass

    @abstractmethod
    def get_confirmation(self, message):
        """
        Requests confirmation from the user (yes/no).
        """
        pass

    @abstractmethod
    def display_note_details(self, note):
        pass

    @abstractmethod
    def format_title(self, text):
        pass

    @abstractmethod
    def format_content(self, text):
        pass


class ConsoleView(BaseView):
    def display_message(self, message):
        print(message)

    def get_input(self, prompt):
        return input(prompt)

    def display_error(self, message):
        """
        Displays an error message to the user in light green color.
        """
        print(f"\033[92mError: {message}\033[0m")

    def display_program_name(self, program_name):
        print(f'{Fore.CYAN}{program_name}{Fore.RESET}')

    def display_menu(self, program_name, commands):
        """
        Displays the menu with options for the user in a visually appealing format using colorama.

        Args:
            program_name (str): The title of the menu.
            commands (dict): Dictionary of commands where the key is the command number
                             and the value is the description of the command.
        """
        self.display_program_name(program_name)
        for cmd, desc in commands.items():
            print(f"{Fore.YELLOW}{cmd}. {Fore.LIGHTWHITE_EX}{desc}{Fore.RESET}")
        choice = input(f"{Fore.CYAN}Please choose an option: {Fore.RESET}")
        return choice

    def get_confirmation(self, message):
        response = input(f'{message} (yes/no): ')
        return response.lower() in ['yes']

    def format_title(self, text):
        return f'{Fore.BLUE}{text}{Fore.RESET}'

    def format_content(self, text):
        return f'{Fore.LIGHTWHITE_EX}{text}{Fore.RESET}'

    def display_note_details(self, note):
        pass

    def display_notes_list(self, notes):
        pass

    def display_event_details(self, event):
        pass

    def display_contact_details(self, contact):
        pass

    def display_events_list(self, events):
        pass

    def display_contacts_list(self, contacts):
        pass


class NoteConsoleView(ConsoleView):

    def display_note_details(self, note):
        details = [
            [self.format_title('Title'), self.format_content(note.title)],
            [self.format_title('Date'), self.format_content(note.note_date)],
            [self.format_title('Tags'), self.format_content(", ".join(note.tags))],
            [self.format_title('Content'), self.format_content(note.content)]
        ]
        print(tabulate(details, tablefmt='pretty'))

    def display_notes_list(self, notes):
        headers = ['No', 'Title', 'Date', 'Tags',
                   'Content']
        notes_table = [
            [self.format_content(i + 1), self.format_content(note.title),
             self.format_content(note.note_date), self.format_content(", ".join(note.tags)),
             self.format_content(note.content)]
            for i, note in enumerate(notes)
        ]
        print(tabulate(notes_table, headers=[self.format_title(header) for header in headers], tablefmt='pretty'))


class EventConsoleView(ConsoleView):

    def display_event_details(self, event):
        """
        Displays detailed information about a single event.

        :param event: The event to display.
        """
        details = [
            [self.format_title('Title'), self.format_content(event.title)],
            [self.format_title('Date and Time'), self.format_content(event.date_time.strftime('%Y-%m-%d %H:%M'))],
            [self.format_title('Tags'), self.format_content(", ".join(event.tags))]
        ]
        print(tabulate(details, tablefmt='pretty'))

    def display_events_list(self, events):
        """
        Displays a list of events.

        :param events: An iterable of event objects to display.
        """
        headers = ['No', 'Title', 'Date and Time', 'Tags']
        events_table = [
            [
                self.format_content(str(index + 1)),
                self.format_content(event.title),
                self.format_content(event.date_time.strftime('%Y-%m-%d %H:%M')),
                self.format_content(", ".join(event.tags))
            ] for index, event in enumerate(events)
        ]
        print(tabulate(events_table, headers=[self.format_title(header) for header in headers], tablefmt='pretty'))


class ContactConsoleView(ConsoleView):

    def display_contact_details(self, contact):
        details = [
            [self.format_title('Name'), self.format_content(contact.name)],
            [self.format_title('Phones'), self.format_content(', '.join(phone.value for phone in contact.phones))]
        ]

        if contact.email:
            details.append([self.format_title('Email'), self.format_content(contact.email)])

        if contact.address:
            details.append([self.format_title('Address'), self.format_content(contact.address)])

        if contact.birthday:
            details.append([self.format_title('Birthday'), self.format_content(contact.birthday)])

        print(tabulate(details, tablefmt="pretty"))

    def display_all_contacts(self, address_book, page_size=10):
        contacts_list = list(address_book.data.values())
        total_pages = len(contacts_list) // page_size + (1 if len(contacts_list) % page_size > 0 else 0)

        for page_number in range(total_pages):
            start_index = page_number * page_size
            end_index = start_index + page_size
            page = contacts_list[start_index:end_index]

            headers = ['No', 'Name', 'Phones', 'Email', 'Address', 'Birthday']
            contacts_table = [
                [
                    self.format_content(str(index + 1)),
                    self.format_content(contact.name),
                    self.format_content(', '.join([phone.value for phone in contact.phones])),
                    self.format_content(contact.email if contact.email else ''),
                    self.format_content(contact.address if contact.address else ''),
                    self.format_content(contact.birthday if contact.birthday else '')
                ] for index, contact in enumerate(page)
            ]

            print(tabulate(contacts_table, headers=[self.format_title(header) for header in headers], tablefmt='pretty'))
            if page_number < total_pages - 1:
                input('Press Enter для continue...')

