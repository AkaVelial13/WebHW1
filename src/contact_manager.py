from models import ObjectValidateError, AddressBook, Record, Name, Address, Phone, Email, Birthday
from common import CommandHandler, handle_error
from base_view import ContactConsoleView


class UserInputHandler:
    @staticmethod
    @handle_error
    def get_user_name(required=False):
        while True:
            name = input('Name: ')
            if not name:
                if required:
                    print("Name is required.")
                else:
                    return None
            else:
                return name

    @staticmethod
    @handle_error
    def get_user_phones(required=False):
        while True:
            phones_input = input('Phones (comma-separated, 10 digits only): ')
            if required and not phones_input:
                print("At least one phone number is required.")
                continue
            phones = [phone.strip() for phone in phones_input.split(',')]
            all_valid = True
            for phone in phones:
                try:
                    Phone(phone)
                except ObjectValidateError as e:
                    print(f"Validation error occurred: {e}")
                    all_valid = False
                    break
            if all_valid:
                return phones

    @staticmethod
    @handle_error
    def get_user_email(required=False):
        while True:
            email = input('Email (optional): ')
            if required and not email:
                print("Email is required.")
                continue
            if not email:
                return None
            try:
                Email(email)
            except ObjectValidateError as e:
                print(f"Validation error occurred: {e}")
                continue
            return email

    @staticmethod
    @handle_error
    def get_user_birthday(required=False):
        while True:
            birthday = input('Birthday (optional, dd.mm.yyyy): ')
            if required and not birthday:
                print("Birthday is required.")
                continue
            if not birthday:
                return None
            try:
                Birthday(birthday)
            except ObjectValidateError as e:
                print(f"Validation error occurred: {e}")
                continue
            return birthday

    @staticmethod
    @handle_error
    def get_user_address(required=False):
        while True:
            address = input('Address (optional, max length 25): ')
            if required and not address:
                print("Address is required.")
                continue
            if not address:
                return None
            try:
                Address(address)
            except ObjectValidateError as e:
                print(f"Validation error occurred: {e}")
                continue
            return address

    @staticmethod
    def get_user_output(entity, required=False):
        if entity == 'name':
            return UserInputHandler.get_user_name(required)
        elif entity == 'phone':
            return UserInputHandler.get_user_phones(required)
        elif entity == 'email':
            return UserInputHandler.get_user_email(required)
        elif entity == 'birthday':
            return UserInputHandler.get_user_birthday(required)
        elif entity == 'address':
            return UserInputHandler.get_user_address(required)


class ContactManager:
    """Class to manage contacts."""

    def __init__(self, address_book, view):
        """
        Initialize ContactManager.

        :param address_book: The address book containing contacts.
        :param view: The view for displaying messages.
        """
        self.address_book = address_book
        self.view = view
        self.user_input_handler = UserInputHandler()

    @handle_error
    def handle_add_contact(self):
        """
        Handle the addition of a new contact.
        """
        name = self.user_input_handler.get_user_output('name', required=True)
        if not name:
            return

        if self.address_book.find(name):
            self.view.display_error(f'Contact with name "{name}" already exists.')
            return

        phones = self.user_input_handler.get_user_output('phone', required=True)
        if not phones:
            return

        email = self.user_input_handler.get_user_output('email', required=False)
        birthday = self.user_input_handler.get_user_output('birthday', required=False)
        address = self.user_input_handler.get_user_output('address', required=False)

        record = Record(name, email=email, birthday=birthday, address=address)
        record.phones.extend(Phone(phone_number) for phone_number in phones)
        self.address_book.add_record(record)
        self.address_book.save_data_to_file()
        self.view.display_message(f'Contact {name} added.Contact details: ')
        self.view.display_contact_details(record)

    @handle_error
    def handle_change_contact(self):
        """
        Handle the modification of an existing contact.
        """
        name_to_change = self.user_input_handler.get_user_output('name', required=True)
        if not name_to_change:
            return

        contact = self.address_book.find(name_to_change)
        if contact:
            name = self.user_input_handler.get_user_output('New name')
            phones = self.user_input_handler.get_user_output('phone')
            email = self.user_input_handler.get_user_output('email', required=False)
            birthday = self.user_input_handler.get_user_output('birthday', required=False)
            address = self.user_input_handler.get_user_output('address', required=False)

            contact.name = Name(name) if name else contact.name
            contact.phones = [Phone(phone) for phone in phones] if phones else contact.phones
            if email:
                contact.add_email(email)
            if birthday:
                contact.set_birthday(birthday)
            if address:
                contact.add_address(address)

            self.address_book.save_data_to_file()
            self.view.display_message(f'Contact {name_to_change} changed.Updated details: ')
            self.view.display_contact_details(contact)
        else:
            self.view.display_error(f'Contact with name "{name_to_change}" not found.')

    @handle_error
    def handle_delete_contact(self):
        """
        Handle the deletion of a contact.
        """
        name = self.view.get_input("Enter the name of the contact to delete: ")
        if self.address_book.find(name):
            self.address_book.delete(name)
            self.address_book.save_data_to_file()
            self.view.display_message(f"Contact '{name}' successfully deleted.")
        else:
            self.view.display_error(f"Contact with the name '{name}' not found.")

    @handle_error
    def handle_get_contact_by_name(self):
        """
        Handle retrieving contact information by name.
        """
        name = self.view.get_input("Enter the name of the contact to search for: ")
        record = self.address_book.find(name)
        if record:
            self.view.display_contact_details(record)
        else:
            self.view.display_error(f"Contact with the name '{name}' not found.")

    @handle_error
    def handle_search_contacts(self):
        """
        Handle searching for contacts based on a query.
        """
        query = self.view.get_input("Enter the query to search for contacts: ")
        found_contacts = self.address_book.search_full(query)
        if found_contacts:
            self.view.display_message("Found contacts:")
            for contact in found_contacts:
                self.view.display_contact_details(contact)
        else:
            self.view.display_error(f"No contacts found for the query '{query}'.")

    def handle_display_all_contacts(self):
        """
        Handle displaying all contacts.
        """
        try:
            if not self.address_book.data:
                raise ValueError("The address book is empty.")
            self.view.display_all_contacts(self.address_book)
        except ValueError as e:
            self.view.display_error(str(e))

    @handle_error
    def handle_congratulate(self):
        """
        Handles the congratulate command.

        Asks the user to input the number of days for congratulations.
        If a valid number is provided, it congratulates all contacts whose birthdays are within the specified number
         of days.
        If no contacts with birthday information are found, it displays a message accordingly.

        Raises:
            ValueError: If the input provided is not a valid number.
        """
        days = self.view.get_input("Enter the number of days for congratulations: ")
        try:
            days = int(days)
            congratulation_list = []

            for record in self.address_book.data.values():
                if record.birthday and record.is_in_range(days):
                    congratulation_list.append(record)

            if congratulation_list:
                result = f'\nCongratulations to the following contacts, whose birthday is in the next {days} days:\n'
                for record in congratulation_list:
                    result += f'{record.name.value} - Birthday: {record.birthday.value}\n'
            else:
                result = f'No contacts have birthdays in the next {days} days.'

            self.view.display_contact_details(result)

        except ValueError:
            self.view.display_error("Please enter a valid number of days.")


class ContactCommandHandler(CommandHandler):
    """Command handler for contact management."""
    def __init__(self, manager, view):
        """
        Initialize ContactCommandHandler.

        :param manager: The ContactManager instance.
        :param view: The view for displaying messages.
        """
        self.manager = manager
        commands = {
            '1': ("Add contact", manager.handle_add_contact),
            '2': ("Change contact", manager.handle_change_contact),
            '3': ("Delete contact", manager.handle_delete_contact),
            '4': ("Get contact info", manager.handle_get_contact_by_name),
            '5': ("Search", manager.handle_search_contacts),
            '6': ("Show all contacts", manager.handle_display_all_contacts),
            '7': ("Greets", manager.handle_congratulate),
            '0': ("Return to main menu", self.return_to_main_menu())
        }
        super().__init__(commands, view)


def run_contact_manager():
    """
    Run the contact manager program.
    """

    program_name = "Contact Manager V0.1"
    view = ContactConsoleView()
    address_book = AddressBook()
    address_book.load_data_from_file()
    manager = ContactManager(address_book, view)
    contact_command_handler = ContactCommandHandler(manager, view)

    while True:
        options = contact_command_handler.get_commands_for_display()
        choice = view.display_menu(program_name, options)
        if choice == '0':
            return
        else:
            contact_command_handler.handle_command(choice)


if __name__ == '__main__':
    run_contact_manager()

