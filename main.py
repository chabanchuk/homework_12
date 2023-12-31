from collections import UserDict
from datetime import datetime
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


class Birthday(Field):
    def is_validate(self, value):
        return datetime.strptime(value, "%d-%m-%Y")


class Phone(Field):
    def is_validate(self, value):
        return value.isdigit() and len(value) == 10


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        if birthday:
            self.birthday = Birthday(birthday)

    def add_phone(self, value):
        self.phones.append(Phone(value))

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                break
        else:
            raise ValueError(f"Phone number {old_phone} not found")

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                break
        else:
            raise ValueError(f"Phone number {phone} not found")

    def find_phone(self, value):
        for phone in self.phones:
            if value == phone.value:
                return phone

    def __str__(self):
        contact_name = f"Contact name: {self.name.value}"
        phones = f"phones: {'; '.join(p.value for p in self.phones)}"
        return f"{contact_name}, {phones}"

    def days_to_birthday(self):
        if self.birthday:
            now = datetime.now()
            birthday_date = datetime.strptime(self.birthday.value, "%d-%m-%Y")
            next_birthday = datetime(now.year, birthday_date.month,
                                     birthday_date.day)
            if now > next_birthday:
                next_birthday = datetime(now.year + 1,
                                         birthday_date.month,
                                         birthday_date.day)
            return (next_birthday - now).days
        else:
            raise ValueError("Birthday not set")


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
            _phone = any(value in phone.value for phone in record.phones)
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
            json.dump(self.data, file)

    def load_file(self, filename):
        with open(filename, 'r') as file:
            self.data = json.load(file)
