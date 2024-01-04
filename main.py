from collections import UserDict
import json


class Field:
    def __init__(self, value):
        if not self.is_validate(value):
            raise ValueError("Invalid value type")
        self.__value = value

    def __str__(self):
        return str(self.__value)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not self.is_validate(value):
            raise ValueError("Invalid value type")
        self.__value = value

    def is_validate(self, value):
        return True


class Name(Field):
    pass


class Phone(Field):
    def is_validate(self, value):
        return value.isdigit() and len(value) == 10


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = None

    def add_phone(self, value):
        self.phone = Phone(value)

    def edit_phone(self, new_phone):
        if self.phone is not None:
            self.phone.value = new_phone
        else:
            raise ValueError(f"Phone number {self.phone} not found")

    def remove_phone(self):
        self.phone = None

    def __str__(self):
        contact_name = f"Name: {self.name.value}"
        phone = f"phone: {self.phone.value}"
        return f"{contact_name}, {phone}"


class AddressBook(UserDict):
    def add_record(self, record):
        if record.name.value not in self.data:
            self.data[record.name.value] = record
        else:
            raise ValueError(f"Record: {record.name.value} already exists.")

    def find(self, value):
        result = []
        for record in self.data.values():
            _name = value in record.name.value
            _phone = value in record.phone.value
            if _name or _phone:
                result.append(record)
        return result

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, n):
        records = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i: i + n]

    def save_file(self, filename):
        with open(filename, 'w') as file:
            data_save = {
                str(i + 1): {
                    "name": record.name.value,
                    "phone": record.phone.value
                }
                for i, record in enumerate(self.data.values())
            }
            json.dump(data_save, file, indent=4, ensure_ascii=False)
        return self.data

    def load_file(self, filename):
        try:
            with open(filename, 'r') as file:
                data_loaded = json.load(file)
            self.data = {}
            for key, record_data in data_loaded.items():
                record = Record(record_data["name"])
                if record_data["phone"]:
                    record.add_phone(record_data["phone"])
                self.data[key] = record

        except FileNotFoundError:
            print(f"File {filename} not found. A new file will be created.")


def input_error(func):
    def wrappper(*args):
        try:
            result = func(*args)
        except KeyError:
            return "Enter the command, name or phone number correctly."
        except ValueError:
            return "Enter the command, name or phone number correctly."
        except IndexError:
            return "Enter the command, name or phone number correctly."
        except TypeError:
            return "Enter the command, name or phone number correctly."
        except Exception:
            return "Enter the command, name or phone number correctly."
        return result
    return wrappper


@input_error
def bot_hello():
    return "How can I help you?"


@input_error
def bot_add_contact(name, phone_number):
    if name not in dict_contacts:
        record = Record(name)
        record.add_phone(phone_number)
        dict_contacts.add_record(record)
        return "Contact details saved."
    else:
        return "A contact with this name already exists."


@input_error
def bot_change_phone(name, new_phone):
    for _, record in dict_contacts.data.items():
        if record.name.value == name:
            record.edit_phone(new_phone)
            return f"Phone number for {name} changed to {new_phone}."
    return "Contact with this name does not exist."


@input_error
def bot_get_phone(name):
    for _, record in dict_contacts.data.items():
        if record.name.value == name:
            return record.phone.value
    return "Contact with this name does not exist."


@input_error
def bot_show_all():
    if not dict_contacts:
        return "The contact list is empty."
    else:
        return "\n".join([str(record) for record in dict_contacts.values()])


@input_error
def bot_find(value):
    results = dict_contacts.find(value)
    if results:
        return "\n".join(str(record) for record in results)
    else:
        return "No contacts found."


@input_error
def bot_exit():
    dict_contacts.save_file("data.json")
    return "Good bye!"


@input_error
def bot_check_command():
    raise ValueError


@input_error
def main():
    handler = {
        "hello": bot_hello,
        "add": bot_add_contact,
        "change": bot_change_phone,
        "phone": bot_get_phone,
        "show all": bot_show_all,
        "good bye": bot_exit,
        "close": bot_exit,
        "exit": bot_exit,
        "find": bot_find
    }
    while True:
        user_input = input(">>> ").lower()
        args = user_input.split()

        if len(args) > 1 and f"{args[0]} {args[1]}" in handler:
            handler_name = f"{args[0]} {args[1]}"
            args = args[2:]
        else:
            handler_name = args[0]
            args = args[1:]

        if handler_name not in handler:
            result = bot_check_command()
            print(result)
        else:
            result = handler[handler_name](*args)
            print(result)

        if result == "Good bye!":
            break


if __name__ == "__main__":
    dict_contacts = AddressBook()
    dict_contacts.load_file("data.json")
    main()
